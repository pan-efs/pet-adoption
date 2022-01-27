import os
import time
import pytest

from brownie import DogAdoption, network

from scripts.deploy_contracts_cls import Deploying
from scripts.deploy_dog_adoption import *

load_dotenv()


@pytest.fixture
def deploy():
    return Deploying()


def test_dog_adoption(deploy):
    deploying = deploy
    
    if network.show_active() in deploying.LOCAL:
        pytest.skip()
    
    account = deploying.get_account()
    
    # Deploy the contract
    dog_adoption = deploy_dog_adoption()
    # Assert is not None
    assert dog_adoption is not None
    
    # Start the adoption campaign
    DogAdoption[-1].startAdoptionCampaign({"from": account})
    time.sleep(20)
    # Assert that the campaign started
    assert DogAdoption[-1].statusOfAdoption() == 1
    
    # Add adopter (i.e. owner can be adopter as well, it's not given)
    adopter = os.getenv("PUBLIC_KEY")
    DogAdoption[-1].addAdopter(adopter, 25, "male", {"from": account})
    time.sleep(20)
    
    # Get balance of contract
    assert DogAdoption[-1].balance() == 0
    
    # Add pets
    DogAdoption[-1].addPet(5, "smurf", 2, "male", "pitbull", 2, {"from": account})
    time.sleep(20)
    DogAdoption[-1].addPet(6, "smurfaki", 3, "male", "pitbull", 2, {"from": account})
    
    # Adopt the pet with id=5
    DogAdoption[-1].adoptPet(5, {"from": account})
    time.sleep(20)
    
    # Assert that the dog with id=5 has been adopted, while the dog with id=6 has not
    assert DogAdoption[-1].hasBeenAdopted(5) == True
    assert DogAdoption[-1].hasBeenAdopted(6) == False
    
    # Donation
    DogAdoption[-1].sendDonation({"from": account, "value": 500000000000000})
    
    # Assert that the balance is > 0
    assert DogAdoption[-1].balance() > 0
    
    # Get the great benefactor
    assert DogAdoption[-1].benefactors(adopter, {"from": account}) > 0
    
    # Terminate the dog adoption campaign
    DogAdoption[-1].terminateAdoptionCampaign({"from": account})
    # Assert that the campaign terminated
    assert DogAdoption[-1].statusOfAdoption({"from": account}) == 0