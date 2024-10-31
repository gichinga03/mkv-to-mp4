import os
import ffmpeg
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import shutil

class FolderConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Video Converter")
        self.root.geometry("500x200")

        self.label = tk.Label(root, text="Select a folder to convert MKV files to MP4")
        self.label.pack(pady=20)

        self.progress_label = tk.Label(root, text="")
        self.progress_label.pack()

        self.progress = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(root, variable=self.progress, maximum=100)
        self.progress_bar.pack(fill=tk.X, padx=20, pady=10)

        self.browse_button = tk.Button(root, text="Browse Folder", command=self.browse_folder)
        self.browse_button.pack()

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            output_folder = filedialog.askdirectory(title="Select Output Folder")
            if output_folder:
                threading.Thread(target=self.convert_folder, args=(folder_path, output_folder)).start()

    def convert_folder(self, input_folder, output_folder):
        if not shutil.which("ffmpeg"):
            messagebox.showerror("Error", "FFmpeg is not installed or not found in PATH.")
            return

        self.progress.set(0)
        self.progress_label.config(text="Conversion started...")
        mkv_files = [f for f in os.listdir(input_folder) if f.endswith('.mkv')]
        total_files = len(mkv_files)

        if total_files == 0:
            messagebox.showinfo("No Files", "No MKV files found in the selected folder.")
            return

        for index, mkv_file in enumerate(mkv_files):
            input_file = os.path.join(input_folder, mkv_file)
            output_file = os.path.join(output_folder, os.path.splitext(mkv_file)[0] + '.mp4')

            try:
                ffmpeg.input(input_file).output(output_file).run()
                self.progress.set((index + 1) / total_files * 100)
                self.progress_label.config(text=f"Converting {index + 1}/{total_files}: {mkv_file}")
            except ffmpeg.Error as e:
                self.progress_label.config(text=f"Error occurred: {e}")
                messagebox.showerror("Error", f"Error occurred: {e}")
                return

        self.progress_label.config(text="Conversion completed successfully!")
        messagebox.showinfo("Success", "All files converted successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = FolderConverter(root)
    root.mainloop()
