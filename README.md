# BitBuddy Cryptocurrency Platform

BitBuddy is a cryptocurrency platform built with Flask that allows users to buy, sell, and stake cryptocurrencies, as well as providing access to real-time market data through external APIs.

## Features

- User authentication and registration systems
- Dashboard to view user information and portfolio
- Real-time market data for Bitcoin and blockchain information
- Ability to buy and sell Bitcoin
- Transaction history tracking
- Staking calculator to estimate returns
- RESTful API for managing cryptocurrencies
- Crypto mining game

## Technologies Used

- Flask: Python web framework for backend development
- SQLAlchemy: Python SQL toolkit and Object-Relational Mapper (ORM)
- Flask Bcrypt: Flask extension for password hashing
- Flask CORS: Flask extension for handling Cross-Origin Resource Sharing (CORS)
- PostgreSQL: Relational database management system
- External APIs:
  - Crypto API: for fetching real-time market data
  - Blockchain API: for retrieving blockchain information
- HTML/CSS/JS: Frontend development
- Jinja2: Templating engine for rendering HTML templates
- WTForms: Library for handling form rendering and validation in Flask
- Psycopg2: PostgreSQL adapter for Python
- Requests: HTTP library for making API calls
- Python Decimal: Library for precise decimal arithmetic

## Project Structure

- **app.py**: Main Flask application file containing route definitions and application setup.
- **models.py**: SQLAlchemy models for database tables.
- **forms.py**: Flask-WTF forms for user registration and login.
- **templates/**: HTML templates for rendering pages.
- **static/**: Static files such as CSS and JavaScript.
- **seed.sql**: SQL script for seeding the database with initial data.
- **README.md**: Documentation for the project.

## Getting Started

1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Set up a PostgreSQL database and update the `SQLALCHEMY_DATABASE_URI` in `app.py` with your database URL.
4. Run the database migration using `flask db upgrade`.
5. Seed the database with initial data by running `psql < seed.sql`.
6. Start the Flask server with `flask run`.

## Usage

- Register a new account or log in with existing credentials.
- Explore the dashboard to view user information and portfolio.
- Buy and sell Bitcoin from the respective pages.
- View transaction history and staking returns.
- Access real-time market data for Bitcoin and blockchain information.
- Play the crypto mining game for fun!

## External API Integration

This project uses external APIs to fetch real-time data for Bitcoin prices and blockchain information. 

### Setting Up API Keys

1. Obtain an API key from CoinMarketCap by signing up at [CoinMarketCap API](https://pro.coinmarketcap.com/signup/).

2. Set the API key as an environment variable. You can do this by running the following command in your terminal:

   ```sh
   export COINMARKETCAP_API_KEY="Enter your key here"

   OR 
   To make the change permanent try this:


   echo 'export COINMARKETCAP_API_KEY="Enter your key here"' >> ~/.bashrc
source ~/.bashrc

## API Documentation

- `/api/cryptocurrencies`: GET (List all cryptocurrencies), POST (Add a new cryptocurrency)
- `/api/cryptocurrencies/<int:currency_id>`: GET (Get details of a specific cryptocurrency), PATCH (Update a cryptocurrency), DELETE (Delete a cryptocurrency)

## Testing

- All tests work and come back 'OK' 
- Be sure to psql < seed.sql after running the tests to reseed the database.

## Credits

- This project was developed by Joseph Skokan.
- External APIs used: Crypto API, Blockchain API.
- ATGTG.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
