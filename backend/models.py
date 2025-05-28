from sqlalchemy import create_engine, Column, Integer, Float, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get DB credentials from environment
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME')

# Compose full connection string
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine and session
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

# Base model
Base = declarative_base()

# Sensor data table
class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float, nullable=False)
    acceleration = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    tx_hash = Column(String(66), nullable=False)  # Ethereum transaction hash (0x + 64 chars)
    access_control = Column(String, nullable=True)  # JSON-encoded string of attributes

# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)
