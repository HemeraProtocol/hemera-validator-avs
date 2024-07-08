#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import flask
from flask import Blueprint, jsonify, current_app
from flask_marshmallow import Marshmallow

from service.task import send_task, publish_json_to_ipfs
from service.hemera import get_transactions, get_token_holdings


# Initialize Marshmallow
ma = Marshmallow()

# Create the Blueprint
performer_bp = Blueprint('performer', __name__)


@performer_bp.route('/task/execute', methods=['POST'])
def perform():
    body = flask.request.json

    wallet_address = body.get("walletAddress")
    current_app.logger.info(f"Validating data for {wallet_address} on ethereum chain")

    task_definition_id = int(body.get("taskDefinitionId") or 0)
    if task_definition_id == 0:
        current_app.logger.info(f"Getting taskDefinitionId: {task_definition_id}, validate wallet transactions")
        data = get_transactions("ethereum", wallet_address)
    elif task_definition_id == 1:
        current_app.logger.info(f"Getting taskDefinitionId: {task_definition_id}, validate wallet token holdings")
        data = get_token_holdings("ethereum", wallet_address)
    else:
        return "Invalid defination", 400


    cid = publish_json_to_ipfs({ "chain_name": 'ethereum', "wallet_address": wallet_address, "data": json.dumps(data) })

    send_task(cid, json.dumps(data), task_definition_id)
    
    return jsonify({"proofOfTask": cid, "data": data, "taskDefinitionId": task_definition_id}), 200
