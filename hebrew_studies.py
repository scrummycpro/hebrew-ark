import tkinter as tk
from tkinter import messagebox, Menu, filedialog
import sqlite3
from datetime import datetime
import subprocess
import json

def save_to_database(timestamp, hebrew_topic, calendar_data):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('hebrew_studies.db')
        cursor = conn.cursor()

        # Create a table if not exists
        cursor.execute('''CREATE TABLE IF NOT EXISTS commands (
                            id INTEGER PRIMARY KEY,
                            timestamp TEXT,
                            hebrew_topic TEXT,
                            calendar_data TEXT
                        )''')

        # Insert timestamp, Hebrew topic, and calendar data into the table
        cursor.execute("INSERT INTO commands (timestamp, hebrew_topic, calendar_data) VALUES (?, ?, ?)",
                       (timestamp, hebrew_topic, calendar_data))
        conn.commit()

        # Close the connection
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def execute_command():
    # Define the commands
    hebrew_command = "curl --request GET --url https://www.sefaria.org/api/texts/random-by-topic --header 'accept: application/json'"
    calendar_command = "curl --request GET --url https://www.sefaria.org/api/calendars --header 'accept: application/json'"

    try:
        # Execute the Hebrew topic command
        hebrew_result = subprocess.run(hebrew_command.split(), capture_output=True, text=True)
        hebrew_json_result = json.loads(hebrew_result.stdout)

        # Execute the calendar command
        calendar_result = subprocess.run(calendar_command.split(), capture_output=True, text=True)
        calendar_json_result = json.loads(calendar_result.stdout)

        # Extract data from the results
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        hebrew_topic = hebrew_json_result.get('topic', {}).get('primaryTitle', {}).get('he', 'Unknown')
        calendar_data = json.dumps(calendar_json_result, ensure_ascii=False, indent=4)

        # Save data to the database
        save_to_database(timestamp, hebrew_topic, calendar_data)

        # Display the results
        command_label.config(text="Study This today")
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        decoded_hebrew_result = json.dumps(hebrew_json_result, indent=4, ensure_ascii=False)
        result_text.insert(tk.END, f"Hebrew Topic Data:\n{decoded_hebrew_result}\n\nCalendar Data:\n{calendar_data}")
        result_text.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while executing the commands: {e}")

def save_as_json():
    try:
        result = result_text.get("1.0", tk.END)
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(result)
            messagebox.showinfo("Success", "Command results saved as JSON file.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving JSON file: {e}")

# Create the GUI
root = tk.Tk()
root.title("Hebrew Studies")
root.geometry("800x600")

# Command label
command_label = tk.Label(root, text="Study This today", wraplength=700)
command_label.pack(pady=10)

# Execute button
execute_button = tk.Button(root, text="Execute Command", command=execute_command)
execute_button.pack(pady=5)

# Save as JSON button
save_button = tk.Button(root, text="Save as JSON", command=save_as_json)
save_button.pack(pady=5)

# Result text area with scroll bar
result_frame = tk.Frame(root)
result_frame.pack(pady=5, fill=tk.BOTH, expand=True)

result_text = tk.Text(result_frame, height=20, width=80)
result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(result_frame, command=result_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_text.config(yscrollcommand=scrollbar.set)

# Context menu for result text area (right-click to paste)
context_menu = Menu(result_text, tearoff=0)
context_menu.add_command(label="Paste", command=lambda: result_text.event_generate("<Control-v>"))
result_text.bind("<Button-3>", lambda event: context_menu.post(event.x_root, event.y_root))

root.mainloop()