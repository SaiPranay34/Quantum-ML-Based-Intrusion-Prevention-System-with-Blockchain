// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Intrusion {
    struct Log {
        uint256 id;
        uint256 timestamp;
        string attackType;
        string dataHash;
        uint256 confidence;
        string ipAddress;
    }

    Log[] private logs;
    address public owner;

    event IntrusionLogged(uint256 indexed id, string attackType, uint256 confidence);

    constructor() {
        owner = msg.sender;
    }

    function logIntrusion(
        string memory _attackType,
        string memory _dataHash,
        uint256 _confidence,
        string memory _ipAddress
    ) public {
        uint256 newId = logs.length + 1;
        logs.push(Log(newId, block.timestamp, _attackType, _dataHash, _confidence, _ipAddress));
        emit IntrusionLogged(newId, _attackType, _confidence);
    }

    function getLog(uint256 index) public view returns (Log memory) {
        require(index < logs.length, "Index out of bounds");
        return logs[index];
    }

    function getLogsCount() public view returns (uint256) {
        return logs.length;
    }

    function getAllLogs() public view returns (Log[] memory) {
        return logs;
    }
}
