from scripts.deploy_contracts_cls import Deploying

def main():
    deploying = Deploying()
    
    deploying.deploy_mocks(
        deploying.DECIMALS, 
        deploying.INITIAL_VALUE
    )