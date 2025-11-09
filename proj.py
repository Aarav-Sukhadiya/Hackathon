import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import json 

root = tk.Tk()
root.title("Intelligent Storage System")
root.geometry("600x500") 

media_frame = tk.Frame(root, pady=10)
media_frame.pack()

json_frame = tk.Frame(root, pady=10)
json_frame.pack()

tk.Label(media_frame, text="Media File Uploader", font=("Arial", 14)).pack()

def upload_media_files():
    filenames = filedialog.askopenfilenames(
        title="Select Media Files",
        filetypes=(
            ("Media Files", "*.png *.jpg *.jpeg *.mp4 *.mov *.avi"),
            ("All Files", "*.*")
        )
    )
    
    if filenames:
        messagebox.showinfo("Files Selected", f"You selected {len(filenames)} file(s).")
        print(f"Selected files: {filenames}")

upload_button = tk.Button(media_frame, text="Select Media Files...", command=upload_media_files)
upload_button.pack()

tk.Label(json_frame, text="Structured Data (JSON)", font=("Arial", 14)).pack()
tk.Label(json_frame, text="Paste your JSON data or upload a file:").pack()

json_input = scrolledtext.ScrolledText(json_frame, height=10, width=60)
json_input.pack()

def upload_json_file():
    filenames = filedialog.askopenfilenames(
        title="Select a JSON File",
        filetypes=(("JSON Files", "*.json"), ("All Files", "*.*"))
    )
    
    if not filenames: 
        return 
    all_json_data = []

        
    try:
        for file in filenames:
            with open(file, 'r') as f:
                file_content = f.read()
                read_json = json.loads(file_content)
                all_json_data.append(read_json)

        final_json_string = json.dumps(all_json_data, indent = 2)
        json_input.delete("1.0", tk.END) 
        json_input.insert("1.0", final_json_string)
        messagebox.showinfo("File Loaded", f"Successfully loaded and combined {len(filenames)} JSON file(s).")
    except json.JSONDecodeError:
        messagebox.showerror("Error", f"One of the files ({filenames.split('/')[-1]}) is not a valid json.")    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file: {e}")

tk.Label(json_frame, text="Optional comments:").pack()
comments_input = tk.Entry(json_frame, width=70) 
comments_input.pack(pady=5)

json_button_frame = tk.Frame(json_frame)
json_button_frame.pack()

def submit_json_data():

    json_data = json_input.get("1.0", tk.END)
    comments = comments_input.get()
    
    if not json_data.strip():
        messagebox.showwarning("Empty Input", "Please paste or upload your JSON data.")
        return

    try:
        json.loads(json_data)
    except json.JSONDecodeError:
        messagebox.showerror("Invalid JSON", "The text in the box is not valid JSON. Please fix it or upload a valid file.")
        return

    if comments:
        print(f"Submitted comments: {comments}")
    
    print(f"Submitted JSON: {json_data}")
    messagebox.showinfo("JSON Submitted", "Your valid JSON data has been received.")


upload_file_btn = tk.Button(json_button_frame, text="Upload .json File", command=upload_json_file)
upload_file_btn.pack(side=tk.LEFT, padx=5)


submit_text_btn = tk.Button(json_button_frame, text="Submit JSON Text", command=submit_json_data)
submit_text_btn.pack(side=tk.LEFT, padx=5)

root.mainloop()