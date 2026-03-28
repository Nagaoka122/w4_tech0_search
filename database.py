"""
database.py — Tech0 Search v1.1
SQLite DB への接続・初期化・CRUD・ログ操作を一元管理する。
"""

import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("data/tech0_search.db")


def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    with open("schema.sql", "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()


def insert_page(page: dict) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO pages
            (url, title, description, full_text, author, category, word_count, crawled_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        page["url"],
        page["title"],
        page.get("description", ""),
        page.get("full_text", ""),
        page.get("author", ""),
        page.get("category", ""),
        page.get("word_count", 0),
        page.get("crawled_at", datetime.now().isoformat()),
    ))

    page_id = cursor.lastrowid

        # 既存キーワードを削除
    cursor.execute("DELETE FROM keywords WHERE page_id = ?", (page_id,))

    # 新しいキーワードを登録
    keywords = page.get("keywords", [])
    for kw in keywords:
        kw = kw.strip()
        if kw:
            cursor.execute("""
                INSERT INTO keywords (page_id, keyword, tf_score, tfidf_score)
                VALUES (?, ?, 0.0, 0.0)
            """, (page_id, kw))
            
    conn.commit()
    conn.close()
    return page_id


def get_all_pages() -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pages ORDER BY created_at DESC")
    rows = cursor.fetchall()

    pages = []
    for row in rows:
        page = dict(row)

        cursor.execute(
            "SELECT keyword FROM keywords WHERE page_id = ? ORDER BY id",
            (page["id"],)
        )
        page["keywords"] = [r["keyword"] for r in cursor.fetchall()]

        pages.append(page)

    conn.close()
    return pages


def get_page_by_url(url: str) -> dict | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pages WHERE url = ?", (url,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def log_search(query: str, results_count: int, user_id: str = None) -> int:
    """
    検索ログを search_logs に記録し、そのログIDを返す。
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO search_logs (query, results_count, user_id)
        VALUES (?, ?, ?)
    """, (query.strip(), results_count, user_id))

    search_log_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return search_log_id


def log_click(search_log_id: int | None, page_id: int, position: int | None = None) -> int:
    """
    検索結果のクリックログを click_logs に記録する。
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO click_logs (search_log_id, page_id, position)
        VALUES (?, ?, ?)
    """, (search_log_id, page_id, position))

    click_log_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return click_log_id


def get_search_stats(limit: int = 10) -> dict:
    """
    検索統計を集計して返す。
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT query, COUNT(*) AS search_count,
               AVG(results_count) AS avg_results_count,
               MAX(searched_at) AS last_searched_at
        FROM search_logs
        GROUP BY query
        ORDER BY search_count DESC, last_searched_at DESC
        LIMIT ?
    """, (limit,))
    popular_queries = [dict(row) for row in cursor.fetchall()]

    cursor.execute("""
        SELECT p.id, p.title, p.url, COUNT(*) AS click_count
        FROM click_logs c
        JOIN pages p ON c.page_id = p.id
        GROUP BY p.id, p.title, p.url
        ORDER BY click_count DESC, p.title ASC
        LIMIT ?
    """, (limit,))
    popular_pages = [dict(row) for row in cursor.fetchall()]

    cursor.execute("SELECT COUNT(*) AS cnt FROM search_logs")
    total_searches = cursor.fetchone()["cnt"]

    cursor.execute("SELECT COUNT(*) AS cnt FROM click_logs")
    total_clicks = cursor.fetchone()["cnt"]

    conn.close()

    return {
        "total_searches": total_searches,
        "total_clicks": total_clicks,
        "popular_queries": popular_queries,
        "popular_pages": popular_pages,
    }