import sys
from pathlib import Path

# Добавляем корень проекта в PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from app.database import engine
from app.models import Base

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")

if __name__ == "__main__":
    init_db()