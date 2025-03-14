from flask import Blueprint, request, jsonify
import random
from heroes import heroes  # Import our in-memory heroes list

adventures_bp = Blueprint('adventures', __name__)

# Global in-memory list to store adventure logs
adventures = []

# Predefined challenges for our DevOps world
challenge_pool = [
    "Production outage at 3 AM",
    "CI/CD pipeline meltdown",
    "Server cluster rebellion",
    "Configuration drift crisis",
    "Unexpected container explosion",
    "Load balancer gone rogue",
    "Database replication hiccup",
    "DNS misconfiguration dilemma",
    "Secrets leak fiasco",
    "Cache invalidation nightmare",
    "Kubernetes podocalypse",
    "Microservices orchestration mayhem"
]


@adventures_bp.route('/', methods=['POST'])
def create_adventure():
    """
    Initiate a new adventure for a hero.
    
    Expected JSON payload:
    {
      "hero_id": 0,
      "challenge": "Optional custom challenge string"
    }
    
    If no challenge is provided, a random one is selected.
    The outcome is determined randomly to simulate the unpredictability of a DevOps incident.
    """
    data = request.get_json()
    if not data or 'hero_id' not in data:
        return jsonify({'error': 'Missing required field: hero_id'}), 400
    
    hero_id = data['hero_id']
    # Verify hero exists
    if hero_id < 0 or hero_id >= len(heroes):
        return jsonify({'error': 'Hero not found'}), 404
    
    challenge = data.get('challenge')
    if not challenge:
        challenge = random.choice(challenge_pool)
        
    # Determine outcome based on a random chance
    outcome_roll = random.randint(1, 100)
    
    if outcome_roll > 70:
        result = "Victory! The hero fixed the issue with epic automation flair."
        exp_gain = random.randint(10, 20)
    elif outcome_roll > 30:
        result = "Draw. The crisis was averted… just barely."
        exp_gain = random.randint(5, 10)
    else:
        result = "Defeat! The hero's code integrity was compromised by chaos."
        exp_gain = 0
    
    adventure_record = {
        "id": len(adventures),
        "hero_id": hero_id,
        "challenge": challenge,
        "result": result,
        "experience_gain": exp_gain
    }
    adventures.append(adventure_record)
    
    # Update the hero's experience if necessary
    if exp_gain > 0:
        heroes[hero_id]['experience'] += exp_gain
    
    return jsonify(adventure_record), 201

@adventures_bp.route('/<int:adventure_id>', methods=['GET'])
def get_adventure(adventure_id):
    """
    Retrieve details of a specific adventure by its ID.
    """
    if adventure_id < 0 or adventure_id >= len(adventures):
        return jsonify({'error': 'Adventure not found'}), 404
    return jsonify(adventures[adventure_id])

@adventures_bp.route('/history', methods=['GET'])
def get_adventure_history():
    """
    Retrieve a history of all adventures.
    """
    return jsonify(adventures)
