## Pet Adoption Smart Contract :unicorn:

[![AUR maintainer](https://img.shields.io/badge/Houba-Hej%2C%20Folks!-brightgreen)]()
[![Python 3.9](https://img.shields.io/badge/python-3.9.6-blue)](https://www.python.org/downloads/release/python-390/)

:warning: Do not use the smart contracts in production. Watch out with your wallet's keys. See it as an example!

### Installation
- [Install brownie](https://eth-brownie.readthedocs.io/en/stable/install.html)
- [Install ganache-cli](https://www.npmjs.com/package/ganache-cli)

Clone the repo if you would like to experiment with it:
- `git clone https://github.com/pan-efs/pet-adoption`

### Create .env file
```diff
+ export PRIVATE_KEY = <YOUR_PRIVATE_KEY>
+ export PUBLIC_KEY = <YOUR_PUBLIC_KEY>
+ export WEB3_INFURA_PROJECT_ID = <YOUR_PROJECT_ID>
+ export ETHERSCAN_TOKEN = <YOUR_ETHERSCAN_TOKEN>
```

It is not necessary to use all aforementioned keys in order to run the repo.

### Deployment
Deploy: `brownie run scripts\deploy_main.py --network rinkeby`

### Etherscan Rinkeby
See all your Txn Hash at: `https://rinkeby.etherscan.io/address/{your_account_address}`.

More details can been found there.

### Run tests
Local: `brownie test`

Testnet (rinkeby): `brownie test --network rinkeby`