import logging
from dotenv import load_dotenv

from brownie import (
    DogAdoption,
    config,
    network,
    MockV3Aggregator
)
from web3 import Web3

from scripts.deploy_contracts_cls import Deploying


load_dotenv()

logging.basicConfig(
        format='%(asctime)s - %(message)s', 
        datefmt='%d-%b-%y %H:%M:%S',
        level=logging.INFO
    )

deploying = Deploying()

def deploy_dog_adoption():
    account = deploying.get_account()
    
    dog_adoption = DogAdoption.deploy(
        deploying.get_contract("eth_usd_price_feed"),
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify")
    )
    
    logging.info(f"Contract DogAdoption deployed to {dog_adoption}")
    
    return dog_adoption


def start_adoption_campaign():
    account = deploying.get_account()
    
    dog_adoption = DogAdoption[-1]
    
    start_tx = dog_adoption.startAdoptionCampaign({"from": account})
    start_tx.wait(1)
    
    logging.info("Adoption campaign has started!")


def terminate_adoption_campaign():
    account = deploying.get_account()
    
    dog_adoption = DogAdoption[-1]
    
    terminate_tx = dog_adoption.terminateAdoptionCampaign({"from": account})
    terminate_tx.wait(1)
    
    logging.info("Adoption campaign has been terminated!")


def add_adopter(adopter_address, age: int, gender: str):
    account = deploying.get_account()
    
    dog_adoption = DogAdoption[-1]
    
    add_adopter_tx = dog_adoption.addAdopter(
                                    adopter_address, 
                                    age, 
                                    gender, 
                                    {"from": account}
                                )
    add_adopter_tx.wait(1)
    
    logging.info(f"A new adopter added with address {adopter_address}")
    
    return adopter_address


def add_pet(
    id: int, 
    name: str, 
    age: int, 
    gender: str, 
    race: str, 
    size: int
):
    account = deploying.get_account()
    
    dog_adoption = DogAdoption[-1]
    
    add_pet_tx = dog_adoption.addPet(
                                id, 
                                name, 
                                age, 
                                gender,
                                race,
                                size,
                                {"from": account}
                            )
    add_pet_tx.wait(1)
    
    pet = {
        "id": id, 
        "name": name, 
        "age": age, 
        "gender": gender,
        "race": race,
        "size": size,
    }
    
    logging.info(f"A new pet added: {pet}")
    
    return pet


def adopt_pet(id: int):
    account = deploying.get_account()
    
    dog_adoption = DogAdoption[-1]
    
    adopt_pet_tx = dog_adoption.adoptPet(id, {"from": account})
    adopt_pet_tx.wait(1)
    
    logging.info(f"The pet with the id:{id} has been adopted!:)")
    
    return id


def send_donation(value: float):
    account = deploying.get_account()
    
    dog_adoption = DogAdoption[-1]
    
    donation = dog_adoption.sendDonation({"from": account, "value": value})
    donation.wait(1)
    
    logging.info(f"{value} ETH just donated!:)")


def get_balance():
    account = deploying.get_account()
    
    dog_adoption = DogAdoption[-1]
    
    balance = dog_adoption.getBalance({"from": account})
    balance_to_wei = Web3.toWei(balance, 'ether')
    
    logging.info(f"The current balance of the shelter is {balance_to_wei} Wei.")
    
    return balance