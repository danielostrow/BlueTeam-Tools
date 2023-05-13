import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import hashlib
import subprocess

def check_sigtool():
    try:
        # Attempt to run sigtool to see if it is installed
        subprocess.run(['sigtool', '-h'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("sigtool is already installed.")
    except FileNotFoundError:
        # If sigtool is not found, prompt the user to install it
        response = tk.messagebox.askquestion("Sigtool not found", "Sigtool is not installed. Would you like to install it now?")
        if response == 'yes':
            try:
                # Attempt to install sigtool using apt-get
                subprocess.run(['sudo', 'apt-get', 'install', 'clamav'], check=True)
                print("sigtool has been installed.")
            except subprocess.CalledProcessError:
                print("An error occurred while installing sigtool. Please check the console for more information.")

check_sigtool()

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
root.title("Import Dialog")

# Create the label for displaying critical files
label = tk.Label(root, text="Known Malware (critical file):")
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
dictionary_text = tk.Text(root, height=10, width=100)
dictionary_text.pack()

# Define the function for generating the signature and displaying the dictionary
def generate_signature():
    CRITICAL_FILE_PATHS = list(CRITICAL_FILES.keys())
    CRITICAL_FILE_PATHS.sort()
    md5_hash = hashlib.md5(repr(CRITICAL_FILES).encode()).hexdigest()
    clamav_signatures = []
    for file_path in CRITICAL_FILE_PATHS:
        clamav_signature = subprocess.check_output(["sigtool", "--md5", file_path]).decode().strip()
        clamav_signatures.append(clamav_signature)
    clamav_signature_text = "\n".join(clamav_signatures)
    dictionary_text.delete("1.0", tk.END)
    # dictionary_text.insert(tk.END, f"{md5_hash}\n")
    dictionary_text.insert(tk.END, clamav_signature_text)
    dictionary_text.insert(tk.END, "\n\n")


# Create the button for confirming files to generate dictionary
confirm_button = tk.Button(root, text="Generate MD5 Signature", command=generate_signature)
confirm_button.pack()

# Start the GUI main loop
root.mainloop()
