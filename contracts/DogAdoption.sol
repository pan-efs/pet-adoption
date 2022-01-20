// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

import "./FundETHUSD.sol";
import "./PetAdoptionAbstract.sol";


/**
 * @title DogAdoption smart contract related to dog shelter.
 * @notice The PetAdoption abstract contract gives you the opportunity to join the adoption list of a dog shelter and
 *         to gain the privilige adopting and adding dogs.
 *         FundETHUSD contract is used in order to inherent useful funding functions.
 */
contract DogAdoption is PetAdoptionAbstract, FundETHUSD, Ownable {
    
    // Global variables
    address payable ownerOfDogShelter;
    StatusAdoption public statusOfAdoption;
    bool public lockedSendDonation;
    AggregatorV3Interface internal ethUsdPriceFeed;

    mapping(uint256 => Pet) public dogs;
    mapping(uint256 => bool) public hasBeenAdopted;
    mapping(address => Adopter) private mapAdopters;
    mapping(address => bool) public isAdopter;
    address[] public greatBenefactors;
    
    
    // Events
    event AddedDog(Pet dog, string message);
    event AddedAdopter(address indexed addrAdopter, Adopter adopter, string message);
    event DogAdopted(address indexed addrAdopter, Pet dog, string message);
    event Donation(address indexed addrAdopter, uint256 amount);
    event Started(uint256 startedTime, string message);
    event Terminated(uint256 terminatedTime, string message);

    // Errors
    error BenefactorsException(string message);
    

    /**
     * @notice The constructor of the smart contract
     * @param _priceFeedAddress Chainlink ETH/USD contract address on the corresponding network
     */
    constructor(
        address _priceFeedAddress
    )
    public
    FundETHUSD(_priceFeedAddress)
    {
        ownerOfDogShelter = payable(msg.sender);
        statusOfAdoption = StatusAdoption.TERMINATED;
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
    }
    

    // The contract can receive payments
    receive() external payable {}
    

    /**
     * @notice Adoption campaign should be in progress
     */
    modifier inProgress()
        {
            require(statusOfAdoption == StatusAdoption.IN_PROGRESS, "Campaign is not in progress anymore.");
            _;
        }

    
    /**
     * @notice Add an adopter in the dog shelter list
     * @param _addrAdopter Candidate's account address on the corresponding network
     * @param _age Age of the candidate adopter
     * @param _gender Gender of the candidate adopter
     * @dev Emits AddedAdopter event
     */
    function addAdopter(address _addrAdopter, uint8 _age, string calldata _gender)
        external
        override
        onlyOwner
        inProgress
        returns (address)
        {
            require(!isAdopter[_addrAdopter], "The adopter already exists.");
            require(_age >= 18, "The candidate adopter must be over 18 years old.");

            Adopter memory adopter;
            Pet memory _dog;
            adopter.addrAdopter = _addrAdopter;
            adopter.age = _age;
            adopter.gender = _gender;
            adopter.pet = _dog;
            adopter.hasAdopted = false;
            adopter.timeOfJoined = block.timestamp;
            adopter.timeOfAdoption = 0;
            mapAdopters[_addrAdopter] = adopter;

            emit AddedAdopter(_addrAdopter, adopter, "Welcome to the new adopter!:)");

            isAdopter[_addrAdopter] = true;

            return _addrAdopter;
        }
    
    
    /**
     * @notice Modifier for only adopters privilige
     * @dev Requires an adopter to be in the list
     */
    modifier onlyAdopter()
        {
            require(isAdopter[msg.sender] == true, "Only adopters have access in the system.");
            _;
        }
    
    
    /**
     * @param _dogId Dog's id
     * @param _name Dog's name
     * @param _age Dog's age
     * @param _gender Dog's gender
     * @param _race Dog's race
     * @param _size Dog's size
     * @dev onlyOwner and onlyAdopter can call this function
     * @dev Emits AddedDog event
     * @dev Default values of mapping 'dogs' are 0, so we do not accept 0 as _dog.id
     */
    function addPet(
            uint256 _dogId,
            string calldata _name,
            uint8 _age,
            string calldata _gender,
            string calldata _race,
            Size _size
        )
        external
        override
        onlyOwner 
        onlyAdopter
        inProgress
        returns (bool, address)
        {
            require(!hasBeenAdopted[_dogId], "Cannot add this dog because it has been adopted in the past.");
            require(_dogId > 0, "Dog's id should not be zero.");

            Pet memory _dog;

            _dog.id = _dogId;
            _dog.name = _name;
            _dog.age = _age;
            _dog.gender = _gender;
            _dog.size = _size;

            dogs[_dogId] = _dog;
            
            emit AddedDog(_dog, "Dog has been added! :)");

            return (true, msg.sender);
        }
    

    /**
     * @notice Adopt a dog
     * @param _dogId Dog's id
     */
    function adoptPet(uint256 _dogId)
        external
        override
        onlyAdopter
        inProgress
        returns (address, uint256)
        {   
            require(_dogId > 0, "There is no dog with this id.");
            require(!hasBeenAdopted[_dogId], "This dog is already adopted!");

            mapAdopters[msg.sender].pet = dogs[_dogId];
            hasBeenAdopted[_dogId] = true;
            
            return (msg.sender, _dogId);
        }
    
    
    /**
     * @notice Prevents sendDonation to be called while it is executing.
     * @dev Reentrancy guard prevention
     */
    modifier onlySend()
        {
            require(!lockedSendDonation, "Can't donate now!");
            lockedSendDonation = true;
            _;
            lockedSendDonation = false;
        }

    
    /**
     * @notice Donate to this contract
     * @dev onlyAdopter can call this function
     * @dev Emits Donation event
     */
    function sendDonation()
        public
        payable
        onlyAdopter
        onlySend
        {
            uint256 ethToUsd = getConversionRate(msg.value);

            if (ethToUsd > 100){
                greatBenefactors.push(msg.sender);
            }

            emit Donation(msg.sender, ethToUsd);
        }
    
    
    /**
     * @dev Return the current balance of this contract
     */
    function getBalance()
        public 
        view 
        returns(uint) 
        {
            return address(this).balance;
        }
    
    
    /**
     * @notice Start the adoption campaign
     * @dev Emits Started event
     */
    function startAdoptionCampaign()
        external
        override
        onlyOwner
        returns (bool)
        {
            require(statusOfAdoption == StatusAdoption.TERMINATED);
            statusOfAdoption = StatusAdoption.IN_PROGRESS;
            uint256 startedTime = block.timestamp;

            emit Started(startedTime, "Adoption campaign has started!");

            return true;
        }

    /**
     * @notice Terminate the adoption campaign
     * @dev Emits Terminated event
     */
    function terminateAdoptionCampaign()
        external
        override
        onlyOwner
        inProgress
        returns (bool)
        {
            statusOfAdoption = StatusAdoption.TERMINATED;
            uint256 terminatedTime = block.timestamp;
            emit Terminated(terminatedTime, "Adoption campaign is terminated.");

            return true;
        }
    

    /**
     * @notice Check if an address is valid
     * @param _addr The desired address
     */
    modifier validAddress(address _addr)
        {
            require(_addr != address(0), "Not valid address");
            _;
        }
    
    
    /**
     * @notice Change the owner of the contract
     * @param _newOwner The address of the new owner
     */
    function changeOwner(address payable _newOwner)
        internal 
        onlyOwner 
        validAddress(_newOwner) 
        {
            ownerOfDogShelter = _newOwner;
        }
    
    
    /**
     * @notice Withdraw the balance of this contract
     * @dev Only owner can call this function
     */
    function withdraw()
        public
        payable
        onlyOwner
        {
            ownerOfDogShelter.transfer(address(this).balance);
        }

}