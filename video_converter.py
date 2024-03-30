import os
import tkinter as tk
from tkinter import filedialog
import subprocess
from tqdm import tqdm

def select_input_file():
    input_file = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.mkv *.avi *.ts")])
    input_entry.delete(0, tk.END)
    input_entry.insert(0, input_file)

def select_output_directory():
    output_dir = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_dir)

def convert_video():
    input_file = input_entry.get()
    output_dir = output_entry.get()

    if not input_file or not output_dir:
        status_label.config(text="Please select input file and output directory.")
        return

    output_file = os.path.join(output_dir, "output.mp4")

    try:
        cmd = f"ffmpeg -i {input_file} -c:v libx265 -c:a copy -threads 0 {output_file}"
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

        
        total_duration = get_video_duration(input_file)
        with tqdm(total=total_duration, unit="s", desc="Converting") as pbar:
            for line in process.stdout:
                if "time=" in line:
                    time_str = line.split("time=")[1].split()[0]
                    current_time = parse_time(time_str)
                    pbar.update(current_time - pbar.n)

        status_label.config(text="Conversion completed successfully!")
    except subprocess.CalledProcessError:
        status_label.config(text="Error during conversion. Check input file and output directory.")

def get_video_duration(video_file):
    cmd = f"ffprobe -i {video_file} -show_entries format=duration -v quiet -of csv=p=0"
    try:
        duration_str = subprocess.check_output(cmd, shell=True, universal_newlines=True).strip()
        return float(duration_str)
    except subprocess.CalledProcessError as e:

        print("Error:", e)
        return 0
    except ValueError as e:
        print("Error parsing duration:", e)
        return 0


def parse_time(time_str):
    if time_str == "N/A":
        return 0
    h, m, s = map(float, time_str.split(":"))
    return h * 3600 + m * 60 + s

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Video Converter")

    input_label = tk.Label(root, text="Select Input Video:")
    input_entry = tk.Entry(root, width=40)
    input_button = tk.Button(root, text="Browse", command=select_input_file)

    output_label = tk.Label(root, text="Select Output Directory:")
    output_entry = tk.Entry(root, width=40)
    output_button = tk.Button(root, text="Browse", command=select_output_directory)

    convert_button = tk.Button(root, text="Convert", command=convert_video)
    status_label = tk.Label(root, text="")

    input_label.pack()
    input_entry.pack()
    input_button.pack()

    output_label.pack()
    output_entry.pack()
    output_button.pack()

    convert_button.pack()
    status_label.pack()

    root.mainloop()

