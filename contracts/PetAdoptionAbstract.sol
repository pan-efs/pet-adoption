// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./StructsEnumsAdoption.sol";

abstract contract PetAdoptionAbstract {
    
    function addAdopter(
        address _addrAdopter,
        uint8 _age,
        string calldata _gender
    ) 
        external 
        virtual 
        returns (address);

    function addPet(
        uint256 _id,
        string calldata _name,
        uint8 _age,
        string calldata _gender,
        string calldata _race,
        Size _size
    )
        external
        virtual
        returns (bool, address);

    function adoptPet(uint256 _petId)
        external
        virtual
        returns (address, uint256);

    function startAdoptionCampaign() external virtual returns (bool);

    function terminateAdoptionCampaign() external virtual returns (bool);
}
