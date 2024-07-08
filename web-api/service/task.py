#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json

import requests

from web3 import Web3
from eth_account import Account
from eth_abi import encode


ipfs_host =  os.getenv('IPFS_HOST')
pinata_api_key = os.getenv('PINATA_API_KEY')
pinata_secret_api_key = os.getenv('PINATA_SECRET_API_KEY')
rpc_base_address = os.getenv('OTHENTIC_CLIENT_RPC_ADDRESS')
private_key = os.getenv('PRIVATE_KEY')


def send_task(proof_of_task, data, task_definition_id):
    # Initialize Web3
    web3 = Web3(Web3.HTTPProvider(rpc_base_address))

    # Create a wallet from the private key
    account = Account.from_key(private_key) 
    performer_address = account.address

    # Convert data to hex and create the message
    message = encode(["string", "bytes", "address", "uint16"], [proof_of_task, data.encode('utf-8'), performer_address, task_definition_id])
    message_hash = web3.keccak(message)

    # Sign the message
    signed_message = Account.signHash(message_hash, private_key=private_key)
    signature = signed_message.signature.hex()
    
    # Create the JSON-RPC request body
    json_rpc_body = {
        "jsonrpc": "2.0",
        "method": "sendTask",
        "params": [
            proof_of_task,
            web3.to_hex(text=data),
            task_definition_id,
            performer_address,
            signature,
        ],
        "id": 1
    }

    # Send the request
    try:
        response = web3.manager.request_blocking(json_rpc_body["method"], json_rpc_body["params"])
        print("API response:", response)
    except Exception as error:
        print("Error making API request:", error)


def publish_json_to_ipfs(data):
    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    headers = {
        "Content-Type": "application/json",
        "pinata_api_key": pinata_api_key,
        "pinata_secret_api_key": pinata_secret_api_key
    }
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        response.raise_for_status()
        response_data = response.json()
        proof_of_task = response_data['IpfsHash']
        return proof_of_task
    except requests.exceptions.RequestException as error:
        print(f'Error making API request to Pinata: {error}')
        return None


def get_ipfs_task(cid):
    try:
        response = requests.get(f'{ipfs_host}{cid}')
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f'Error fetching IPFS data: {e}')
        return None

