from pathlib import Path
import sqlite3
from pickletools import uint8
from typing import List, Tuple, Optional

import numpy as np
from numpy import ndarray


def db_init():
    Path("Data").mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect("Data\\database.db")

    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS charts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            width INTEGER,
            height INTEGER,
            dx REAL,
            dy REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS ref_points (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chart_id INTEGER NOT NULL REFERENCES charts(id) ON DELETE CASCADE,
            ref_index INTEGER NOT NULL,
            pixel_x REAL NOT NULL,
            pixel_y REAL NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS ply_points (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chart_id INTEGER NOT NULL REFERENCES charts(id) ON DELETE CASCADE,
            ply_index INTEGER NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS chartdata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chart_id INTEGER NOT NULL REFERENCES charts(id) ON DELETE CASCADE,
            data BLOB NOT NULL,
            d1 INTEGER NOT NULL,
            d2 INTEGER NOT NULL,
            d3 INTEGER NOT NULL
        );
        """
    )
    conn.commit()

def insert_chart_with_points(
        name: str,
        chart_data: ndarray,
        meta: dict,
        ref_points: List[Tuple[int, float, float, float, float]],
        ply_points: List[Tuple[int, float, float]],
) -> int:

    conn = sqlite3.connect("Data\\database.db")
    try:
        cur = conn.cursor()
        cur.execute("delete from charts where name =? ",(name,))
        cur.execute(
            """
            INSERT INTO charts (name, width, height, dx, dy)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                name,
                meta.get("width"),
                meta.get("height"),
                meta.get("dx"),
                meta.get("dy"),
            ),
        )
        chart_id = cur.lastrowid

        cur.execute("""
                    INSERT INTO chartdata (chart_id,data,d1,d2,d3) 
                    VALUES(?,?,?,?,?)
                    """,
                    (chart_id, chart_data.tobytes(), chart_data.shape[0], chart_data.shape[1], chart_data.shape[2]))

        # Insert REF points
        if ref_points:
            ref_rows = [
                (chart_id, idx, px, py, lat, lon) for (idx, px, py, lat, lon) in ref_points
            ]
            cur.executemany(
                """
                INSERT INTO ref_points (chart_id, ref_index, pixel_x, pixel_y, latitude, longitude)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                ref_rows,
            )

        # Insert PLY points
        if ply_points:
            ply_rows = [(chart_id, idx, lat, lon) for (idx, lat, lon) in ply_points]
            cur.executemany(
                """
                INSERT INTO ply_points (chart_id, ply_index, latitude, longitude)
                VALUES (?, ?, ?, ?)
                """,
                ply_rows,
            )


        conn.commit()
    except Exception as e:
        print("trouble",e)
    finally:
        conn.close()
    return chart_id

def db_get_chart_names():
    conn = sqlite3.connect("Data\\database.db")

    cur = conn.cursor()
    cur.execute("select name from charts order by name asc")
    return cur.fetchall()


def db_get_chart(id=1) -> np.ndarray:
    conn = sqlite3.connect("Data\\database.db")
    try:
        cur = conn.cursor()
        cur.execute("SELECT data, d1, d2, d3 FROM chartdata WHERE chart_id = ?", (id,))
        row = cur.fetchone()
        if row is None:
            raise ValueError(f"No chart found with id {id}")

        data_blob, d1, d2, d3 = row
        return np.frombuffer(data_blob, dtype=np.uint8).reshape((d1, d2, d3))
    finally:
        conn.close()
