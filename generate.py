"""
Pokemon Greeting Generator

This script generates a random Pokemon greeting and updates the README.md file.
It fetches Pokemon data from the PokeAPI and creates a beautiful greeting card.
"""

import json
import random
import logging
from typing import Dict, List, Optional
from datetime import datetime

import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/pokemon"
MAX_POKEMON_ID = 1025
README_FILE = "./README.md"
HISTORY_FILE = "./pokemon_history.json"

# Greeting templates
GREETING_TEMPLATES = [
    "You have been greeted by <strong>{name}</strong>",
    "A wild <strong>{name}</strong> appeared to greet you!",
    "<strong>{name}</strong> wants to brighten your day!",
    "Say hello to <strong>{name}</strong>!",
    "<strong>{name}</strong> is here to wish you well!",
    "Greetings from <strong>{name}</strong>!",
    "<strong>{name}</strong> sends you positive vibes!",
]

CLOSING_MESSAGES = [
    "Have a wonderful day!",
    "May your day be filled with joy!",
    "Wishing you happiness and success!",
    "Hope you have an amazing day ahead!",
    "Sending you good vibes!",
    "Have a fantastic day!",
    "May your journey be legendary!",
]

def load_history() -> List[Dict]:
    """Load Pokemon history from file."""
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_history(history: List[Dict]) -> None:
    """Save Pokemon history to file."""
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Failed to save history: {e}")

def fetch_pokemon_data(pokemon_id: int) -> Optional[Dict]:
    """
    Fetch Pokemon data from PokeAPI.
    
    Args:
        pokemon_id: The ID of the Pokemon to fetch
        
    Returns:
        Dictionary containing Pokemon data or None if failed
    """
    try:
        url = f"{POKEAPI_BASE_URL}/{pokemon_id}"
        logger.info(f"Fetching Pokemon data for ID: {pokemon_id}")
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch Pokemon data: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Pokemon data: {e}")
        return None

def get_pokemon_sprite(pokemon_data: Dict) -> str:
    """
    Get the best available sprite for the Pokemon.
    
    Args:
        pokemon_data: Pokemon data from API
        
    Returns:
        URL of the sprite image
    """
    sprites = pokemon_data.get('sprites', {})
    
    # Try different sprite options in order of preference
    sprite_options = [
        sprites.get('front_default'),
        sprites.get('front_shiny'),
        sprites.get('other', {}).get('official-artwork', {}).get('front_default'),
        sprites.get('other', {}).get('home', {}).get('front_default'),
    ]
    
    for sprite in sprite_options:
        if sprite:
            return sprite
    
    # Fallback to a default Pokemon image
    return "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png"

def get_pokemon_info(pokemon_data: Dict) -> Dict[str, str]:
    """
    Extract relevant Pokemon information.
    
    Args:
        pokemon_data: Pokemon data from API
        
    Returns:
        Dictionary with Pokemon information
    """
    types = [t['type']['name'].title() for t in pokemon_data.get('types', [])]
    
    return {
        'name': pokemon_data['name'].title(),
        'id': pokemon_data['id'],
        'types': ' / '.join(types),
        'height': f"{pokemon_data.get('height', 0) / 10:.1f} m",
        'weight': f"{pokemon_data.get('weight', 0) / 10:.1f} kg",
    }

def generate_readme_content(pokemon_data: Dict, sprite_url: str, pokemon_info: Dict) -> str:
    """
    Generate the README.md content.
    
    Args:
        pokemon_data: Raw Pokemon data
        sprite_url: URL of the Pokemon sprite
        pokemon_info: Processed Pokemon information
        
    Returns:
        Formatted README content
    """
    greeting = random.choice(GREETING_TEMPLATES).format(name=pokemon_info['name'])
    closing = random.choice(CLOSING_MESSAGES)
    
    content = f'''<div align="center">
    <img src="{sprite_url}" width="200" height="200" alt="{pokemon_info['name']}">
    
    <h1>{greeting}</h1>
    
    <p>
        <strong>#{pokemon_info['id']:03d}</strong> • 
        <strong>Type:</strong> {pokemon_info['types']} • 
        <strong>Height:</strong> {pokemon_info['height']} • 
        <strong>Weight:</strong> {pokemon_info['weight']}
    </p>
    
    <h2>✨ {closing} ✨</h2>
    
    <p><em>Last updated: {datetime.now().strftime("%B %d, %Y at %H:%M UTC")}</em></p>
</div>

---

<div align="center">
    <p>🌟 <strong>This README is automatically updated every 24 hours with a new Pokémon greeting!</strong> 🌟</p>
    <p>Powered by <a href="https://pokeapi.co/">PokéAPI</a> | Made with ❤️ by <a href="https://github.com/isyuricunha">@isyuricunha</a></p>
</div>
'''
    
    return content

def update_readme(content: str) -> bool:
    """
    Update the README.md file with new content.
    
    Args:
        content: The content to write to README.md
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(README_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info("README.md updated successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to update README.md: {e}")
        return False

def main() -> None:
    """Main function to generate Pokemon greeting."""
    logger.info("Starting Pokemon greeting generation")
    
    # Load history
    history = load_history()
    
    # Generate random Pokemon ID
    pokemon_id = random.randint(1, MAX_POKEMON_ID)
    logger.info(f"Selected Pokemon ID: {pokemon_id}")
    
    # Fetch Pokemon data
    pokemon_data = fetch_pokemon_data(pokemon_id)
    if not pokemon_data:
        logger.error("Failed to fetch Pokemon data, exiting")
        return
    
    # Get sprite and info
    sprite_url = get_pokemon_sprite(pokemon_data)
    pokemon_info = get_pokemon_info(pokemon_data)
    
    # Generate README content
    readme_content = generate_readme_content(pokemon_data, sprite_url, pokemon_info)
    
    # Update README
    if update_readme(readme_content):
        # Update history
        history_entry = {
            'timestamp': datetime.now().isoformat(),
            'pokemon_id': pokemon_id,
            'pokemon_name': pokemon_info['name'],
            'types': pokemon_info['types']
        }
        history.append(history_entry)
        
        # Keep only last 100 entries
        if len(history) > 100:
            history = history[-100:]
        
        save_history(history)
        logger.info(f"Successfully generated greeting for {pokemon_info['name']}")
    else:
        logger.error("Failed to update README")

if __name__ == "__main__":
    main()
