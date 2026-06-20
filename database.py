"""Database operations for reminders."""

import sqlite3
from typing import List, Optional
from datetime import datetime
from config import DB_PATH, DB_TIMEOUT
from reminder import Reminder


class ReminderDatabase:
    """Handle all database operations for reminders."""
    
    def __init__(self, db_path=DB_PATH):
        """Initialize database connection."""
        self.db_path = db_path
        self.timeout = DB_TIMEOUT
        self.init_database()
    
    def get_connection(self):
        """Get database connection."""
        conn = sqlite3.connect(str(self.db_path), timeout=self.timeout)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database tables."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create reminders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'Pending',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
    
    def add_reminder(self, reminder: Reminder) -> int:
        """Add a new reminder to the database.
        
        Args:
            reminder: Reminder object to add
            
        Returns:
            The ID of the inserted reminder
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO reminders (title, date, time, description, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            reminder.title,
            reminder.date,
            reminder.time,
            reminder.description,
            reminder.status,
            reminder.created_at,
            reminder.updated_at
        ))
        
        reminder_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return reminder_id
    
    def get_reminder(self, reminder_id: int) -> Optional[Reminder]:
        """Get a specific reminder by ID.
        
        Args:
            reminder_id: ID of the reminder
            
        Returns:
            Reminder object or None if not found
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM reminders WHERE id = ?",
            (reminder_id,)
        )
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_reminder(row)
        return None
    
    def get_reminders_by_date(self, date: str) -> List[Reminder]:
        """Get all reminders for a specific date.
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            List of Reminder objects
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM reminders WHERE date = ? ORDER BY time",
            (date,)
        )
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_reminder(row) for row in rows]
    
    def get_reminders_by_month(self, year: int, month: int) -> List[Reminder]:
        """Get all reminders for a specific month.
        
        Args:
            year: Year
            month: Month (1-12)
            
        Returns:
            List of Reminder objects
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create date pattern for the month
        month_str = f"{year:04d}-{month:02d}"
        
        cursor.execute(
            "SELECT * FROM reminders WHERE date LIKE ? ORDER BY date, time",
            (f"{month_str}%",)
        )
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_reminder(row) for row in rows]
    
    def get_all_reminders(self) -> List[Reminder]:
        """Get all reminders from database.
        
        Returns:
            List of all Reminder objects
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM reminders ORDER BY date, time")
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_reminder(row) for row in rows]
    
    def update_reminder(self, reminder: Reminder) -> bool:
        """Update an existing reminder.
        
        Args:
            reminder: Updated Reminder object (must have an id)
            
        Returns:
            True if update was successful, False otherwise
        """
        if reminder.id is None:
            return False
        
        reminder.updated_at = datetime.now().isoformat()
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE reminders
            SET title = ?, date = ?, time = ?, description = ?, status = ?, updated_at = ?
            WHERE id = ?
        """, (
            reminder.title,
            reminder.date,
            reminder.time,
            reminder.description,
            reminder.status,
            reminder.updated_at,
            reminder.id
        ))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def delete_reminder(self, reminder_id: int) -> bool:
        """Delete a reminder by ID.
        
        Args:
            reminder_id: ID of the reminder to delete
            
        Returns:
            True if deletion was successful, False otherwise
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def get_dates_with_reminders(self, year: int, month: int) -> List[int]:
        """Get list of day numbers that have reminders in a given month.
        
        Args:
            year: Year
            month: Month (1-12)
            
        Returns:
            List of day numbers (1-31)
        """
        reminders = self.get_reminders_by_month(year, month)
        days = set()
        
        for reminder in reminders:
            # Extract day from date string (YYYY-MM-DD)
            day = int(reminder.date.split('-')[2])
            days.add(day)
        
        return sorted(list(days))
    
    @staticmethod
    def _row_to_reminder(row: sqlite3.Row) -> Reminder:
        """Convert database row to Reminder object.
        
        Args:
            row: Database row
            
        Returns:
            Reminder object
        """
        return Reminder(
            id=row['id'],
            title=row['title'],
            date=row['date'],
            time=row['time'],
            description=row['description'],
            status=row['status'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
