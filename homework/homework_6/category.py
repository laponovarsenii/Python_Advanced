from flask import Blueprint, request, jsonify, abort
from models.category import Category
from core.db import db

bp = Blueprint('categories', __name__, url_prefix='/categories')

@bp.route('/', methods=['POST'])
def create_category():
    data = request.json
    name = data.get('name')
    if not name:
        abort(400, 'No category name provided')
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return jsonify({'id': category.id, 'name': category.name}), 201

@bp.route('/', methods=['GET'])
def list_categories():
    categories = Category.query.all()
    result = [{'id': c.id, 'name': c.name} for c in categories]
    return jsonify(result)

@bp.route('/<int:id>', methods=['PUT'])
def update_category(id):
    category = Category.query.get_or_404(id)
    data = request.json or {}
    name = data.get('name')
    if not name:
        abort(400, 'No category name provided')
    category.name = name
    db.session.commit()
    return jsonify({'id': category.id, 'name': category.name})

@bp.route('/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'ok': True})