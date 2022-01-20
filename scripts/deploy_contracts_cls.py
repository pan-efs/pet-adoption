from dataclasses import dataclass
import logging

from brownie import (
    accounts, 
    config, 
    Contract, 
    network, 
    MockV3Aggregator
)


@dataclass(frozen=True)
class BlockChains:
    LOCAL = ["development", "ganache-local"]
    FORKED_LOCAL = ["mainnet-fork"]
    MOCK_CONTRACT = {
        "eth_usd_price_feed": MockV3Aggregator
        }
    DECIMALS = 8
    INITIAL_VALUE = 200000000000


@dataclass(frozen=True)
class Deploying(BlockChains):
    
    logging.basicConfig(
        format='%(asctime)s - %(message)s', 
        datefmt='%d-%b-%y %H:%M:%S',
        level=logging.INFO
    )
    
    def get_account(self, index=None, id=None):
        if index:
            account = accounts[index]
            logging.info(f"Get account: {account}")
            return account
        
        if id:
            account = accounts.load(id)
            logging.info(f"Get account: {account}")
            return account
        
        if(network.show_active() in Deploying.LOCAL or network.show_active() in Deploying.FORKED_LOCAL):
            account = accounts[0]
            logging.info(f"Get account: {account}")
            return account
        
        account = accounts.add(config["wallets"]["from_key"])
        logging.info(f"Get account: {account}")
        return account
    
    
    def get_contract(self, contract_name: str):
        contract_type = Deploying.MOCK_CONTRACT[contract_name]
        
        if network.show_active() in Deploying.LOCAL:
            if len(contract_type) <= 0: self.deploy_mocks(
                                                Deploying.DECIMALS,
                                                Deploying.INITIAL_VALUE
                                            )
            
            contract = contract_type[-1]
        
        else:
            contract_address = config["networks"][network.show_active()][contract_name]
            
            contract = Contract.from_abi(
                contract_type._name,
                contract_address,
                contract_type.abi
            )
        
        logging.info(f"Get contract: {contract}")
        return contract
    
    
    def deploy_mocks(self, decimals, initial_value):
        account = self.get_account()
        
        MockV3Aggregator.deploy(
            decimals, 
            initial_value, 
            {"from": account}
        )
        
        logging.info(f"Deploy mocks: {account}")