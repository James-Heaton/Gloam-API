# Gloam: The Winding Path - API

The backend API for Gloam: The Winding Path, a dark fantasy text-based adventure game where users create and manage adventurers to explore a deadly castle.

## Tech Stack

- **Django 6.0** - Web framework
- **Django REST Framework** - API toolkit
- **SQLite** - Database
- **Token Authentication** - User authentication

## Features

- User registration and authentication
- Character CRUD operations
- Character types with unique stats (Fighter, Ranger, Wizard)
- Character traits system (Strong, Wise, Lucky, Stealthy)
- Automatic character stat management (HP, MP, starting area)
- Active character management (one active character per user)

## Setup

1. Clone the repository
```bash
git clone git@github.com:James-Heaton/Gloam-API.git
cd Gloam-API
```

2. Install dependencies with pipenv
```bash
pipenv install
```

3. Activate virtual environment
```bash
pipenv shell
```

4. Run migrations
```bash
python manage.py migrate
```

5. Seed reference data
```bash
python manage.py seed_data
```

6. Create superuser (optional, for admin access)
```bash
python manage.py createsuperuser
```

7. Run the development server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /register` - Create new user account
- `POST /login` - Login and receive auth token

### Reference Data (Read-only)
- `GET /charactertypes` - List all character types
- `GET /traits` - List all available traits
- `GET /areas` - List all game areas

### Characters
- `GET /characters` - List all characters for authenticated user
- `POST /characters` - Create a new character
- `GET /characters/<id>` - Get single character details
- `PUT /characters/<id>` - Update character (resets progress)
- `DELETE /characters/<id>` - Delete character

All character endpoints require authentication via token in headers:
```
Authorization: Token <your-token-here>
```

## Data Models

### Character
- User (FK to Django User)
- Name (cannot be changed after creation)
- Character Type (Fighter/Ranger/Wizard)
- HP/MP (auto-set from character type)
- Current Area (resets on character edit)
- Is Active (only one active character per user)
- Traits (exactly 2 required)

### Character Types
- Fighter: 12 HP, 8 MP
- Ranger: 10 HP, 10 MP
- Wizard: 8 HP, 12 MP

### Traits
- Strong: Chance to ignore harm
- Wise: Chance to ignore MP cost
- Lucky: Chance to improve your odds of success
- Stealthy: Automatically find safest route through an area

## Admin Panel

Access the Django admin at `http://localhost:8000/admin` to manage:
- Users
- Characters
- Areas
- Character Types
- Traits

## Project Status

This is the MVP version focusing on character CRUD operations. Future features include:
- Game adventure mechanics
- Turn-based gameplay
- Area progression
- Character death/resurrection mechanics

## License

This is a personal portfolio project.