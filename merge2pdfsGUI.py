# Please make sure you already have these libraries 
# pip install PyPDF2 tkinterdnd2 pyinstaller
# to create exe file
# pyinstaller --onefile --windowed merge2pdfsGUI.py

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PyPDF2 import PdfMerger
import os

def add_files(files):
    for f in files:
        if f.lower().endswith(".pdf") and f not in file_list.get(0, tk.END):
            file_list.insert(tk.END, f)

def select_files():
    files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
    add_files(files)

def on_drop(event):
    files = root.tk.splitlist(event.data)
    add_files(files)

def remove_selected():
    selected = file_list.curselection()
    for i in reversed(selected):
        file_list.delete(i)

def move_up():
    selected = file_list.curselection()
    for i in selected:
        if i > 0:
            text = file_list.get(i)
            file_list.delete(i)
            file_list.insert(i - 1, text)
            file_list.select_set(i - 1)

def move_down():
    selected = file_list.curselection()
    for i in reversed(selected):
        if i < file_list.size() - 1:
            text = file_list.get(i)
            file_list.delete(i)
            file_list.insert(i + 1, text)
            file_list.select_set(i + 1)

def merge_pdfs():
    files = file_list.get(0, tk.END)
    if len(files) < 2:
        messagebox.showwarning("Need more files", "Select at least two PDF files.")
        return

    merger = PdfMerger()
    try:
        for pdf in files:
            merger.append(pdf)

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if output_path:
            merger.write(output_path)
            messagebox.showinfo("Success", f"Merged PDF saved to:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")
    finally:
        merger.close()

# --- GUI Setup ---
root = TkinterDnD.Tk()
root.title("PDF Merger")
root.geometry("500x400")

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add PDFs", command=select_files).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Remove Selected", command=remove_selected).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Move Up", command=move_up).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Move Down", command=move_down).grid(row=0, column=3, padx=5)

file_list = tk.Listbox(root, selectmode=tk.EXTENDED, width=70, height=15)
file_list.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

file_list.drop_target_register(DND_FILES)
file_list.dnd_bind("<<Drop>>", on_drop)

tk.Button(root, text="Merge PDFs", command=merge_pdfs, height=2).pack(pady=10)

root.mainloop()
