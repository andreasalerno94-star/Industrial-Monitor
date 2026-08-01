import os
import sqlite3
from datetime import datetime, timedelta

DB_PATH = os.environ.get('DB_PATH', 'alarms.db')


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS alarms (
                id             INTEGER PRIMARY KEY,
                machine_id     INTEGER,
                machine_name   TEXT,
                sensor         TEXT,
                value          REAL,
                threshold_min  REAL,
                threshold_max  REAL,
                timestamp      TEXT
            )
        ''')


def save_alarm(machine_id, machine_name, sensor, value, threshold_min, threshold_max):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            '''INSERT INTO alarms
               (machine_id, machine_name, sensor, value,
                threshold_min, threshold_max, timestamp)
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (machine_id, machine_name, sensor, value,
             threshold_min, threshold_max,
             datetime.now().isoformat()),
        )


def get_alarms(days=7):
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            'SELECT * FROM alarms WHERE timestamp >= ? ORDER BY timestamp DESC',
            (cutoff,),
        ).fetchall()
    return [dict(row) for row in rows]


def cleanup_old(days=7):
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('DELETE FROM alarms WHERE timestamp < ?', (cutoff,))
