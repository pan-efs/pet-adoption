import pytest

from brownie import network

from scripts.deploy_contracts_cls import Deploying
from scripts.deploy_dog_adoption import *


@pytest.fixture
def deploy():
    return Deploying()

@pytest.fixture
def not_local():
    if network.show_active() not in deploying.LOCAL:
        pytest.skip()


def test_deploy_dog_adoption(not_local):
    not_local
    
    dog_adoption = deploy_dog_adoption()
    
    assert dog_adoption is not None


def test_start_adoption_campaign(deploy, not_local):
    deploying = deploy
    not_local
    
    account = deploying.get_account()
    dog_adoption = deploy_dog_adoption()
    
    # start
    dog_adoption.startAdoptionCampaign({"from": account})
    
    assert dog_adoption.statusOfAdoption() == 1


def test_terminate_adoption_campaign(deploy, not_local):
    deploying = deploy
    not_local
    
    account = deploying.get_account()
    dog_adoption = deploy_dog_adoption()
    
    dog_adoption.startAdoptionCampaign({"from": account})
    # termination
    dog_adoption.terminateAdoptionCampaign({"from": account})
    
    assert dog_adoption.statusOfAdoption() == 0


def test_add_adopter(deploy, not_local):
    deploying = deploy
    not_local
    
    account = deploying.get_account()
    dog_adoption = deploy_dog_adoption()
    
    # start
    dog_adoption.startAdoptionCampaign({"from": account})
    
    assert dog_adoption.statusOfAdoption() == 1
    
    adopter = deploying.get_account(index=1)
    dog_adoption.addAdopter(adopter, 25, "male", {"from": account})
    
    assert dog_adoption.isAdopter(adopter)
    assert not dog_adoption.isAdopter(dog_adoption.owner())


def test_add_pet(deploy, not_local):
    deploying = deploy
    not_local
    
    account = deploying.get_account()
    dog_adoption = deploy_dog_adoption()
    
    dog_adoption.startAdoptionCampaign({"from": account})
    assert dog_adoption.statusOfAdoption() == 1
    
    # add as adopter
    adopter = deploying.get_account(index=5)
    dog_adoption.addAdopter(adopter, 25, "male", {"from": account})
    dog_adoption.addPet(5, "smurf", 2, "male", "pitbull", 2, {"from": adopter})
    dog_adoption.addPet(6, "smurfaki", 3, "male", "pitbull", 2, {"from": adopter})
    
    # exist
    assert dog_adoption.dogs(5) == (5, 'smurf', 2, 'male', 'pitbull', 2)
    assert dog_adoption.dogs(6) == (6, 'smurfaki', 3, 'male', 'pitbull', 2)
    # doesn't exist
    assert dog_adoption.dogs(3) == (0, '', 0, '', '', 0)


def test_adopt_pet(deploy, not_local):
    deploying = deploy
    not_local
    
    account = deploying.get_account()
    dog_adoption = deploy_dog_adoption()
    
    dog_adoption.startAdoptionCampaign({"from": account})
    assert dog_adoption.statusOfAdoption() == 1
    
    adopter = deploying.get_account(index=5)
    dog_adoption.addAdopter(adopter, 25, "male", {"from": account})
    dog_adoption.addPet(5, "smurf", 2, "male", "pitbull", 2, {"from": adopter})
    
    assert dog_adoption.dogs(5) == (5, 'smurf', 2, 'male', 'pitbull', 2)
    
    dog_adoption.adoptPet(5, {"from": adopter})
    # id=5 has been adopted
    assert dog_adoption.hasBeenAdopted(5) == True


def test_send_donation(deploy, not_local):
    deploying = deploy
    not_local
    
    account = deploying.get_account()
    dog_adoption = deploy_dog_adoption()
    
    dog_adoption.startAdoptionCampaign({"from": account})
    assert dog_adoption.statusOfAdoption() == 1
    
    adopter = deploying.get_account(index=5)
    dog_adoption.addAdopter(adopter, 25, "male", {"from": account})
    assert dog_adoption.isAdopter(adopter)
    
    assert dog_adoption.balance() == 0
    dog_adoption.sendDonation({"from": adopter, "value": 500000000})
    assert dog_adoption.balance() > 0
    
    # donation has been added to correspond account
    assert dog_adoption.benefactors(adopter) > 0


def test_change_owner(deploy, not_local):
    deploying = deploy
    not_local
    
    account = deploying.get_account()
    dog_adoption = deploy_dog_adoption()
    
    dog_adoption.startAdoptionCampaign({"from": account})
    assert dog_adoption.statusOfAdoption() == 1
    
    # pre
    assert dog_adoption.owner() == account
    
    new_owner = deploying.get_account(index=3)
    dog_adoption.changeOwner(new_owner)
    # after
    assert dog_adoption.owner() == new_owner


def test_withdraw(deploy, not_local):
    deploying = deploy
    not_local
    
    account = deploying.get_account()
    dog_adoption = deploy_dog_adoption()
    
    dog_adoption.startAdoptionCampaign({"from": account})
    assert dog_adoption.statusOfAdoption() == 1
    
    adopter = deploying.get_account(index=5)
    dog_adoption.addAdopter(adopter, 25, "male", {"from": account})
    assert dog_adoption.isAdopter(adopter)
    
    assert dog_adoption.balance() == 0
    dog_adoption.sendDonation({"from": adopter, "value": 500000000})
    assert dog_adoption.balance() > 0
    
    current_balance = account.balance()
    dog_adoption.withdraw()
    
    assert account.balance() > current_balance