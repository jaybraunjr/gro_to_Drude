import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from grocharmm.gro_to_crd import CRDeditor
from grocharmm.gro_to_psf import PSFeditor

class EditorGUI:
    def __init__(self, root):
        self.root = root
        root.title("CHARMM File Editor")

        self.mode = tk.StringVar(value="crd")

        # --- File selectors
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()

        tk.Label(root, text="Input file").grid(row=0, column=0)
        tk.Entry(root, textvariable=self.input_path, width=40).grid(row=0, column=1)
        tk.Button(root, text="Browse", command=self.select_input).grid(row=0, column=2)

        tk.Label(root, text="Output file").grid(row=1, column=0)
        tk.Entry(root, textvariable=self.output_path, width=40).grid(row=1, column=1)
        tk.Button(root, text="Browse", command=self.select_output).grid(row=1, column=2)

        # --- Mode
        tk.Label(root, text="Mode").grid(row=2, column=0)
        tk.Radiobutton(root, text="CRD", variable=self.mode, value="crd").grid(row=2, column=1, sticky="w")
        tk.Radiobutton(root, text="PSF", variable=self.mode, value="psf").grid(row=2, column=1)

        # --- Options
        self.replace_resnames = tk.BooleanVar()
        tk.Checkbutton(root, text="Replace resnames (CRD only)", variable=self.replace_resnames).grid(row=3, columnspan=2)

        # --- Run button
        tk.Button(root, text="Run", command=self.run_editor).grid(row=4, column=1)

    def select_input(self):
        path = filedialog.askopenfilename()
        if path:
            self.input_path.set(path)

    def select_output(self):
        path = filedialog.asksaveasfilename(defaultextension=".crd")
        if path:
            self.output_path.set(path)

    def run_editor(self):
        input_path = self.input_path.get()
        output_path = self.output_path.get()

        if not input_path or not output_path:
            messagebox.showerror("Missing file paths", "Please select both input and output files.")
            return

        try:
            if self.mode.get() == "crd":
                editor = CRDeditor(input_path)
                editor.read()
                if self.replace_resnames.get():
                    editor.replace_resnames()
                editor.update_segments()
                editor.update_segment_numbers()
                editor.write(output_path)
            else:
                editor = PSFeditor(input_path)
                editor.read_lines()
                editor.update_psf_segments()
                editor.update_psf_resids()
                editor.write_lines(output_path)

            messagebox.showinfo("Success", f"File saved to:\n{output_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    gui = EditorGUI(root)
    root.mainloop()
