
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from flask import Flask, jsonify
from validator.routes import validator_bp, ma as validator_ma
from performer.routes import performer_bp, ma as performer_ma
from marshmallow import ValidationError
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Initialize Marshmallow with the app
validator_ma.init_app(app)
performer_ma.init_app(app)

# Register Blueprints
app.register_blueprint(validator_bp)
app.register_blueprint(performer_bp)

# Configure rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per minute", "10 per second"],
)

# Configure Flask-Caching with Redis
cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    # 'CACHE_REDIS_URL': 'redis://localhost:6379/0',  # Replace with your Redis URL
    'CACHE_DEFAULT_TIMEOUT': 300  # Cache timeout in seconds (5 minutes)
})

# Global error handler for ValidationError
@app.errorhandler(ValidationError)
def handle_validation_error(error):
    response = jsonify({'error': 'Validation Error', 'messages': error.messages})
    response.status_code = 400
    return response

# Global error handler for 404 Not Found
@app.errorhandler(404)
def handle_404_error(error):
    response = jsonify({'error': 'Not Found'})
    response.status_code = 404
    return response

# Global error handler for 500 Internal Server Error
@app.errorhandler(500)
def handle_500_error(error):
    response = jsonify({'error': 'Internal Server Error'})
    response.status_code = 500
    return response

# Global error handler for all other exceptions
@app.errorhandler(Exception)
def handle_exception_error(error):
    response = jsonify({'error': 'An unexpected error occurred'})
    response.status_code = 500
    return response

if __name__ == '__main__':
    app.run("0.0.0.0", port=4002, debug=True)