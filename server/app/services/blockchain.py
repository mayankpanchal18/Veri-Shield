from __future__ import annotations

import json
from pathlib import Path
from web3 import Web3

from ..core.config import settings

ABI = [
    {
        "inputs": [
            {"internalType": "bytes32", "name": "documentHash", "type": "bytes32"},
            {"internalType": "string", "name": "status", "type": "string"},
            {"internalType": "bytes32", "name": "eventHash", "type": "bytes32"},
        ],
        "name": "recordVerification",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    }
]


def anchor_verification(document_hash: str, status: str, event_hash: str) -> str | None:
    if not settings.blockchain_enabled:
        return None
    if not settings.blockchain_contract_address or not settings.blockchain_private_key:
        raise RuntimeError("Blockchain is enabled but contract address/private key is missing")

    w3 = Web3(Web3.HTTPProvider(settings.blockchain_rpc_url))
    if not w3.is_connected():
        raise RuntimeError("Could not connect to BLOCKCHAIN_RPC_URL")
    account = w3.eth.account.from_key(settings.blockchain_private_key)
    contract = w3.eth.contract(address=Web3.to_checksum_address(settings.blockchain_contract_address), abi=ABI)
    nonce = w3.eth.get_transaction_count(account.address)
    tx = contract.functions.recordVerification(
        bytes.fromhex(document_hash), status, bytes.fromhex(event_hash)
    ).build_transaction({
        "from": account.address,
        "nonce": nonce,
        "gas": 250000,
        "gasPrice": w3.eth.gas_price,
        "chainId": w3.eth.chain_id,
    })
    signed = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    return tx_hash.hex()
