#!/usr/bin/env python3
"""Entry point for the Calendar and Reminder App."""

import sys
import os

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from calendar_app import CalendarApp


def main():
    """Main entry point."""
    app = CalendarApp()
    app.mainloop()


if __name__ == "__main__":
    main()
