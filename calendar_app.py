"""Main GUI application for the Calendar and Reminder App."""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta
import calendar
from typing import Optional

from config import (
    APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE,
    COLORS, DEFAULT_REMINDER_TIME
)
from database import ReminderDatabase
from reminder import Reminder


class CalendarApp(tk.Tk):
    """Main application window."""
    
    def __init__(self):
        """Initialize the application."""
        super().__init__()
        
        self.title(WINDOW_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(800, 600)
        
        # Initialize database
        self.db = ReminderDatabase()
        
        # Current month and year
        today = datetime.now()
        self.current_year = today.year
        self.current_month = today.month
        
        # Selected date for reminder operations
        self.selected_date: Optional[str] = None
        
        # Configure style
        self._configure_styles()
        
        # Build UI
        self._create_ui()
        
        # Bind events
        self._bind_events()
    
    def _configure_styles(self):
        """Configure tkinter styles."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        self.configure(bg=COLORS['bg_main'])
    
    def _create_ui(self):
        """Create the user interface."""
        # Header frame
        header_frame = tk.Frame(self, bg=COLORS['bg_header'])
        header_frame.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0)
        
        # Title
        title_label = tk.Label(
            header_frame, text=APP_NAME, font=("Arial", 18, "bold"),
            bg=COLORS['bg_header'], fg=COLORS['text_header']
        )
        title_label.pack(pady=10)
        
        # Main content frame
        main_frame = tk.Frame(self, bg=COLORS['bg_main'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Calendar frame
        calendar_frame = tk.Frame(main_frame, bg=COLORS['bg_calendar'])
        calendar_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Month/Year navigation
        nav_frame = tk.Frame(calendar_frame, bg=COLORS['bg_calendar'])
        nav_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.month_year_label = tk.Label(
            nav_frame, text="", font=("Arial", 14, "bold"),
            bg=COLORS['bg_calendar'], fg=COLORS['text_main']
        )
        self.month_year_label.pack()
        
        # Navigation buttons
        button_frame = tk.Frame(nav_frame, bg=COLORS['bg_calendar'])
        button_frame.pack()
        
        prev_btn = tk.Button(
            button_frame, text="< Previous", command=self.previous_month,
            bg=COLORS['bg_button'], fg=COLORS['text_button'],
            relief=tk.RAISED, cursor="hand2"
        )
        prev_btn.pack(side=tk.LEFT, padx=5)
        
        today_btn = tk.Button(
            button_frame, text="Today", command=self.go_to_today,
            bg=COLORS['bg_button'], fg=COLORS['text_button'],
            relief=tk.RAISED, cursor="hand2"
        )
        today_btn.pack(side=tk.LEFT, padx=5)
        
        next_btn = tk.Button(
            button_frame, text="Next >", command=self.next_month,
            bg=COLORS['bg_button'], fg=COLORS['text_button'],
            relief=tk.RAISED, cursor="hand2"
        )
        next_btn.pack(side=tk.LEFT, padx=5)
        
        # Calendar grid
        self.calendar_frame = tk.Frame(calendar_frame, bg=COLORS['bg_calendar'])
        self.calendar_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Reminders panel
        reminders_frame = tk.Frame(main_frame, bg=COLORS['bg_main'])
        reminders_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        reminders_label = tk.Label(
            reminders_frame, text="Reminders", font=("Arial", 14, "bold"),
            bg=COLORS['bg_main'], fg=COLORS['text_main']
        )
        reminders_label.pack(pady=10)
        
        # Reminders listbox
        list_frame = tk.Frame(reminders_frame, bg=COLORS['bg_main'])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.reminders_listbox = tk.Listbox(
            list_frame, yscrollcommand=scrollbar.set,
            bg=COLORS['bg_calendar'], fg=COLORS['text_main'],
            font=("Arial", 10), height=10
        )
        self.reminders_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.reminders_listbox.yview)
        self.reminders_listbox.bind('<<ListboxSelect>>', self._on_reminder_select)
        
        # Reminder action buttons
        action_frame = tk.Frame(reminders_frame, bg=COLORS['bg_main'])
        action_frame.pack(fill=tk.X, padx=10, pady=5)
        
        add_btn = tk.Button(
            action_frame, text="Add Reminder", command=self.add_reminder,
            bg=COLORS['bg_button'], fg=COLORS['text_button'],
            relief=tk.RAISED, cursor="hand2"
        )
        add_btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        edit_btn = tk.Button(
            action_frame, text="Edit", command=self.edit_reminder,
            bg=COLORS['bg_button'], fg=COLORS['text_button'],
            relief=tk.RAISED, cursor="hand2"
        )
        edit_btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        delete_btn = tk.Button(
            action_frame, text="Delete", command=self.delete_reminder,
            bg=COLORS['bg_button'], fg=COLORS['text_button'],
            relief=tk.RAISED, cursor="hand2"
        )
        delete_btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        # Status bar
        status_frame = tk.Frame(self, bg=COLORS['bg_header'])
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=0, pady=0)
        
        self.status_label = tk.Label(
            status_frame, text="Ready", font=("Arial", 10),
            bg=COLORS['bg_header'], fg=COLORS['text_header']
        )
        self.status_label.pack(pady=5)
        
        # Initial calendar render
        self.render_calendar()
    
    def render_calendar(self):
        """Render the calendar for the current month."""
        # Clear calendar frame
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        
        # Update month/year label
        month_name = calendar.month_name[self.current_month]
        self.month_year_label.config(text=f"{month_name} {self.current_year}")
        
        # Get days with reminders
        days_with_reminders = self.db.get_dates_with_reminders(
            self.current_year, self.current_month
        )
        
        # Get current date
        today = datetime.now()
        is_current_month = (
            self.current_year == today.year and
            self.current_month == today.month
        )
        
        # Weekday headers
        weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(weekdays):
            is_weekend = i >= 5
            label = tk.Label(
                self.calendar_frame, text=day,
                bg=COLORS['bg_weekend'] if is_weekend else COLORS['bg_calendar'],
                fg=COLORS['text_main'], font=("Arial", 10, "bold"),
                relief=tk.RAISED, width=8, height=2
            )
            label.grid(row=0, column=i, sticky='nsew', padx=1, pady=1)
        
        # Get calendar days
        cal = calendar.monthcalendar(self.current_year, self.current_month)
        
        # Create buttons for each day
        for week_num, week in enumerate(cal, start=1):
            for day_num, day in enumerate(week):
                if day == 0:
                    # Empty cell for days from other months
                    label = tk.Label(
                        self.calendar_frame, text="",
                        bg=COLORS['bg_main']
                    )
                    label.grid(row=week_num, column=day_num, sticky='nsew', padx=1, pady=1)
                else:
                    # Day button
                    is_today = is_current_month and day == today.day
                    has_reminder = day in days_with_reminders
                    is_weekend = day_num >= 5
                    
                    # Determine colors
                    if is_today:
                        bg_color = COLORS['bg_today']
                        text_color = COLORS['text_header']
                    elif has_reminder:
                        bg_color = COLORS['bg_reminder']
                        text_color = COLORS['text_header']
                    elif is_weekend:
                        bg_color = COLORS['bg_weekend']
                        text_color = COLORS['text_main']
                    else:
                        bg_color = COLORS['bg_calendar']
                        text_color = COLORS['text_main']
                    
                    btn = tk.Button(
                        self.calendar_frame, text=str(day),
                        bg=bg_color, fg=text_color, font=("Arial", 10, "bold"),
                        relief=tk.RAISED, width=8, height=3,
                        command=lambda d=day: self.on_date_select(d),
                        cursor="hand2"
                    )
                    btn.grid(row=week_num, column=day_num, sticky='nsew', padx=1, pady=1)
        
        # Configure grid weights for responsiveness
        for i in range(7):
            self.calendar_frame.grid_columnconfigure(i, weight=1)
        for i in range(len(cal) + 1):
            self.calendar_frame.grid_rowconfigure(i, weight=1)
    
    def on_date_select(self, day: int):
        """Handle date selection."""
        year = self.current_year
        month = self.current_month
        self.selected_date = f"{year:04d}-{month:02d}-{day:02d}"
        
        # Load reminders for selected date
        self.load_reminders_for_date(self.selected_date)
        
        # Update status
        date_obj = datetime.strptime(self.selected_date, "%Y-%m-%d")
        date_str = date_obj.strftime("%A, %B %d, %Y")
        self.status_label.config(text=f"Selected: {date_str}")
    
    def load_reminders_for_date(self, date: str):
        """Load and display reminders for a specific date."""
        reminders = self.db.get_reminders_by_date(date)
        
        # Clear listbox
        self.reminders_listbox.delete(0, tk.END)
        
        # Store reminders for later access
        self.current_reminders = reminders
        
        if not reminders:
            self.reminders_listbox.insert(tk.END, "No reminders for this date")
        else:
            for reminder in reminders:
                status_indicator = "✓" if reminder.status == "Completed" else " "
                display_text = f"[{status_indicator}] {reminder.time} - {reminder.title}"
                self.reminders_listbox.insert(tk.END, display_text)
    
    def _on_reminder_select(self, event):
        """Handle reminder selection in listbox."""
        pass  # Currently just for display
    
    def add_reminder(self):
        """Open dialog to add a new reminder."""
        if self.selected_date is None:
            messagebox.showwarning("No Date Selected", "Please select a date first.")
            return
        
        # Open reminder dialog
        dialog = ReminderDialog(self, self.selected_date)
        self.wait_window(dialog)
        
        if dialog.reminder:
            self.db.add_reminder(dialog.reminder)
            messagebox.showinfo("Success", "Reminder added successfully!")
            self.load_reminders_for_date(self.selected_date)
            self.render_calendar()
    
    def edit_reminder(self):
        """Edit selected reminder."""
        selection = self.reminders_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a reminder to edit.")
            return
        
        if not hasattr(self, 'current_reminders') or not self.current_reminders:
            return
        
        index = selection[0]
        reminder = self.current_reminders[index]
        
        # Open reminder dialog with existing data
        dialog = ReminderDialog(self, reminder.date, reminder)
        self.wait_window(dialog)
        
        if dialog.reminder:
            self.db.update_reminder(dialog.reminder)
            messagebox.showinfo("Success", "Reminder updated successfully!")
            self.load_reminders_for_date(self.selected_date)
            self.render_calendar()
    
    def delete_reminder(self):
        """Delete selected reminder."""
        selection = self.reminders_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a reminder to delete.")
            return
        
        if not hasattr(self, 'current_reminders') or not self.current_reminders:
            return
        
        index = selection[0]
        reminder = self.current_reminders[index]
        
        if messagebox.askyesno("Confirm Delete", f"Delete reminder: {reminder.title}?"):
            self.db.delete_reminder(reminder.id)
            messagebox.showinfo("Success", "Reminder deleted successfully!")
            self.load_reminders_for_date(self.selected_date)
            self.render_calendar()
    
    def previous_month(self):
        """Navigate to previous month."""
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.render_calendar()
    
    def next_month(self):
        """Navigate to next month."""
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.render_calendar()
    
    def go_to_today(self):
        """Navigate to current month."""
        today = datetime.now()
        self.current_year = today.year
        self.current_month = today.month
        self.render_calendar()
    
    def _bind_events(self):
        """Bind keyboard events."""
        self.bind('<Left>', lambda e: self.previous_month())
        self.bind('<Right>', lambda e: self.next_month())
        self.bind('<Home>', lambda e: self.go_to_today())


class ReminderDialog(tk.Toplevel):
    """Dialog for creating/editing reminders."""
    
    def __init__(self, parent, date: str, reminder: Optional[Reminder] = None):
        """Initialize the reminder dialog.
        
        Args:
            parent: Parent window
            date: Date for the reminder (YYYY-MM-DD)
            reminder: Existing reminder to edit (optional)
        """
        super().__init__(parent)
        
        self.title("Edit Reminder" if reminder else "Add Reminder")
        self.geometry("400x350")
        self.resizable(False, False)
        
        self.date = date
        self.reminder = None
        
        # Configure style
        self.configure(bg=COLORS['bg_main'])
        
        # Create UI
        self._create_ui(reminder)
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        self.focus_set()
    
    def _create_ui(self, reminder: Optional[Reminder]):
        """Create the dialog UI."""
        # Date label
        date_obj = datetime.strptime(self.date, "%Y-%m-%d")
        date_str = date_obj.strftime("%A, %B %d, %Y")
        
        tk.Label(
            self, text=f"Date: {date_str}", font=("Arial", 11, "bold"),
            bg=COLORS['bg_main'], fg=COLORS['text_main']
        ).pack(pady=10)
        
        # Form frame
        form_frame = tk.Frame(self, bg=COLORS['bg_main'])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Title
        tk.Label(
            form_frame, text="Title:", bg=COLORS['bg_main'], fg=COLORS['text_main']
        ).pack(anchor=tk.W)
        
        self.title_var = tk.StringVar(value=reminder.title if reminder else "")
        title_entry = tk.Entry(form_frame, textvariable=self.title_var, width=40)
        title_entry.pack(fill=tk.X, pady=(0, 10))
        title_entry.focus()
        
        # Time
        tk.Label(
            form_frame, text="Time (HH:MM):", bg=COLORS['bg_main'], fg=COLORS['text_main']
        ).pack(anchor=tk.W)
        
        self.time_var = tk.StringVar(
            value=reminder.time if reminder else DEFAULT_REMINDER_TIME
        )
        time_entry = tk.Entry(form_frame, textvariable=self.time_var, width=40)
        time_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Description
        tk.Label(
            form_frame, text="Description:", bg=COLORS['bg_main'], fg=COLORS['text_main']
        ).pack(anchor=tk.W)
        
        self.desc_text = tk.Text(form_frame, width=40, height=5)
        self.desc_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        if reminder:
            self.desc_text.insert("1.0", reminder.description)
        
        # Status (only for editing)
        if reminder:
            tk.Label(
                form_frame, text="Status:", bg=COLORS['bg_main'], fg=COLORS['text_main']
            ).pack(anchor=tk.W)
            
            self.status_var = tk.StringVar(value=reminder.status)
            status_combo = ttk.Combobox(
                form_frame, textvariable=self.status_var,
                values=["Pending", "Completed", "Cancelled"],
                state="readonly", width=37
            )
            status_combo.pack(fill=tk.X, pady=(0, 10))
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg=COLORS['bg_main'])
        button_frame.pack(fill=tk.X, pady=10)
        
        save_btn = tk.Button(
            button_frame, text="Save", command=self.save_reminder,
            bg=COLORS['bg_button'], fg=COLORS['text_button'],
            relief=tk.RAISED, cursor="hand2", width=15
        )
        save_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(
            button_frame, text="Cancel", command=self.cancel,
            bg=COLORS['bg_button'], fg=COLORS['text_button'],
            relief=tk.RAISED, cursor="hand2", width=15
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def save_reminder(self):
        """Save the reminder."""
        # Validate input
        title = self.title_var.get().strip()
        time = self.time_var.get().strip()
        
        if not title:
            messagebox.showerror("Validation Error", "Please enter a title.")
            return
        
        # Validate time format
        try:
            datetime.strptime(time, "%H:%M")
        except ValueError:
            messagebox.showerror("Validation Error", "Please enter time in HH:MM format.")
            return
        
        description = self.desc_text.get("1.0", tk.END).strip()
        
        # Create reminder
        self.reminder = Reminder(
            title=title,
            date=self.date,
            time=time,
            description=description,
            status=getattr(self, 'status_var', tk.StringVar(value="Pending")).get()
        )
        
        # If editing, preserve ID and timestamps
        if hasattr(self, '_existing_reminder'):
            self.reminder.id = self._existing_reminder.id
            self.reminder.created_at = self._existing_reminder.created_at
        
        self.destroy()
    
    def cancel(self):
        """Cancel the dialog."""
        self.destroy()
