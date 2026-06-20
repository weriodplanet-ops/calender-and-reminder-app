"""Configuration settings for the Calendar and Reminder App."""

import os
from pathlib import Path

# Project directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "reminders.db"

# Create data directory if it doesn't exist
DATA_DIR.mkdir(exist_ok=True)

# Application settings
APP_NAME = "Calendar and Reminder App"
APP_VERSION = "1.0.0"

# GUI Settings
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
WINDOW_TITLE = f"{APP_NAME} v{APP_VERSION}"

# Color scheme
COLORS = {
    "bg_main": "#f0f0f0",
    "bg_header": "#2c3e50",
    "bg_calendar": "#ecf0f1",
    "bg_weekend": "#e8e8e8",
    "bg_today": "#3498db",
    "bg_reminder": "#e74c3c",
    "bg_button": "#3498db",
    "text_header": "#ffffff",
    "text_main": "#2c3e50",
    "text_button": "#ffffff",
    "border": "#bdc3c7",
}

# Database settings
DB_NAME = "reminders"
DB_TIMEOUT = 30

# Reminder settings
DEFAULT_REMINDER_TIME = "09:00"
REMINDER_STATUSES = ["Pending", "Completed", "Cancelled"]
