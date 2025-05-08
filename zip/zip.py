import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import zipfile

class ZipApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Directory Zipper")
        self.selected_dir = tk.StringVar()
        self.check_vars = {}

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        dir_frame = ttk.Frame(frame)
        dir_frame.pack(fill=tk.X, pady=5)

        ttk.Label(dir_frame, text="Directory:").pack(side=tk.LEFT)
        ttk.Entry(dir_frame, textvariable=self.selected_dir, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(dir_frame, text="Browse", command=self.browse_directory).pack(side=tk.LEFT)

        self.items_frame = ttk.LabelFrame(frame, text="Contents")
        self.items_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X)

        ttk.Button(btn_frame, text="Create Zip", command=self.create_zip).pack(side=tk.RIGHT)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.selected_dir.set(directory)
            self.populate_items(directory)

    def populate_items(self, directory):
        for widget in self.items_frame.winfo_children():
            widget.destroy()

        self.check_vars.clear()

        for item in sorted(os.listdir(directory)):
            full_path = os.path.join(directory, item)
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(self.items_frame, text=item, variable=var)
            chk.pack(anchor=tk.W)
            self.check_vars[full_path] = var

    def create_zip(self):
        if not self.selected_dir.get():
            messagebox.showerror("Error", "Please select a directory first.")
            return

        items_to_zip = [path for path, var in self.check_vars.items() if var.get()]

        if not items_to_zip:
            messagebox.showwarning("No Selection", "No items selected to zip.")
            return

        zip_path = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("Zip files", "*.zip")])
        if not zip_path:
            return

        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                base_dir = self.selected_dir.get()
                for path in items_to_zip:
                    if os.path.isdir(path):
                        for root, _, files in os.walk(path):
                            for f in files:
                                abs_path = os.path.join(root, f)
                                rel_path = os.path.relpath(abs_path, base_dir)
                                zipf.write(abs_path, rel_path)
                    else:
                        rel_path = os.path.relpath(path, base_dir)
                        zipf.write(path, rel_path)

            messagebox.showinfo("Success", f"Zip created at:\n{zip_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create zip file:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ZipApp(root)
    root.mainloop()
