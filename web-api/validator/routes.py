#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import flask
from flask import Blueprint, jsonify, current_app
from flask_marshmallow import Marshmallow

from service.task import get_ipfs_task
from service.rpc import get_transaction_simple

# Initialize Marshmallow
ma = Marshmallow()

# Create the Blueprint
validator_bp = Blueprint('validator', __name__)


@validator_bp.route('/task/validate', methods=['POST'])
def validate():
    body = flask.request.json

    proof_of_task = body.get("proofOfTask")
    current_app.logger.info(f"Validate task: proof of task: {proof_of_task}")

    data = get_ipfs_task(proof_of_task)

    # Validate transaction
    is_approve = True
    for txn in json.loads(data["data"]):
        hash =  txn["transaction_hash"]
        current_app.logger.info(f"Validation txn {hash}")
        real_txn = get_transaction_simple(data["chain_name"], hash)

        if real_txn and real_txn["from"].lower() != txn["from_address"].lower() and real_txn["to"].lower() != txn["to_address"].lower():
            is_approve = False

    result = "Approve" if is_approve else "Not Approve"
    current_app.logger.info(f"Vote {result}")
    return jsonify({"data": result}), 200
