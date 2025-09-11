"""
Unit tests for the Pokemon Greeting Generator.
"""

import json
import unittest
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime

from generate import (
    fetch_pokemon_data,
    get_pokemon_sprite,
    get_pokemon_info,
    generate_readme_content,
    load_history,
    save_history,
    update_readme
)


class TestPokemonGreeting(unittest.TestCase):
    """Test cases for Pokemon greeting functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.sample_pokemon_data = {
            'id': 25,
            'name': 'pikachu',
            'height': 4,
            'weight': 60,
            'types': [
                {'type': {'name': 'electric'}}
            ],
            'sprites': {
                'front_default': 'https://example.com/pikachu.png',
                'front_shiny': 'https://example.com/pikachu_shiny.png'
            }
        }

    @patch('generate.requests.get')
    def test_fetch_pokemon_data_success(self, mock_get):
        """Test successful Pokemon data fetching."""
        mock_response = MagicMock()
        mock_response.json.return_value = self.sample_pokemon_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fetch_pokemon_data(25)
        
        self.assertEqual(result, self.sample_pokemon_data)
        mock_get.assert_called_once_with(
            'https://pokeapi.co/api/v2/pokemon/25', 
            timeout=10
        )

    @patch('generate.requests.get')
    def test_fetch_pokemon_data_failure(self, mock_get):
        """Test Pokemon data fetching failure."""
        mock_get.side_effect = Exception("Network error")
        
        result = fetch_pokemon_data(25)
        
        self.assertIsNone(result)

    def test_get_pokemon_sprite_with_default(self):
        """Test getting Pokemon sprite with front_default available."""
        result = get_pokemon_sprite(self.sample_pokemon_data)
        
        self.assertEqual(result, 'https://example.com/pikachu.png')

    def test_get_pokemon_sprite_fallback(self):
        """Test Pokemon sprite fallback when front_default is None."""
        pokemon_data = {
            'sprites': {
                'front_default': None,
                'front_shiny': 'https://example.com/pikachu_shiny.png'
            }
        }
        
        result = get_pokemon_sprite(pokemon_data)
        
        self.assertEqual(result, 'https://example.com/pikachu_shiny.png')

    def test_get_pokemon_sprite_no_sprites(self):
        """Test Pokemon sprite fallback when no sprites available."""
        pokemon_data = {'sprites': {}}
        
        result = get_pokemon_sprite(pokemon_data)
        
        self.assertEqual(
            result, 
            'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png'
        )

    def test_get_pokemon_info(self):
        """Test extracting Pokemon information."""
        result = get_pokemon_info(self.sample_pokemon_data)
        
        expected = {
            'name': 'Pikachu',
            'id': 25,
            'types': 'Electric',
            'height': '0.4 m',
            'weight': '6.0 kg'
        }
        
        self.assertEqual(result, expected)

    def test_get_pokemon_info_multiple_types(self):
        """Test extracting Pokemon info with multiple types."""
        pokemon_data = {
            'id': 1,
            'name': 'bulbasaur',
            'height': 7,
            'weight': 69,
            'types': [
                {'type': {'name': 'grass'}},
                {'type': {'name': 'poison'}}
            ]
        }
        
        result = get_pokemon_info(pokemon_data)
        
        self.assertEqual(result['types'], 'Grass / Poison')

    def test_generate_readme_content(self):
        """Test README content generation."""
        sprite_url = 'https://example.com/pikachu.png'
        pokemon_info = {
            'name': 'Pikachu',
            'id': 25,
            'types': 'Electric',
            'height': '0.4 m',
            'weight': '6.0 kg'
        }
        
        result = generate_readme_content(
            self.sample_pokemon_data, 
            sprite_url, 
            pokemon_info
        )
        
        self.assertIn('Pikachu', result)
        self.assertIn('#025', result)
        self.assertIn('Electric', result)
        self.assertIn('0.4 m', result)
        self.assertIn('6.0 kg', result)
        self.assertIn(sprite_url, result)

    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_load_history_empty(self, mock_file):
        """Test loading empty history."""
        result = load_history()
        
        self.assertEqual(result, [])

    @patch('builtins.open', new_callable=mock_open)
    def test_load_history_file_not_found(self, mock_file):
        """Test loading history when file doesn't exist."""
        mock_file.side_effect = FileNotFoundError()
        
        result = load_history()
        
        self.assertEqual(result, [])

    @patch('builtins.open', new_callable=mock_open)
    def test_save_history(self, mock_file):
        """Test saving history."""
        history = [{'pokemon_id': 25, 'pokemon_name': 'Pikachu'}]
        
        save_history(history)
        
        mock_file.assert_called_once_with('./pokemon_history.json', 'w', encoding='utf-8')

    @patch('builtins.open', new_callable=mock_open)
    def test_update_readme_success(self, mock_file):
        """Test successful README update."""
        content = "Test content"
        
        result = update_readme(content)
        
        self.assertTrue(result)
        mock_file.assert_called_once_with('./README.md', 'w', encoding='utf-8')
        mock_file().write.assert_called_once_with(content)

    @patch('builtins.open', side_effect=Exception("Write error"))
    def test_update_readme_failure(self, mock_file):
        """Test README update failure."""
        content = "Test content"
        
        result = update_readme(content)
        
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
