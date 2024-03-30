#database.py
import sqlite3
import bcrypt
from settings import DATABASE_PATH


def db_connect(db_path=DATABASE_PATH):
    return sqlite3.connect(db_path)


def init_db():
    with db_connect() as conn:
        with open('schema.sql', 'r') as f:
            conn.executescript(f.read())


def create_account(username, password):
    with db_connect() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone() is not None:
            return False  # Username already exists

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))

        conn.commit()
        return True


def verify_login(username, password):
    with db_connect() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT password FROM users WHERE username = ?", (username,))
        user_record = cursor.fetchone()

        if user_record and bcrypt.checkpw(password.encode('utf-8'), user_record[0]):
            return True
        return False


def insert_network_traffic(data):
    with db_connect() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO network_traffic (src_ip, dst_ip, protocol, src_port, dst_port, packet_length, flags, checksum, ttl, ihl, tos, payload, timestamp, label) 
            VALUES (:src_ip, :dst_ip, :protocol, :src_port, :dst_port, :packet_length, :flags, :checksum, :ttl, :ihl, :tos, :payload, :timestamp, :label)
            ''', data
        )
        conn.commit()


def add_column_to_table():
    with db_connect() as conn:
        cursor = conn.cursor()

        cursor.execute("PRAGMA table_info(network_traffic);")
        if 'checksum' not in [column[1] for column in cursor.fetchall()]:
            cursor.execute(
                "ALTER TABLE network_traffic ADD COLUMN checksum TEXT;")
            conn.commit()
            print("Column added successfully.")
        else:
            print("Column already exists.")

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
