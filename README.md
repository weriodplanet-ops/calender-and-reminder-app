# Calendar and Reminder App

A Python application that displays a monthly calendar with the ability to set and manage reminders.

## Features

- **Monthly Calendar Display**: Interactive GUI showing a full month view
- **Reminder Management**: Create, edit, delete, and view reminders
- **Persistent Storage**: All reminders are saved to a database
- **Date Navigation**: Easy navigation between months and years
- **Reminder Notifications**: Visual indicators for dates with reminders
- **Time-based Reminders**: Set reminders for specific times on specific dates

## Project Structure

```
calender-and-reminder-app/
├── main.py                 # Entry point of the application
├── calendar_app.py         # Main GUI application
├── reminder.py             # Reminder data model
├── database.py             # Database operations
├── config.py               # Configuration settings
├── requirements.txt        # Project dependencies
├── data/                   # Data directory
│   └── reminders.db        # SQLite database (auto-created)
└── README.md              # This file
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/weriodplanet-ops/calender-and-reminder-app.git
   cd calender-and-reminder-app
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python main.py
```

### How to Use

1. **Navigate Calendar**: Use the arrow buttons to move between months
2. **Add Reminder**: Click on any date to open the reminder dialog
3. **View Reminders**: Click on highlighted dates to see all reminders for that date
4. **Edit Reminder**: Select a reminder from the list and click "Edit"
5. **Delete Reminder**: Select a reminder and click "Delete"

## Features in Detail

### Calendar Display
- Shows the current month by default
- Dates with reminders are highlighted in a different color
- Easy month/year navigation

### Reminder Management
- Title and description for each reminder
- Set specific time for reminders
- Mark reminders as completed
- Edit existing reminders
- Delete reminders

## Technology Stack

- **GUI Framework**: tkinter (built-in with Python)
- **Database**: SQLite3
- **Date Handling**: datetime, calendar modules

## Requirements

See `requirements.txt` for all dependencies.

## Future Enhancements

- Email notifications for reminders
- Sound alerts
- Recurring reminders
- Reminder categories/tags
- Dark mode theme
- Export/Import functionality
- Multiple calendar views (weekly, yearly)

## License

MIT License

## Author

Weriodplanet Ops
