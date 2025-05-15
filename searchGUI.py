import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class SearchingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Find keyword")
        self.geometry("900x600")

        self.create_widgets()

    def create_widgets(self):
        # Layout: Paned window
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)

        # Left panel: Folder Tree
        self.tree_frame = ttk.Frame(paned, width=250)
        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewOpen>>", self.expand_tree)
        paned.add(self.tree_frame)

        # Right panel
        right_frame = ttk.Frame(paned)
        paned.add(right_frame)

        # Top: Search bar
        top_frame = ttk.Frame(right_frame)
        top_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(top_frame, text="Keywords:").pack(side=tk.LEFT)
        self.keyword_entry = ttk.Entry(top_frame, width=50)
        self.keyword_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Search", command=self.search_keywords).pack(side=tk.LEFT)

        # Results area
        self.result_box = tk.Listbox(right_frame)
        self.result_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.result_box.bind('<Double-1>', self.on_result_double_click)

        # Menu
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open Folder", command=self.choose_folder)
        menubar.add_cascade(label="File", menu=file_menu)

    def choose_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.root_path = path
            self.tree.delete(*self.tree.get_children())
            self.insert_tree_items('', path)

    def insert_tree_items(self, parent, path):
        try:
            for item in os.listdir(path):
                abs_path = os.path.join(path, item)
                node = self.tree.insert(parent, 'end', text=item, values=[abs_path])
                if os.path.isdir(abs_path):
                    self.tree.insert(node, 'end')  # Add dummy child
        except PermissionError:
            pass

    def expand_tree(self, event):
        node = self.tree.focus()
        abs_path = self.tree.item(node, 'values')[0]
        if os.path.isdir(abs_path):
            self.tree.delete(*self.tree.get_children(node))
            self.insert_tree_items(node, abs_path)

    def search_keywords(self):
        keywords = self.keyword_entry.get().split(',')
        keywords = [k.strip() for k in keywords if k.strip()]
        if not hasattr(self, 'root_path') or not keywords:
            messagebox.showwarning("Input", "Select a folder and enter keywords.")
            return

        self.result_box.delete(0, tk.END)
        for root, _, files in os.walk(self.root_path):
            for file in files:
                if file.endswith(('.txt', '.py', '.log', '.md')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()
                            for i, line in enumerate(lines, 1):
                                if any(k.lower() in line.lower() for k in keywords):
                                    display = f"{file_path} | Line {i}: {line.strip()}"
                                    self.result_box.insert(tk.END, display)
                    except Exception as e:
                        self.result_box.insert(tk.END, f"Error reading {file}: {e}")

    def on_result_double_click(self, event):
        selection = self.result_box.get(self.result_box.curselection())
        if "|" in selection:
            filepath = selection.split('|')[0].strip()
            os.system(f'notepad "{filepath}"')  # Or use a code editor

if __name__ == "__main__":
    app = SearchingApp()
    app.mainloop()
