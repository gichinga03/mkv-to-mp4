Here's a comprehensive README template for your GitHub repository, covering all key points, usage instructions, and setup details. You'll need to add images or screenshots where noted.

---

# MKV to MP4 Video Converter with Multi-GPU Acceleration

This Python-based video converter converts `.mkv` files to `.mp4` format using FFmpeg and supports multi-threading, as well as hardware acceleration for both NVIDIA and Intel GPUs (or a CPU fallback). It features a simple GUI using Tkinter, making it easy to select folders for batch conversions and monitor progress.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Algorithm](#algorithm)
- [Hardware Acceleration](#hardware-acceleration)
- [Example Outputs](#example-outputs)
- [Troubleshooting](#troubleshooting)

---

## Features
- **Batch Conversion**: Select entire folders to convert all `.mkv` files to `.mp4`.
- **Multi-threading**: Leverages multi-core processors for parallel processing, speeding up the conversion.
- **GPU Acceleration**: Utilizes both NVIDIA (NVENC) and Intel (QSV) hardware acceleration (if available).
- **Progress Tracking**: Displays real-time progress updates in the GUI.
- **Fallback to CPU**: Automatically uses CPU encoding if GPUs are unavailable.

---

## Requirements
1. **FFmpeg**: Install FFmpeg and add it to your system PATH. Download it from [ffmpeg.org](https://ffmpeg.org/download.html).
2. **Python 3.7+**: Ensure Python is installed.
3. **Python Packages**:
   - Install requirements using `pip install -r requirements.txt`.

---

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/gichinga03/mkv-to-mp4-main.git
   cd mkv-to-mp4-main
   ```
2. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv myvenv
   myvenv\Scripts\activate  # Windows
   # or
   source myvenv/bin/activate  # macOS/Linux
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Setup FFmpeg**:
   - Download and install FFmpeg.
   - Add the FFmpeg path to your environment variables for system-wide access.

---

## Usage
1. **Run the Converter**:
   ```bash
   python convertor2.py
   ```
2. **Select Folders**:
   - Click **Browse Folder** in the GUI to choose the input folder with `.mkv` files.
   - Select an output folder where the converted `.mp4` files will be saved.

### Example GUI
(Add your screenshots here to showcase the interface)

![image](https://github.com/user-attachments/assets/98d2874f-7992-4664-a501-ceb42be0c0a7)


## Configuration
### Sample File Requirement
The program requires a sample `.mkv` file named `sample.mkv` in the main directory for detecting GPU encoders. Add this file manually, or update the file path in `convertor2.py` if necessary.

### GPU Utilization
The program alternates conversions between available NVIDIA and Intel GPUs, if detected. This configuration optimizes GPU usage and reduces processing time. If no compatible GPU is available, the program falls back to CPU-based conversion.

### Algorithm
1. **Check Available GPUs**:
   - A sample file (`sample.mkv`) is used to detect encoder support for NVIDIA (h264_nvenc) and Intel (h264_qsv) hardware.
2. **Batch Conversion with Multi-threading**:
   - Converts files in parallel, submitting one conversion per thread up to a maximum of 10 concurrent conversions.
3. **Encoder Assignment**:
   - Assigns NVIDIA or Intel GPU encoding for each file alternatively (or CPU if unavailable).
4. **Progress Monitoring**:
   - Tracks conversion progress and updates the GUI in real time.

---

## Hardware Acceleration
### Supported Encoders
1. **NVIDIA NVENC** (`h264_nvenc`): Uses NVIDIA GPU hardware encoding.
2. **Intel QSV** (`h264_qsv`): Uses Intel Quick Sync Video encoding.
3. **CPU Fallback** (`libx264`): Uses software encoding if no compatible GPU is detected.

Add a sample image showing GPU encoder selection in action here.

---

## Example Outputs
| Input File (.mkv)         | Output File (.mp4)      | Encoder Used      |
|---------------------------|-------------------------|--------------------|
| `input1.mkv`              | `output1.mp4`           | `h264_nvenc`      |
| `input2.mkv`              | `output2.mp4`           | `h264_qsv`        |
| `input3.mkv`              | `output3.mp4`           | `libx264` (CPU)   |

---

## Troubleshooting
1. **Error: Sample File Not Found**:
   - Add a sample `.mkv` file to the directory to enable GPU detection.
2. **FFmpeg Not Found**:
   - Ensure FFmpeg is installed and added to your system PATH.
3. **GPU Encoder Not Available**:
   - Update GPU drivers and confirm your GPU model supports NVENC or QSV.
4. **Program Hangs**:
   - Reduce the number of threads or check your system resources.

---

## Contributing
Feel free to open issues or create pull requests to improve this project. Contributions are welcome!

---

## License
MIT License. See `LICENSE` file for more details.

---
