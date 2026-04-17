from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from decouple import config
import urllib.parse

# Get exact credentials from your .env file
DB_USER = str(config("POSTGRES_USER", default="sadat"))
# URL encode the password to safely handle characters like '!'
DB_PASSWORD = urllib.parse.quote_plus(str(config("POSTGRES_PASSWORD")))
DB_HOST = str(config("DB_HOST", default="127.0.0.1"))
DB_PORT = str(config("DB_PORT", default="5433"))
DB_NAME = str(config("POSTGRES_DB", default="ai_images_db"))

# Expected format: postgresql://user:password@localhost:5432/agency_db
SQLALCHEMY_DATABASE_URL = config(
    "DATABASE_URL", 
    default=f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL) # type: ignore
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get DB session in endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()