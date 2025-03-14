from flask import Blueprint, request, jsonify

heroes_bp = Blueprint('heroes', __name__)

# Global in-memory list to store heroes
heroes = []

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
    
    new_hero = {
        "id": len(heroes),
        "name": data['name'],
        "role": data['role'],
        "health": 100,            # Represents resilience
        "automation": 50,         # Level of automation skills
        "experience": 0,          # Starting experience
        "integrity": 50           # Adherence to best practices (code integrity)
    }
    heroes.append(new_hero)
    return jsonify(new_hero), 201

@heroes_bp.route('/<int:hero_id>', methods=['GET'])
def get_hero(hero_id):
    """
    Retrieve details about a specific hero by ID.
    """
    if hero_id < 0 or hero_id >= len(heroes):
        return jsonify({'error': 'Hero not found'}), 404
    
    return jsonify(heroes[hero_id])

@heroes_bp.route('/<int:hero_id>', methods=['PUT'])
def update_hero(hero_id):
    """
    Update a hero's attributes.
    
    Expected JSON payload can include any of the attributes (e.g., health, experience).
    This endpoint is used to reflect progress and improvements after an adventure.
    """
    if hero_id < 0 or hero_id >= len(heroes):
        return jsonify({'error': 'Hero not found'}), 404

    data = request.get_json()
    hero = heroes[hero_id]
    
    # Update only provided fields: health, automation, experience, integrity.
    for key in ['health', 'automation', 'experience', 'integrity']:
        if key in data:
            hero[key] = data[key]
    
    return jsonify(hero)

@heroes_bp.route('/<int:hero_id>', methods=['DELETE'])
def delete_hero(hero_id):
    """
    Delete a specific hero by its ID.
    """
    if hero_id < 0 or hero_id >= len(heroes):
        return jsonify({'error': 'Hero not found'}), 404

    deleted_hero = heroes.pop(hero_id)
    # Optionally, reassign IDs to maintain consistency
    for idx, hero in enumerate(heroes):
        hero['id'] = idx

    return jsonify({'message': 'Hero deleted successfully', 'hero': deleted_hero})

