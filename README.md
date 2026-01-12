# Gloam: The Winding Path - API

The backend API for Gloam: The Winding Path, a dark fantasy text-based adventure game. Players create characters and navigate a deadly castle with hidden dice mechanics and trait-based gameplay.

**Frontend Repository**: https://github.com/James-Heaton/Gloam-Client

## Tech Stack

- **Django 6.0** - Web framework
- **Django REST Framework** - RESTful API
- **SQLite** - Database (development)
- **Token Authentication** - Secure user sessions

## Features

### Game Mechanics
- **Character Management**: Create, edit, and delete characters with unique stats
- **Character Types**: Fighter (7 HP, 5 MP), Ranger (6 HP, 6 MP), Wizard (5 HP, 7 MP)
- **Trait System**: Choose 2 traits per character (Lucky, Strong, Wise, Stealthy)
- **Hidden Dice Rolling**: Server-side 2d6 resolution prevents cheating
- **Action Types**: Safe (no risk), Risky (2d6 outcomes), Magic (costs MP)
- **Trait Procs**: Lucky (35%), Strong (25%), Wise (25%), Stealthy (3 uses)
- **Resource Management**: HP, MP, GP tracked throughout adventure
- **Persistent Progress**: Game state auto-saves, resume anytime

### Security & Data
- **Token-based auth**: Secure user sessions
- **Server-side validation**: All game logic happens backend
- **User isolation**: Players only access their own characters
- **Game state integrity**: No client-side manipulation possible

## Project Structure
```
Gloam-API/
├── fixtures/               # Game content (areas, actions, traits)
├── gloam_api/              # Django project settings
├── gloam_api_app/
│   ├── logic/              # Game engine
│   │   ├── dice.py         # 2d6 rolls, trait procs
│   │   └── game_engine.py  # Action execution, state management
│   ├── migrations/         # Database migrations
│   ├── models.py           # Database models
│   ├── serializers/        # DRF serializers
│   │   ├── character_serializers.py
│   │   ├── game_serializers.py
│   │   └── reference_serializers.py
│   └── views/              # API endpoints
│       ├── auth.py
│       ├── character_views.py
│       ├── game_views.py
│       └── reference_views.py
└── manage.py
```

## Setup & Installation

### Prerequisites
- Python 3.13+
- pipenv

### Installation

1. **Clone the repository**
```bash
git clone git@github.com:James-Heaton/Gloam-API.git
cd Gloam-API
```

2. **Install dependencies**
```bash
pipenv install
```

3. **Activate virtual environment**
```bash
pipenv shell
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Load game content**
```bash
python manage.py loaddata fixtures/character_types.json
python manage.py loaddata fixtures/traits.json
python manage.py loaddata fixtures/areas.json
python manage.py loaddata fixtures/actions.json
```

6. **Create superuser (optional)**
```bash
python manage.py createsuperuser
```

7. **Start development server**
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /register` - Create account
- `POST /login` - Get auth token

### Reference Data
- `GET /charactertypes` - List character types
- `GET /traits` - List available traits
- `GET /areas` - List all areas

### Characters
- `GET /characters` - List user's characters
- `POST /characters` - Create character
- `GET /characters/<id>` - Get character details
- `PUT /characters/<id>` - Update character (resets progress)
- `DELETE /characters/<id>` - Delete character

### Game
- `GET /game/state` - Get current game state
- `POST /game/action` - Execute action
- `POST /game/reset` - Reset character to start

**Authentication**: All endpoints except `/register` and `/login` require:
```
Authorization: Token <your-token-here>
```

## Game Mechanics

### Character Types
| Type    | HP  | MP  | Playstyle              |
|---------|-----|-----|------------------------|
| Fighter | 7   | 5   | Durable, less magic    |
| Ranger  | 6   | 6   | Balanced               |
| Wizard  | 5   | 7   | Fragile, magic-focused |

### Traits
| Trait    | Effect                                |
|----------|---------------------------------------|
| Lucky    | 35% chance for +1 to risky rolls      |
| Strong   | 25% chance to reduce damage by 1      |
| Wise     | 25% chance to refund 1 MP             |
| Stealthy | Safe passage through area (3 uses)    |

### Action Resolution
**Safe Actions**: No roll, no damage, advance safely

**Risky Actions** (2d6):
- 1-6 (Failure): Take damage, no reward
- 7-9 (Mixed): Take damage, get reward
- 10-12 (Success): No damage, get reward

**Magic Actions**: Cost MP, always safe, variable rewards

## Development

### Admin Panel
Access at `http://localhost:8000/admin` to manage game content.

### Exporting Fixtures
```bash
python manage.py dumpdata gloam_api_app.CharacterType --indent 2 > fixtures/character_types.json
python manage.py dumpdata gloam_api_app.Trait --indent 2 > fixtures/traits.json
python manage.py dumpdata gloam_api_app.Area --indent 2 > fixtures/areas.json
python manage.py dumpdata gloam_api_app.Action --indent 2 > fixtures/actions.json
```

### Testing with curl
```bash
# Register
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"player","password":"pass123"}'

# Login
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"player","password":"pass123"}'

# Get game state
curl http://localhost:8000/game/state \
  -H "Authorization: Token YOUR_TOKEN"

# Execute action
curl -X POST http://localhost:8000/game/action \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"action_id": 1}'
```

## Credits

- **Developer**: James Heaton
- **Nashville Software School**: Coding Bootcamp Capstone Project

## License

This project is for educational purposes.