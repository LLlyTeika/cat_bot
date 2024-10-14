import os
import sqlite3


# Функция для проверки наличия таблицы
def check_table_exists(table_name, cursor):
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
    result = cursor.fetchone()
    if result:
        print(f"Таблица '{table_name}' существует.")
        return True
    else:
        print(f"Таблица '{table_name}' не найдена.")
        return False


# Функция для проверки наличия полей в таблице и создание таблицы, если она отсутствует
def check_or_create_table(table_name, expected_columns, create_table_sql, cursor):
    if not check_table_exists(table_name, cursor):
        print(f"Создание таблицы '{table_name}'...")
        cursor.execute(create_table_sql)
        print(f"Таблица '{table_name}' успешно создана.")
    else:
        # Если таблица существует, проверяем наличие колонок
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]  # Получаем имена колонок
        print(f"Колонки в таблице '{table_name}': {column_names}")

        # Проверка, что все ожидаемые колонки существуют
        for col in expected_columns:
            if col not in column_names:
                print(f"Колонка '{col}' отсутствует в таблице '{table_name}'.")
            else:
                print(f"Колонка '{col}' найдена в таблице '{table_name}'.")


# SQL-запросы для создания таблиц
create_admins_sql = """
CREATE TABLE admins (
    id INTEGER NOT NULL UNIQUE,
    PRIMARY KEY(id)
);
"""

create_users_sql = """
CREATE TABLE users (
    id INTEGER NOT NULL UNIQUE,
    full_name TEXT,
    tag TEXT,
    PRIMARY KEY(id)
);
"""

create_users_cats_sql = """
CREATE TABLE users_cats (
    id INTEGER NOT NULL UNIQUE,
    user_id INTEGER NOT NULL,
    photo_id TEXT NOT NULL UNIQUE,
    PRIMARY KEY(id AUTOINCREMENT)
);
"""


def start_check():
    # Путь к базе данных
    db_path = 'db.db'

    # Проверка, существует ли база данных (файл)
    if os.path.exists(db_path):
        print(f"База данных {db_path} существует.")
    else:
        print(f"База данных {db_path} не существует. Она будет создана автоматически.")

    # Подключение к базе данных
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Проверка или создание таблиц
    check_or_create_table('admins', ['id'], create_admins_sql, cursor)
    check_or_create_table('users', ['id', 'full_name', 'tag'], create_users_sql, cursor)
    check_or_create_table('users_cats', ['id', 'user_id', 'photo_id'], create_users_cats_sql, cursor)

    # Закрытие соединения
    conn.commit()  # Сохраняем изменения
    conn.close()
