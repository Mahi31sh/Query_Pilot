from app.config import settings
from sqlalchemy import create_engine, text

engine = create_engine(settings.database_url)

with engine.connect() as conn:
    print("Database:", conn.execute(text("SELECT current_database()")).scalar())
    print("User:", conn.execute(text("SELECT current_user")).scalar())

    result = conn.execute(text(
        "SELECT tablename FROM pg_tables "
        "WHERE schemaname = 'public' ORDER BY tablename"
    ))
    print("Tables:")
    for row in result:
        print("-", row[0])

engine.dispose()
