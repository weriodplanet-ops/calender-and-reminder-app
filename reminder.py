"""Data model for reminders."""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


@dataclass
class Reminder:
    """Represents a reminder with all necessary information."""
    
    title: str
    date: str  # Format: YYYY-MM-DD
    time: str  # Format: HH:MM
    description: str = ""
    status: str = "Pending"  # Pending, Completed, Cancelled
    created_at: str = None
    updated_at: str = None
    id: Optional[int] = None
    
    def __post_init__(self):
        """Initialize timestamps if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.updated_at is None:
            self.updated_at = self.created_at
    
    def to_dict(self):
        """Convert reminder to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create reminder from dictionary."""
        return cls(**data)
    
    def __str__(self):
        """String representation of the reminder."""
        return f"{self.title} on {self.date} at {self.time}"
    
    def mark_completed(self):
        """Mark reminder as completed."""
        self.status = "Completed"
        self.updated_at = datetime.now().isoformat()
    
    def is_overdue(self):
        """Check if reminder is overdue."""
        if self.status == "Completed" or self.status == "Cancelled":
            return False
        
        reminder_datetime = datetime.fromisoformat(f"{self.date}T{self.time}:00")
        return datetime.now() > reminder_datetime
