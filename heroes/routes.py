from flask import Blueprint, request, jsonify
from heroes.models import Hero
from extensions import db 

heroes_bp = Blueprint('heroes', __name__)

@heroes_bp.route('/', methods=['POST'])
def create_hero():
    """
    Create a new DevOps hero.
    
    Expected JSON payload:
    {
      "name": "MariferVL",
      "role": "DevOps Engineer"
    }
    
    Returns the created hero with initial attributes.
    """
    data = request.get_json()
    if not data or 'name' not in data or 'role' not in data:
        return jsonify({'error': 'Missing required fields: name and role'}), 400
    
    new_hero = Hero(
        name=data['name'],
        role=data['role'],
        health=100,  # Valor inicial
        automation=50,  # Valor inicial
        experience=0,  # Valor inicial
        integrity=50  # Valor inicial
    )
    
    db.session.add(new_hero)
    db.session.commit()
    
    return jsonify(new_hero.to_dict()), 201

@heroes_bp.route('/<int:hero_id>', methods=['GET'])
def get_hero(hero_id):
    """
    Retrieve details about a specific hero by ID.
    """
    hero = Hero.query.get(hero_id)
    if not hero:
        return jsonify({'error': 'Hero not found'}), 404
    
    return jsonify(hero.to_dict())

@heroes_bp.route('/<int:hero_id>', methods=['PUT'])
def update_hero(hero_id):
    """
    Update a hero's attributes.
    
    Expected JSON payload can include any of the attributes (e.g., health, experience).
    This endpoint is used to reflect progress and improvements after an adventure.
    """
    hero = Hero.query.get(hero_id)
    if not hero:
        return jsonify({'error': 'Hero not found'}), 404

    data = request.get_json()
    
    if 'health' in data:
        hero.health = data['health']
    if 'automation' in data:
        hero.automation = data['automation']
    if 'experience' in data:
        hero.experience = data['experience']
    if 'integrity' in data:
        hero.integrity = data['integrity']

    db.session.commit()
    
    return jsonify(hero.to_dict())

@heroes_bp.route('/<int:hero_id>', methods=['DELETE'])
def delete_hero(hero_id):
    """
    Delete a specific hero by its ID.
    """
    hero = Hero.query.get(hero_id)
    if not hero:
        return jsonify({'error': 'Hero not found'}), 404
    
    db.session.delete(hero)
    db.session.commit()
    
    return jsonify({'message': 'Hero deleted successfully', 'hero': hero.to_dict()})
