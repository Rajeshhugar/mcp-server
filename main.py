#from fastapi import FastAPI, HTTPException, Query
from fastmcp import FastMCP
from pydantic import BaseModel
import os
import json
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

#app = FastAPI(title="ExpenseTracker")
mcp = FastMCP("Expense Tracker")

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""
CREATE TABLE IF NOT EXISTS expenses(
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  date TEXT NOT NULL,
                  amount REAL NOT NULL,
                  category TEXT NOT NULL,
                  subcategory TEXT DEFAULT "",
                  note TEXT DEFAULT ""
                  )
""")


init_db()


class Expense(BaseModel):
    date: str
    amount: float
    category: str
    subcategory: str = ""
    note: str = ""


@mcp.tool
def summarise(start_date: str, end_date: str, category: str | None = None):
    """Summarize the expenses by category within an inclusive date range."""
    query = """
        SELECT category, SUM(amount) as total_amount
        FROM expenses
        WHERE date BETWEEN ? AND ?
        """
    params = [start_date, end_date]

    if category:
        query += " AND category = ?"
        params.append(category)

    query += " GROUP BY category ORDER BY category ASC"

    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(query, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]


@mcp.tool       
def add_expense(expense: Expense):
    """Add a new expense entry to the database"""
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "INSERT INTO expenses(date,amount,category,subcategory,note) VALUES (?,?,?,?,?)",
            (expense.date, expense.amount, expense.category, expense.subcategory, expense.note),
        )
        return {"status": "ok", "id": cur.lastrowid}


@mcp.tool
def list_expenses():
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("SELECT id,date,amount,category,subcategory,note FROM expenses ORDER BY id ASC")
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]


@mcp.resource("info://categories")
def categories():
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)



if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)