from flask import Blueprint, request, jsonify
from .schemas import ItemSchema, ItemUpdateSchema

from app import cache
from app import limiter

# Create the Blueprint
items_bp = Blueprint('items', __name__)

# In-memory storage for demo purposes
items = []

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)
item_update_schema = ItemUpdateSchema()


# Route to get all items (limited to 100 per day and 10 per hour)
@items_bp.route('/items', methods=['GET'])
@limiter.limit("100/day;10/hour")
@cache.cached(timeout=60)
def get_items():
    return items_schema.jsonify(items)

# Route to get a single item by id (limited to 100 per day and 10 per hour)
@items_bp.route('/items/<int:item_id>', methods=['GET'])
@limiter.limit("100/day;10/hour")
@cache.cached(timeout=60, key_prefix='item_')
def get_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    return item_schema.jsonify(item)

# Route to create a new item (limited to 10 per hour)
@items_bp.route('/items', methods=['POST'])
@limiter.limit("10/hour")
def create_item():
    data = request.get_json()
    item_data = item_schema.load(data)
    item_id = len(items) + 1
    new_item = {'id': item_id, **item_data}
    items.append(new_item)
    # Clear cache for 'get_items' after creating a new item
    cache.delete_memoized(get_items)
    return item_schema.jsonify(new_item), 201

# Route to update an existing item (limited to 10 per hour)
@items_bp.route('/items/<int:item_id>', methods=['PUT'])
@limiter.limit("10/hour")
def update_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404

    data = request.get_json()
    item_data = item_update_schema.load(data)
    item.update(item_data)
    # Clear cache for 'get_item' after updating the item
    cache.delete_memoized(get_item, item_id)
    return item_schema.jsonify(item)

# Route to delete an item (limited to 10 per hour)
@items_bp.route('/items/<int:item_id>', methods=['DELETE'])
@limiter.limit("10/hour")
def delete_item(item_id):
    global items
    items = [item for item in items if item['id'] != item_id]
    cache.delete_memoized(get_items)
    return '', 204