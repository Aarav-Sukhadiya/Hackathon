import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import json, tempfile, os

# 👇 import your processing functions from main.py
from main import process_media, process_json  # uses your existing pipeline
# process_media/process_json definitions live here: see main.py.  # (for reference)

root = tk.Tk()
root.title("Intelligent Storage System")
root.geometry("700x560")

media_frame = tk.Frame(root, pady=10)
media_frame.pack()

json_frame = tk.Frame(root, pady=10)
json_frame.pack()

tk.Label(media_frame, text="Media File Uploader", font=("Arial", 14)).pack()

def upload_media_files():
    filenames = filedialog.askopenfilenames(
        title="Select Media Files",
        filetypes=(
            ("Media Files", "*.png *.jpg *.jpeg *.bmp *.gif *.webp *.tif *.tiff *.mp4 *.mov *.avi *.mkv *.heic *.avif"),
            ("All Files", "*.*")
        )
    )
    if not filenames:
        return
    try:
        # 🚀 Run your pipeline on the selected media files
        process_media(list(filenames))
        messagebox.showinfo("Done", f"Processed {len(filenames)} media file(s). Check output folders.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process media: {e}")

upload_button = tk.Button(media_frame, text="Select Media Files...", command=upload_media_files)
upload_button.pack()

tk.Label(json_frame, text="Structured Data (JSON)", font=("Arial", 14)).pack()
tk.Label(json_frame, text="Paste your JSON data or upload file(s):").pack()

json_input = scrolledtext.ScrolledText(json_frame, height=12, width=70)
json_input.pack()

def upload_json_file():
    filenames = filedialog.askopenfilenames(
        title="Select JSON File(s)",
        filetypes=(("JSON Files", "*.json *.jsonl *.ndjson"), ("All Files", "*.*"))
    )
    if not filenames:
        return

    # Option 1 (keep your preview): read & show combined in the textbox
    all_json_data = []
    try:
        for file in filenames:
            with open(file, "r", encoding="utf-8") as f:
                txt = f.read().strip()
            # try parse—if JSONL, just show raw text in the box
            try:
                data = json.loads(txt)
                all_json_data.append(data)
            except json.JSONDecodeError:
                all_json_data.append(txt)  # show as-is for NDJSON preview

        json_input.delete("1.0", tk.END)
        try:
            json_input.insert("1.0", json.dumps(all_json_data, indent=2, ensure_ascii=False))
        except TypeError:
            # mixed raw text + objects: just join for preview
            json_input.insert("1.0", "\n\n".join(map(str, all_json_data)))
        messagebox.showinfo("Loaded", f"Loaded {len(filenames)} JSON file(s).")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file(s): {e}")

tk.Label(json_frame, text="Optional comments:").pack()
comments_input = tk.Entry(json_frame, width=80)
comments_input.pack(pady=5)

json_button_frame = tk.Frame(json_frame)
json_button_frame.pack()

def submit_json_data():
    json_text = json_input.get("1.0", tk.END).strip()
    comments = comments_input.get().strip()

    # If user pasted JSON, write to a temp file and process
    if json_text:
        # validate basic JSON or allow NDJSON
        is_valid_json = True
        try:
            json.loads(json_text)
        except json.JSONDecodeError:
            is_valid_json = False  # might be NDJSON; we’ll still pass to pipeline

        try:
            with tempfile.NamedTemporaryFile(prefix="ui_json_", suffix=".json", delete=False, mode="w", encoding="utf-8") as tf:
                tf.write(json_text)
                tmp_path = tf.name
            meta = {"comment": comments} if comments else None
            process_json([tmp_path], metadata=meta)  # 🔗 hands off to your pipeline
            messagebox.showinfo("Done", "Pasted JSON processed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process pasted JSON: {e}")
        finally:
            # keep temp for audit; uncomment next line to auto-delete
            # try: os.remove(tmp_path) except: pass
            pass
        return

    messagebox.showwarning("Empty", "Paste JSON text or use 'Upload .json File' first.")

upload_file_btn = tk.Button(json_button_frame, text="Upload .json File(s)", command=upload_json_file)
upload_file_btn.pack(side=tk.LEFT, padx=5)

submit_text_btn = tk.Button(json_button_frame, text="Process Pasted JSON", command=submit_json_data)
submit_text_btn.pack(side=tk.LEFT, padx=5)

root.mainloop()
