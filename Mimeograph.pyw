import shutil
import subprocess
import tempfile
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import whisper
import yt_dlp
import re
import random
import time
import os

from google import genai
from pytube import Search
from threading import Thread

os.makedirs("Output", exist_ok=True)

file = open("key.txt", "r")
KEY_FILE = file.readlines()
KEY = (KEY_FILE[0])

# yt_dlp config
ydl_opts = {
    'format': 'bestaudio/best',
    'headers': {
        'User-Agent': 'Mozilla/5.0',
        'Accept-Language': 'en-US,en;q=0.9',
        'X-Forwarded-For': f'ABC{random.getrandbits(50)}'
    },
}

local_audio_file = None  # Global flag for local file usage


# Core logic functions
def get_video_url(user_input):
    update_status("🔍 Searching YouTube...")
    if user_input.startswith("https://www.youtube.com/watch?v="):
        return user_input
    else:
        search = Search(user_input)
        first_result = search.results[0]
        return first_result.watch_url


def download_audio(url):
    update_status("⬇️ Downloading audio...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)


def transcribe_file(file_path):
    update_status("🧠 Transcribing audio...")
    model = whisper.load_model("small")
    try:
        result = model.transcribe(file_path)
    except UserWarning:
        result = model.transcribe(file_path, fp16=False)
    text = result["text"]
    return ".\n".join(text.split(". "))


def clean_filename(raw):
    cleaned = re.sub(r'\[.*?]', '', raw)
    return os.path.splitext(os.path.basename(cleaned))[0]


def write_to_file(transcription, file_base, fmt):
    update_status("💾 Saving file...")
    path = f"Output/{file_base}{fmt}"
    with open(path, "w", encoding="utf-8") as f:
        f.write(transcription)
    return path


def delete_file(path):
    if local_audio_file:
        return  # Don't delete user's local file
    update_status("🧹 Cleaning up...")
    time.sleep(1)
    if os.path.exists(path):
        try:
            os.remove(path)
        except PermissionError:
            print("Permission error while deleting file.")


def update_status(message):
    status_label.config(text=message)
    status_label.update_idletasks()


def update_progress(value):
    progress['value'] = value
    progress.update_idletasks()


def select_audio_file():
    global local_audio_file
    file_path = filedialog.askopenfilename(filetypes=[
        ("Audio Files", "*.mp3 *.mp4 *.m4a *.wav *.webm *.ogg"),
        ("All Files", "*.*")
    ])
    if file_path:
        local_audio_file = file_path
        url_entry.delete(0, tk.END)
        url_entry.insert(0, "[Local file selected]")
        update_status(f"📁 Selected: {os.path.basename(file_path)}")


def run_in_thread():
    Thread(target=run_transcription).start()


def run_transcription():
    global local_audio_file

    url_or_search = url_entry.get()
    fmt = format_choice.get()

    try:
        update_progress(0)
        update_status("🚀 Starting...")

        if local_audio_file:
            file_path = local_audio_file
            update_progress(20)
        else:
            if not url_or_search or url_or_search == "[Local file selected]":
                messagebox.showerror("Error", "Please enter a YouTube URL, search term, or choose a local file.")
                return

            url = get_video_url(url_or_search)
            update_progress(20)

            file_path = download_audio(url)
            update_progress(50)

        base_name = clean_filename(file_path)
        transcript = transcribe_file(file_path)
        update_progress(75)

        if transcribe_to_latex_var.get():
            transcribe_to_latex(transcript)
            update_progress(90)
            delete_file(file_path)
            update_progress(100)
            update_status("✅ Done.")
            messagebox.showinfo("Success", f"Saved to: Output/Latex.pdf")
            local_audio_file = None
            url_entry.delete(0, tk.END)
        else:
            output_path = write_to_file(transcript, base_name, fmt)
            update_progress(90)
            delete_file(file_path)
            update_progress(100)
            update_status("✅ Done.")
            messagebox.showinfo("Success", f"Saved to:\n{output_path}")
            local_audio_file = None
            url_entry.delete(0, tk.END)

    except Exception as e:
        update_status("❌ Error occurred.")
        messagebox.showerror("Error", str(e))
        update_progress(0)

# ===== LATEX FUNCTIONALITY =====
def wrap_latex_document(body):
    return f"""
\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\begin{{document}}
{body}
\\end{{document}}
""".strip()

def transcribe_to_latex(transcription):
    client = genai.Client(api_key=KEY)
    prompt = (f"translate the following transcript to LaTeX: '{transcription}'")

    response = client.models.generate_content(model="gemini-2.5-flash-preview-04-17", contents=prompt)
    response_text = response.text.strip()


    full_latex = wrap_latex_document(response_text)
    latex_code_to_pdf(full_latex, f"Output/Latex.pdf")


def latex_code_to_pdf(latex_code: str, output_pdf_path: str):

    tex_file = ("temp.tex")

    # Write LaTeX content
    with open(tex_file, "w", encoding="utf-8") as f:
        f.write(latex_code)

    # Run pdflatex from the temporary directory
    try:
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode"],
            check=True,  # Raise exception on error
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )


    except subprocess.CalledProcessError as e:
        print(f"LaTeX compilation failed: {e.stderr.decode()}")
        raise
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        raise



# ===== GUI SETUP =====

root = tk.Tk()
root.title("Atomic Mimeograph")
root.geometry("600x400")
root.configure(bg="#ffffff")
root.resizable(False, False)

try:
    root.iconbitmap("icon.ico")
except:
    print("No icon found, skipping.")

transcribe_to_latex_var = tk.BooleanVar()

style = ttk.Style()
style.theme_use("default")
style.configure("TLabel", background="#ffffff", font=("Segoe UI", 11))
style.configure("TButton", font=("Segoe UI", 11), padding=6)
style.configure("TCombobox", padding=4)
style.configure("Horizontal.TProgressbar", thickness=12, troughcolor="#eee", background="#4a90e2")

tk.Label(root, text="Mimeograph", font=("Segoe UI", 16, "bold"), bg="#ffffff").pack(pady=(20, 10))

form_frame = tk.Frame(root, bg="#ffffff")
form_frame.pack(pady=5)

tk.Label(form_frame, text="YouTube URL or Video Title:", bg="#ffffff").grid(row=0, column=0, sticky="w", padx=5, pady=(0, 5))
url_entry = ttk.Entry(form_frame, width=55)
url_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=(0, 10))

upload_btn = ttk.Button(form_frame, text="📁 Upload Audio File", command=select_audio_file)
upload_btn.grid(row=1, column=2, padx=10, pady=(0, 10))

tk.Label(form_frame, text="Choose output format:", bg="#ffffff").grid(row=2, column=0, sticky="w", padx=5)
format_choice = ttk.Combobox(form_frame, values=[".txt", ".rtf"], state="readonly", width=10)
format_choice.current(0)
format_choice.grid(row=2, column=1, sticky="w", pady=(0, 15))

latex_checkbox = ttk.Checkbutton(
    form_frame,
    text="Transcribe to LaTeX",
    variable=transcribe_to_latex_var
)
latex_checkbox.grid(row=3, column=0, columnspan=2, sticky="w", padx=5, pady=(0, 10))

start_button = ttk.Button(root, text="▶ Start Transcription", command=run_in_thread)
start_button.pack(pady=10)

progress = ttk.Progressbar(root, orient="horizontal", length=480, mode="determinate")
progress.pack(pady=10)

status_label = tk.Label(root, text="Idle", bg="#ffffff", font=("Segoe UI", 10))
status_label.pack(pady=(5, 10))

root.mainloop()