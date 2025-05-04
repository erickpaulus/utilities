# Please make sure you already have these libraries 
# pip install PyPDF2 tkinterdnd2 pyinstaller
# to create exe file
# pyinstaller --onefile --windowed merge2pdfsGUIFlex.py

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
import os
from datetime import datetime

def get_num_pages(path):
    try:
        return len(PdfReader(path).pages)
    except:
        return 0

def parse_range(text, max_pages):
    if text.strip().lower() == 'all':
        return list(range(max_pages))
    result = set()
    for part in text.split(','):
        if '-' in part:
            start, end = map(int, part.strip().split('-'))
            result.update(range(start - 1, end))
        else:
            result.add(int(part.strip()) - 1)
    return sorted([p for p in result if 0 <= p < max_pages])

class PDFToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Tool: Gabung, Sisip, Hapus")
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self.merge_tab = ttk.Frame(self.notebook)
        self.insert_tab = ttk.Frame(self.notebook)
        self.delete_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.merge_tab, text="Gabung")
        self.notebook.add(self.insert_tab, text="Sisip")
        self.notebook.add(self.delete_tab, text="Hapus")

        self.setup_merge_tab()
        self.setup_insert_tab()
        self.setup_delete_tab()

    # ---------------- GABUNG ----------------
    def setup_merge_tab(self):
        self.merge_files = []
        frame = ttk.Frame(self.merge_tab)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.merge_listbox = tk.Listbox(frame, height=8)
        self.merge_listbox.pack(fill="x")

        btns = ttk.Frame(frame)
        btns.pack(fill="x", pady=5)
        ttk.Button(btns, text="Tambah File", command=self.add_merge_files).pack(side="left")
        ttk.Button(btns, text="Hapus", command=self.remove_merge_file).pack(side="left")

        ttk.Button(frame, text="Gabungkan", command=self.merge_pdfs).pack(pady=5)


    def add_merge_files(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        for f in files:
            if f not in self.merge_files:
                self.merge_files.append(f)
                self.merge_listbox.insert("end", f"{os.path.basename(f)} ({get_num_pages(f)} halaman)")

    def remove_merge_file(self):
        idx = self.merge_listbox.curselection()
        for i in reversed(idx):
            self.merge_listbox.delete(i)
            del self.merge_files[i]

    def merge_pdfs(self):
        from PyPDF2 import PdfMerger
        merger = PdfMerger()

        for pdf_file in self.merge_files:
            merger.append(pdf_file)

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if output_path:
            merger.write(output_path)
            merger.close()
            messagebox.showinfo("Sukses", "PDF berhasil digabungkan!")


    # ---------------- SISIP ----------------
    def setup_insert_tab(self):
        frame = ttk.Frame(self.insert_tab)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(frame, text="File Target").pack(anchor="w")
        self.insert_target_path = tk.Entry(frame, width=60)
        self.insert_target_path.pack()
        ttk.Button(frame, text="Pilih", command=self.select_insert_target).pack()

        ttk.Label(frame, text="File Sumber").pack(anchor="w")
        self.insert_source_path = tk.Entry(frame, width=60)
        self.insert_source_path.pack()
        ttk.Button(frame, text="Pilih", command=self.select_insert_source).pack()

        ttk.Label(frame, text="Halaman dari sumber (mis. 1,3-4)").pack(anchor="w")
        self.insert_page_entry = tk.Entry(frame, width=30)
        self.insert_page_entry.insert(0, "all")
        self.insert_page_entry.pack()

        ttk.Label(frame, text="Sisipkan setelah halaman ke (misal: 3, 0 untuk awal)").pack(anchor="w")
        self.insert_pos_entry = tk.Entry(frame, width=10)
        self.insert_pos_entry.insert(0, "0")
        self.insert_pos_entry.pack()

        ttk.Button(frame, text="Sisipkan dan Simpan", command=self.insert_pages).pack(pady=5)

    def select_insert_target(self):
        f = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if f:
            self.insert_target_path.delete(0, "end")
            self.insert_target_path.insert(0, f)

    def select_insert_source(self):
        f = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if f:
            self.insert_source_path.delete(0, "end")
            self.insert_source_path.insert(0, f)

    def insert_pages(self):
        target = self.insert_target_path.get()
        source = self.insert_source_path.get()
        pages_str = self.insert_page_entry.get().strip()
        try:
            pos = int(self.insert_pos_entry.get())
        except ValueError:
            return messagebox.showerror("Error", "Posisi harus berupa angka.")

        if not os.path.exists(target) or not os.path.exists(source):
            return messagebox.showerror("Error", "File tidak ditemukan.")

        reader_target = PdfReader(target)
        reader_source = PdfReader(source)

        writer = PdfWriter()
        source_pages = parse_range(pages_str, len(reader_source.pages))

        for i, page in enumerate(reader_target.pages):
            if i == pos:
                for p in source_pages:
                    writer.add_page(reader_source.pages[p])
            writer.add_page(page)

        if pos >= len(reader_target.pages):
            for p in source_pages:
                writer.add_page(reader_source.pages[p])

        out = filedialog.asksaveasfilename(defaultextension=".pdf")
        if out:
            with open(out, "wb") as f:
                writer.write(f)
            messagebox.showinfo("Sukses", f"Halaman berhasil disisipkan ke {out}.")

    # ---------------- HAPUS ----------------
    def setup_delete_tab(self):
        frame = ttk.Frame(self.delete_tab)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(frame, text="File PDF").pack(anchor="w")
        self.delete_path = tk.Entry(frame, width=60)
        self.delete_path.pack()
        ttk.Button(frame, text="Pilih File", command=self.select_delete_file).pack()

        ttk.Label(frame, text="Halaman yang ingin dihapus (mis. 1,3-5)").pack(anchor="w")
        self.delete_entry = tk.Entry(frame, width=30)
        self.delete_entry.pack()

        ttk.Button(frame, text="Hapus Halaman dan Simpan", command=self.delete_pages).pack(pady=5)

    def select_delete_file(self):
        f = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if f:
            self.delete_path.delete(0, "end")
            self.delete_path.insert(0, f)

    def delete_pages(self):
        path = self.delete_path.get()
        if not os.path.exists(path):
            return messagebox.showerror("Error", "File tidak ditemukan.")
        try:
            pages_to_remove = parse_range(self.delete_entry.get(), get_num_pages(path))
        except Exception as e:
            return messagebox.showerror("Error", f"Format halaman tidak valid: {e}")

        reader = PdfReader(path)
        writer = PdfWriter()

        for i, page in enumerate(reader.pages):
            if i not in pages_to_remove:
                writer.add_page(page)

        out = filedialog.asksaveasfilename(defaultextension=".pdf")
        if out:
            with open(out, "wb") as f:
                writer.write(f)
            messagebox.showinfo("Sukses", f"Halaman berhasil dihapus dan disimpan ke {out}.")

if __name__ == '__main__':
    root = tk.Tk()
    app = PDFToolApp(root)
    root.mainloop()
