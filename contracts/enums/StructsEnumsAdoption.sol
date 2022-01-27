// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;


/**
 * @title Structs and Enums
 * @notice The file with the essential struct and enums
 */



/**
 * @notice Adopter Struct
 * @param addrAdopter The address of the candidate adopter
 * @param age The age of the candidate adopter
 * @param gender The gender of the candidate adopter
 * @param pet The pet which belongs to the adopter
 * @param hasAdopted If the adopter has adopted a dog
 * @param timeOfJoin The block.timestamp where the candidate adopter joined the system
 * @param timeOfAdoption The block.timestamp where the adopter adopted a dog
 */
struct Adopter {
    address addrAdopter;
    uint8 age;
    string gender;
    Pet pet;
    bool hasAdopted;
    uint256 timeOfJoined;
    uint256 timeOfAdoption;
}


/**
 * @notice Size Enum
 * @param Tiny Tiny size of pet (<= 4kg) 
 * @param Small Small size of pet (>4 && <=10 kg)
 * @param Medium Medium size of pet (>10 && <=30 kg)
 * @param Large Large size of pet (>30 kg)
 */
enum Size {
    Tiny,
    Small,
    Medium,
    Large
}


/**
 * @notice Dog Struct
 * @param id The id of the pet. Should be >0
 * @param name The name of the pet
 * @param age The age of the pet
 * @param gender The gender of the pet
 * @param race The race of the pet
 * @param size The size of the pet
 */
struct Pet {
    uint256 id;
    string name;
    uint8 age;
    string gender;
    string race;
    Size size;
}


/**
 * @notice The status of adoption process
 * @param TERMINATED The shelter is closed
 * @param IN_PROGRESS An adoption can take place normally 
 */
enum StatusAdoption {
    TERMINATED,
    IN_PROGRESS
}