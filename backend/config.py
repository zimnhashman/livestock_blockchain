import os
from dotenv import load_dotenv

load_dotenv()

FARMER_ADDRESS = os.getenv('FARMER_ADDRESS')
FARMER_PRIVATE_KEY = os.getenv('FARMER_PRIVATE_KEY')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')
GANACHE_URL = os.getenv('GANACHE_URL', 'http://127.0.0.1:8545')
MYSQL_URI = os.getenv('MYSQL_URI', 'mysql+pymysql://user:pass@localhost/livestock_db')
DB_USER = os.getenv('DB_USER', 'your_mysql_username')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'your_mysql_password')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'livestock_db')

SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

if not FARMER_ADDRESS or not FARMER_PRIVATE_KEY or not CONTRACT_ADDRESS:
    raise Exception("Set FARMER_ADDRESS, FARMER_PRIVATE_KEY, and CONTRACT_ADDRESS in .env")
