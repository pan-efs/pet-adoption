// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "contracts/StructsEnumsAdoption.sol";

interface IPetAdoption {
    function addAdopter(address _addrAdopter, uint8 _age, string memory _gender)
        external
        returns (address);
    
    function addDog(Pet memory _dog, address _addrAdopter)
        external
        returns (bool, address);
    
    function adoptDog(address _addrAdopter, uint256 _dogId)
        external
        returns (address, uint256);
    
    function startAdoptionCampaign()
        external
        returns (bool);

    function terminateAdoptionCampaign()
        external
        returns (bool);

} 