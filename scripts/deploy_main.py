import os
from scripts.deploy_dog_adoption import *

load_dotenv()

def main():
    deploy_dog_adoption()
    start_adoption_campaign()
    add_adopter(os.getenv('PUBLIC_KEY'), 25, "male")
    send_donation(0.05)
    add_pet(5, "smurf", 2, "male", "pitbull", 2)
    adopt_pet(5)
    #get_balance()
    terminate_adoption_campaign()