# PyBet: A Sports Betting Application with Machine Learning Predictions

PyBet is a comprehensive sports betting application that leverages machine learning to predict match outcomes and provide users with an interactive betting experience. The project combines a Django backend with a Vue.js frontend to deliver odds and user account management.

The application utilizes data from various sources, including API-Sports and web scraping from bookmakers, to provide up-to-date information on Premier League matches. PyBet's machine learning model analyzes historical match data to generate predictions, offering users valuable insights for informed betting decisions.

## Repository Structure

The PyBet project is organized into two main directories: `backend` and `frontend`, along with additional configuration files at the root level.

### Backend

- `backend/`: Contains the Django server and data collection scripts
  - `algorithms/`: Houses the machine learning model for match outcome prediction
  - `datacollection/`: Scripts for fetching and processing match data from various sources
  - `server/`: Django application files, including models, views, and URL configurations
  - `utils/`: Utility scripts for data processing and analysis

### Frontend

- `frontend/`: Vue.js application files
  - `src/`: Source code for the Vue.js components and routes
  - `public/`: Static assets and index.html
  - `tests/`: End-to-end and unit tests

### Key Files

- `backend/algorithms/optimized_algorithm.py`: Implements the machine learning model for match outcome prediction
- `backend/server/app/settings.py`: Django settings file
- `backend/server/manage.py`: Django management script
- `frontend/src/main.ts`: Entry point for the Vue.js application
- `frontend/src/router/index.ts`: Vue Router configuration
- `frontend/src/stores/store.ts`: Pinia store for state management
- `package.json`: Project dependencies and scripts

### Installation

1. Clone the repository:
```bash
git clone https://github.com/matadamczyk/PyBet.git
cd PyBet
```

2. Create and activate Python virtual environment:

On macOS and Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

On Windows:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate
```

3. Install all dependencies (Node.js and Python):
```bash
npm run install:all
```

This command will:
- Install Node.js dependencies for the root project
- Install Python dependencies from requirements.txt

4. Run database migrations:
```bash
npm run migrate
```

This command will:
- Set up the database schema
- Create necessary tables for user accounts and betting data
- Initialize the Django database

### Running the Application

1. Start both frontend and backend servers:
```bash
npm run start
```

This will concurrently run:
- Frontend Vue.js server at `http://localhost:5173`
- Backend Django server at `http://localhost:8000`

Alternatively, you can start servers separately:

```bash
# Start only frontend
npm run start:frontend

# Start only backend
npm run start:backend
```

## Data Flow

The PyBet application follows a client-server architecture with data flowing between the frontend, backend, and external data sources.

1. Data Collection:
   - Scripts in `backend/datacollection/` fetch match data from API-Sports and bookmaker websites
   - Collected data is processed and stored in CSV files or the database

2. Machine Learning Prediction:
   - `backend/algorithms/optimized_algorithm.py` trains on historical match data
   - The model generates predictions for upcoming matches

3. User Interaction:
   - Users interact with the Vue.js frontend to view odds and place bets
   - API requests are sent to the Django backend for data retrieval and bet placement

4. Backend Processing:
   - Django views handle API requests, interact with the database, and return responses
   - The machine learning model is queried for match predictions

5. State Management:
   - Pinia store (`frontend/src/stores/store.ts`) manages application state
   - User authentication state and bet data are stored and updated

```
[User] <-> [Vue.js Frontend] <-> [Django Backend] <-> [Database]
                ^                     ^
                |                     |
                v                     v
        [Pinia Store]    [Machine Learning Model]
                                 ^
                                 |
                                 v
                    [Data Collection Scripts]
                                 ^
                                 |
                                 v
            [API-Sports & Bookmaker Websites]
```

