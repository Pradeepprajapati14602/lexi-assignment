"""
Database initialization script.
Run this to create all tables.
"""

from app.db.database import init_db

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print(" Database initialized successfully - UOIONHHC")
