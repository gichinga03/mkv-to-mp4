import os
import ffmpeg
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import shutil
from concurrent.futures import ThreadPoolExecutor
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
        self.executor = ThreadPoolExecutor(max_workers=10)

        # Detect available encoders with a sample file
        sample_file = 'sample.mkv'  # Ensure this file exists in the current directory
        if os.path.exists(sample_file):
            self.nvidia_encoder = self.is_encoder_available('h264_nvenc', sample_file)
            self.intel_encoder = self.is_encoder_available('h264_qsv', sample_file)
        else:
            print("Sample file for encoder check not found. Encoders cannot be detected.")

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

                # Submit each conversion as a separate task, alternating GPUs
                self.converted_files = 0  # Reset progress counter
                for i, mkv_file in enumerate(mkv_files):
                    input_file = os.path.join(folder_path, mkv_file)
                    output_file = os.path.join(output_folder, os.path.splitext(mkv_file)[0] + '.mp4')
                    encoder = self.nvidia_encoder if i % 2 == 0 else self.intel_encoder
                    if encoder:
                        self.executor.submit(self.convert_file, input_file, output_file, encoder)
                    else:
                        self.executor.submit(self.convert_file, input_file, output_file, 'libx264')  # CPU fallback

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

    def convert_file(self, input_file, output_file, encoder):
        """Converts a single file and updates converted file count"""
        if not shutil.which("ffmpeg"):
            messagebox.showerror("Error", "FFmpeg is not installed or not found in PATH.")
            return

        print(f"Starting conversion for {input_file} on encoder {encoder}")  # Debug log
        try:
            ffmpeg.input(input_file).output(output_file, vcodec=encoder).run()
            print(f"Completed conversion for {input_file}")  # Debug log
            self.converted_files += 1
        except ffmpeg.Error as e:
            print(f"Error converting {input_file}: {e}")  # Debug log for errors
            self.progress_label.config(text=f"Error converting {input_file}")

    def is_encoder_available(self, encoder_name, test_file):
        """Check if a specified encoder is available using a real file"""
        try:
            ffmpeg.input(test_file).output('test.mp4', vcodec=encoder_name).run(overwrite_output=True)
            os.remove('test.mp4')  # Clean up test file after check
            return encoder_name
        except ffmpeg.Error:
            print(f"{encoder_name} not available.")
            return None

if __name__ == "__main__":
    root = tk.Tk()
    app = FolderConverter(root)
    root.mainloop()
