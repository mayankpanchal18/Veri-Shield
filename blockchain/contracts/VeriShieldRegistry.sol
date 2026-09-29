// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

/// @title VeriShield Registry
/// @notice Stores only document hashes, review status and revision event hashes. No identity evidence or PII is stored on-chain.
contract VeriShieldRegistry {
    address public owner;

    struct Record {
        string status;
        bytes32 latestEventHash;
        uint64 revision;
        uint64 updatedAt;
    }

    mapping(bytes32 => Record) public records;

    event VerificationRecorded(
        bytes32 indexed documentHash,
        string status,
        bytes32 indexed eventHash,
        uint64 revision,
        uint64 updatedAt
    );

    modifier onlyOwner() {
        require(msg.sender == owner, "owner only");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function recordVerification(bytes32 documentHash, string calldata status, bytes32 eventHash) external onlyOwner {
        Record storage item = records[documentHash];
        item.status = status;
        item.latestEventHash = eventHash;
        item.revision += 1;
        item.updatedAt = uint64(block.timestamp);
        emit VerificationRecorded(documentHash, status, eventHash, item.revision, item.updatedAt);
    }
}
