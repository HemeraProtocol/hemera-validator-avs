#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests

HEMERA_API_HOST = 'https://api.w3w.ai/v1/socialscan/wallet/'

def get_transactions(chain_name, wallet_address):
    response = requests.get(f"{HEMERA_API_HOST}{wallet_address}/transactions?chain={chain_name}")
    if response.status_code == 200:
        return response.json()["transactions"]
    return None
    

def get_token_holdings(chain_name, wallet_address):
    response = requests.get(f"{HEMERA_API_HOST}{wallet_address}/token_holdings?chain={chain_name}")
    if response.status_code == 200:
        return response.json()["holdings"]
    return None