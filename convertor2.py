import os
import ffmpeg
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

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

        self.total_files = 0
        self.converted_files = 0
        self.executor = ThreadPoolExecutor(max_workers=5)  # Limits threads to avoid overload

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            output_folder = filedialog.askdirectory(title="Select Output Folder")
            if output_folder:
                mkv_files = [f for f in os.listdir(folder_path) if f.endswith('.mkv')]
                self.total_files = len(mkv_files)
                if not mkv_files:
                    messagebox.showinfo("No Files", "No MKV files found in the selected folder.")
                    return

                # Submit each conversion as a separate task
                self.converted_files = 0  # Reset progress counter
                for mkv_file in mkv_files:
                    input_file = os.path.join(folder_path, mkv_file)
                    output_file = os.path.join(output_folder, os.path.splitext(mkv_file)[0] + '.mp4')
                    self.executor.submit(self.convert_file, input_file, output_file)

                # Schedule progress updates
                self.update_progress()

    def update_progress(self):
        """Update the progress bar and label in the GUI"""
        if self.converted_files < self.total_files:
            self.progress.set((self.converted_files / self.total_files) * 100)
            self.progress_label.config(text=f"Converted {self.converted_files}/{self.total_files} files")
            self.root.after(500, self.update_progress)  # Check every 500ms
        else:
            messagebox.showinfo("Success", "All files converted successfully!")

    def convert_file(self, input_file, output_file):
        """Converts a single file and updates converted file count"""
        if not shutil.which("ffmpeg"):
            messagebox.showerror("Error", "FFmpeg is not installed or not found in PATH.")
            return

        print(f"Starting conversion for {input_file}")  # Debug log
        try:
            # GPU-accelerated conversion
            ffmpeg.input(input_file).output(output_file, vcodec='h264_nvenc').run()
            print(f"Completed conversion for {input_file}")  # Debug log
            self.converted_files += 1
        except ffmpeg.Error as e:
            print(f"Error converting {input_file}: {e}")  # Debug log for errors
            self.progress_label.config(text=f"Error converting {input_file}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FolderConverter(root)
    root.mainloop()
