import tkinter as tk
import tkinter.filedialog as filedialog
import hashlib


CRITICAL_FILES = {}

def add_critical_file():
    file_paths = filedialog.askopenfilenames()
    for file_path in file_paths:
        if file_path not in CRITICAL_FILES:
            with open(file_path, 'rb') as f:
                file_data = f.read()
                md5_hash = hashlib.md5(file_data).hexdigest()
            CRITICAL_FILES[file_path] = md5_hash
            print(f"Added critical file: ({md5_hash})")
            listbox.insert(tk.END, file_path)

# Create the GUI window
root = tk.Tk()
root.title("Critical File System")

# Create the label for displaying critical files
label = tk.Label(root, text="Critical Files:")
label.pack()

# Create the listbox for displaying critical files
listbox = tk.Listbox(root)
listbox.pack()

for file_path, md5_hash in CRITICAL_FILES.items():
    listbox.insert(tk.END, file_path)

def remove_critical_file():
    selection = listbox.curselection()
    if selection:
        index = selection[0]
        file_path = listbox.get(index)
        listbox.delete(index)
        CRITICAL_FILES.pop(file_path)
        print(f"Removed critical file: {file_path}")

# Create the button for removing a critical file
remove_file_button = tk.Button(root, text="Remove selected file", command=remove_critical_file)
remove_file_button.pack()

# Create the button that triggers the file selection dialog
add_file_button = tk.Button(root, text="Add critical file", command=add_critical_file)
add_file_button.pack()

# Create the text widget for displaying the dictionary
dictionary_text = tk.Text(root, height=10, width=50)
dictionary_text.pack()

# Define the function for generating the signature and displaying the dictionary
def generate_signature():
    CRITICAL_FILE_PATHS = list(CRITICAL_FILES.keys())
    CRITICAL_FILE_PATHS.sort()
    md5_hash = hashlib.md5(repr(CRITICAL_FILES).encode()).hexdigest()
    print(f"Generated signature MD5 hash: {md5_hash}")
    dictionary_text.delete("1.0", tk.END)
    dictionary_text.insert(tk.END, f"<MD5Hash>{md5_hash}\n")
    for file_path in CRITICAL_FILE_PATHS:
        md5_hash = CRITICAL_FILES[file_path]
        dictionary_text.insert(tk.END, f"{md5_hash}\n")
    dictionary_text.insert(tk.END, "</MD5Hash>")

# Create the button for confirming files to generate dictionary
confirm_button = tk.Button(root, text="Confirm", command=generate_signature)
confirm_button.pack()

# Start the GUI main loop
root.mainloop()