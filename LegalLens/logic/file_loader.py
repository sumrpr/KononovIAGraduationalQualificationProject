import docx
import pdfplumber
import tkinter as tk
from tkinter import filedialog

paragraphs = []

def open_file_dialog():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Supported Files", "*.txt *.docx *.pdf")])
    return file_path

def load_file(filepath):
    global paragraphs
    ext = filepath.split(".")[-1].lower()
    text = ""
    try:
        if ext == "txt":
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
        elif ext == "docx":
            doc = docx.Document(filepath)
            text = "\n\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        elif ext == "pdf":
            with pdfplumber.open(filepath) as pdf:
                pages = [page.extract_text() or "" for page in pdf.pages]
                text = "\n\n".join(p.strip() for p in pages if p.strip())
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
        text = ""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

def reset_state_para():
    global paragraphs
    paragraphs = []

def get_paragraphs():
    return paragraphs

def reset_paragraphs():
    global paragraphs
    paragraphs = []