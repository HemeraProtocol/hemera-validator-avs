#!/usr/bin/python3
# -*- coding: utf-8 -*-

from decimal import Decimal

from web3 import Web3
from web3.middleware import geth_poa_middleware


DEFAULT_RPC_ENDPOINTS = {
    "ethereum": "https://ethereum.blockpi.network/v1/rpc/ea36a8b8cd12b8a865024b7d0e51a092cff58d25",
}


ERC20ABI = """
  [{
    "inputs": [{"internalType": "address", "name": "owner", "type": "address"}],
    "name": "balanceOf",
    "outputs": [{"internalType": "uint256", "name": "balance", "type": "uint256"}],
    "stateMutability": "view",
    "type": "function"
  }]
"""


def get_balance_by_chain(chain_name, wallet_address) -> Decimal:
    web3 = Web3(Web3.HTTPProvider(DEFAULT_RPC_ENDPOINTS[chain_name]))
    try:
        if not web3.is_address(wallet_address):
            return Decimal(0)
        wallet_address = web3.to_checksum_address(wallet_address)
        balance = web3.eth.get_balance(wallet_address)
        return Decimal(balance)
    except Exception as e:
        return Decimal(0)


def get_erc20_balance_of(chain_name, token_address, wallet_address) -> Decimal:
    web3 = Web3(Web3.HTTPProvider(DEFAULT_RPC_ENDPOINTS[chain_name]))
    contract = web3.eth.contract(
        address=Web3.to_checksum_address(token_address.lower()),
        abi=ERC20ABI,
    )
    balance = contract.functions.balanceOf(Web3.to_checksum_address(wallet_address.lower())).call()
    return balance


def get_transaction_simple(chain_name, hash):
    try:
        web3 = Web3(Web3.HTTPProvider(DEFAULT_RPC_ENDPOINTS[chain_name]))

        # Get Transaction
        transaction = web3.eth.get_transaction(hash)

        return transaction
    except Exception as e:
        print(e)
        return None
    


def get_transaction_data(chain_name, hash):
    try:
        web3 = Web3(Web3.HTTPProvider(DEFAULT_RPC_ENDPOINTS[chain_name]))
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        # Get Transaction
        transaction = web3.eth.get_transaction(hash)
        full_transaction = web3.eth.get_transaction_receipt(hash)

        # Get block
        block_number = full_transaction.blockNumber
        block = web3.eth.get_block(block_number)

        return transaction, block
    except Exception as e:
        print(e)
        return None


def get_transaction_logs(chain_name, hash):
    try:
        web3 = Web3(Web3.HTTPProvider(DEFAULT_RPC_ENDPOINTS[chain_name]))
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        # Get Transaction
        full_transaction = web3.eth.get_transaction_receipt(hash)

        return full_transaction["logs"]
    except Exception as e:
        print(e)
        return []
