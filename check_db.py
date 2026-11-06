from sqlalchemy import inspect
from app.database import engine

inspector = inspect(engine)

print("Таблицы в базе данных:")

for table in inspector.get_table_names():
    print("-", table)