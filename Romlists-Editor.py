import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox
from datetime import datetime

def update_clock():
    # Get current date and time
    now = datetime.now()
    
    # Format date and time
    formatted_date = now.strftime("%B %d, %Y")
    formatted_time = now.strftime("%I:%M %p")
    
    # Update label text
    clock_label.config(text=f"{formatted_date} {formatted_time}")
    
    # Call update_clock function after 1000ms (1 second)
    root.after(1000, update_clock)    

FIELD_LABELS = [
    "Name", "Title", "Emulator", "CloneOf", "Year", "Manufacturer", "Category",
    "Players", "Rotation", "Control", "Status", "DisplayCount", "DisplayType",
    "AltRomName", "AltTitle", "Extra", "Buttons", "Series", "Language", "Region", "Rating"
]

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        display_file_content(file_path)
        file_name = file_path.split("/")[-1].split(".")[0]  # Extract file name without extension
        textbox.config(state='normal')  # Enable editing
        textbox.delete(1.0, tk.END)  # Clear previous content
        
        # Calculate padding to center text
        textbox_width = int(textbox.cget("width"))
        text_width = len(file_name)
        padding = " " * ((textbox_width - text_width) // 2)
        
        text = padding + file_name + padding  # Center the text
        textbox.insert(tk.END, text)  # Insert centered file name
        textbox.config(state='disabled')  # Disable editing again


def display_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.readlines()
        text_content.delete(1.0, tk.END)
        for line in content:
            text_content.insert(tk.END, line)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open file: {e}")

def save_file():
    try:
        file_content = text_content.get(1.0, tk.END).strip()
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], parent=root)
        if file_path:
            with open(file_path, 'w') as file:
                file.write(file_content)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file: {e}")

def add_text_to_field_label():
    selected_label = field_label_combobox.get()
    new_text = new_text_entry.get()
    if selected_label and new_text:
        try:
            current_content = text_content.get(1.0, tk.END).split('\n')
            updated_content = []
            for line in current_content:
                if not line.startswith("#"):
                    line_split = line.split(";")
                    updated_line = ";".join([new_text if label == selected_label else value for label, value in zip(FIELD_LABELS, line_split)])
                    updated_content.append(updated_line)
                else:
                    updated_content.append(line)
            updated_text = '\n'.join(updated_content)
            text_content.delete(1.0, tk.END)
            text_content.insert(tk.END, updated_text)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showerror("Error", "Please select a field label and enter new text.")
        
def open_website(url):
    import webbrowser
    webbrowser.open(url)        

def exit_app():
    root.destroy()

root = tk.Tk()
root.title("Attract Mode Romlists Editor")
root.geometry("1600x900")
root.configure(bg="#28282B")

# Open Button
open_button = tk.Button(root, text="Open File", command=open_file)
open_button.pack(pady=10)

# Create a frame
textbox_frame = tk.Frame(root, bg="white", bd=1, relief="ridge")
textbox_frame.pack(pady=5)

# Textbox inside the frame
textbox = tk.Text(textbox_frame, height=1, width=50, bg="#CCCCCC", state='disabled')
textbox.pack(expand=True, fill="both")

# Label for column headers
label_headers = tk.Label(root, text="Romlists")
label_headers.pack(pady=5)

# Create a frame for text content
text_content_frame = tk.Frame(root, bg="white", bd=1, relief="ridge")
text_content_frame.pack(pady=5)

# Text content inside the frame
text_content = tk.Text(text_content_frame, height=30, width=190, bg="#CCCCCC")
text_content.pack(expand=True, fill="both")

# Create buttons For Websites
button_width = 10
button_height = 1

button1 = tk.Button(root, text="PRU Website", command=lambda: open_website("https://free-3980544.webador.com/"), width=button_width, height=button_height)
button1.pack(side=tk.LEFT, padx=(40, 10), pady=(0, 250))  # Add horizontal padding from the left and vertical padding only at the top

button2 = tk.Button(root, text="PRU Discord", command=lambda: open_website("https://discord.gg/V9gStB2"), width=button_width, height=button_height)
button2.pack(side=tk.LEFT, padx=(10, 10), pady=(0, 250))  # Add horizontal padding from the left and vertical padding only at the top

button3 = tk.Button(root, text="Attract Mode", command=lambda: open_website("https://attractmode.org/"), width=button_width, height=button_height)
button3.pack(side=tk.LEFT, padx=(10, 10), pady=(0, 250))  # Add horizontal padding from the left and vertical padding only at the top

button4 = tk.Button(root, text="AM+ Github", command=lambda: open_website("https://github.com/oomek/attractplus"), width=button_width, height=button_height)
button4.pack(side=tk.LEFT, padx=(10, 10), pady=(0, 250))  # Add horizontal padding from the left and vertical padding only at the top

# Combobox
field_label_combobox = Combobox(root, values=FIELD_LABELS)
field_label_combobox.place(relx=0.5, rely=0.5, anchor=tk.W, x=-75, y=165)  # Place the Combobox

# Create a frame for the new text entry
new_text_entry_frame = tk.Frame(root, bg="white", bd=1, relief="ridge")
new_text_entry_frame.place(relx=0.5, rely=0.5, anchor=tk.W, x=-67, y=200)  # Place the frame containing the new text entry below the Combobox

# New text entry inside the frame
new_text_entry = tk.Entry(new_text_entry_frame, bg="#CCCCCC")  # Set background color to light grey
new_text_entry.pack(fill="both", expand=True)

# Add text button
add_text_button = tk.Button(root, text="Add To Column", command=add_text_to_field_label)
add_text_button.place(relx=0.5, rely=0.5, anchor=tk.W, x=-53, y=235)  # Place the add text button below the new text entry

# Save button
save_button = tk.Button(root, text="Save Changes", command=save_file)
save_button.place(relx=0.5, rely=0.5, anchor=tk.W, x=-47, y=270)  # Place the save button below the add text button

# Create the exit button
exit_button = tk.Button(root, text="Exit", command=exit_app)
exit_button.place(relx=1, x=-10, rely=1, y=-10, anchor="se")  # Position in bottom right corner with a margin of 10 pixels

# Create label for clock
clock_label = tk.Label(root, text="", font=("Helvetica", 10), background="#28282B", fg="white")
clock_label.place(relx=1, x=-10, y=10, anchor="ne")  # Position in top right corner with a margin of 10 pixels

# Call update_clock function to update the clock
update_clock()

root.mainloop()
