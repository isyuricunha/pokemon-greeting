# 🎮 Pokemon Greeting Generator

<div align="center">
    <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png" width="150" height="150" alt="Pikachu">
    
    <h2>Welcome to the Pokemon Greeting Generator!</h2>
    
    <p>🌟 This repository automatically generates a new Pokémon greeting every 24 hours! 🌟</p>
    
    <p>
        <img src="https://img.shields.io/github/workflow/status/isyuricunha/pokemon-greeting/Generate%20README.md%20File?style=flat-square&logo=github-actions" alt="Build Status">
        <img src="https://img.shields.io/github/last-commit/isyuricunha/pokemon-greeting?style=flat-square&logo=github" alt="Last Commit">
        <img src="https://img.shields.io/github/license/isyuricunha/pokemon-greeting?style=flat-square" alt="License">
    </p>
</div>

---

## 🚀 How it works

This project uses GitHub Actions to automatically:

1. **Fetch** a random Pokémon from the [PokéAPI](https://pokeapi.co/)
2. **Generate** a beautiful greeting card with Pokémon information
3. **Update** this README.md file with the new greeting
4. **Commit** the changes back to the repository

The magic happens every day at midnight UTC, but you can also trigger it manually!

## ✨ Features

- 🎲 **Random Pokémon Selection** - From all 1025+ Pokémon available
- 🎨 **Beautiful Greeting Cards** - With sprites, types, and stats
- 📝 **Multiple Greeting Templates** - Variety in messages and styles
- 🔄 **Automatic Fallbacks** - Handles missing sprites gracefully
- 📊 **Pokemon History** - Keeps track of previously shown Pokémon
- 🛡️ **Error Handling** - Robust error handling and logging
- ⚡ **Fast & Reliable** - Optimized for quick execution

## 🛠️ Technical Details

### Technologies Used
- **Python 3.11** - Main programming language
- **GitHub Actions** - Automation and scheduling
- **PokéAPI** - Pokémon data source
- **Requests** - HTTP library for API calls

### Project Structure
```
pokemon-greeting/
├── generate.py          # Main script
├── requirements.txt     # Python dependencies
├── pokemon_history.json # History of shown Pokémon
├── .github/
│   └── workflows/
│       └── main.yml    # GitHub Actions workflow
└── README.md           # This file (auto-generated)
```

### Script Features
- **Type Hints** - Full type annotations for better code quality
- **Logging** - Comprehensive logging for debugging
- **Error Handling** - Graceful handling of API failures
- **Sprite Fallbacks** - Multiple sprite sources with fallbacks
- **History Tracking** - JSON-based history of generated greetings

## 🎯 Usage

### Automatic Updates
The repository updates automatically every 24 hours via GitHub Actions.

### Manual Trigger
You can manually trigger a new greeting by:
1. Going to the "Actions" tab
2. Selecting "Generate README.md File"
3. Clicking "Run workflow"

### Local Development
```bash
# Clone the repository
git clone https://github.com/isyuricunha/pokemon-greeting.git
cd pokemon-greeting

# Install dependencies
pip install -r requirements.txt

# Run the script
python generate.py
```

## 📈 Statistics

- **Total Pokémon Available**: 1025+
- **Greeting Templates**: 7 unique templates
- **Closing Messages**: 7 variations
- **Update Frequency**: Every 24 hours
- **Sprite Fallbacks**: 4 different sources

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

- 🎨 Add new greeting templates
- 🌐 Add multi-language support
- 📊 Improve the statistics display
- 🐛 Report bugs or suggest improvements
- ⭐ Star this repository if you like it!

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally with `python generate.py`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](license.md) file for details.

## 🙏 Acknowledgments

- [PokéAPI](https://pokeapi.co/) - For providing the amazing Pokémon data
- [GitHub Actions](https://github.com/features/actions) - For the automation platform
- The Pokémon Company - For creating these wonderful creatures

---

<div align="center">
    <p>Made with ❤️ and ☕ by <a href="https://github.com/isyuricunha">@isyuricunha</a></p>
    <p>Powered by <a href="https://pokeapi.co/">PokéAPI</a> | Automated with <a href="https://github.com/features/actions">GitHub Actions</a></p>
</div>
