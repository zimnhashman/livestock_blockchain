// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

contract DataStorage {
    struct SensorData {
        bytes32 dataHash;
        string geoHash;
        uint256 timestamp;
    }

    mapping(bytes32 => SensorData) private _data;
    mapping(address => bool) private _farmOwners;

    event DataSubmitted(bytes32 indexed dataId, address indexed owner);

    constructor() {
        _farmOwners[msg.sender] = true;
    }

    modifier onlyFarmOwner() {
        require(_farmOwners[msg.sender], "Not a farm owner");
        _;
    }

    function submitData(
        bytes32 dataId,
        bytes32 dataHash,
        string memory geoHash
    ) external onlyFarmOwner {
        _data[dataId] = SensorData(dataHash, geoHash, block.timestamp);
        emit DataSubmitted(dataId, msg.sender);
    }

    function getData(bytes32 dataId) external view returns (SensorData memory) {
        return _data[dataId];
    }
}