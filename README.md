# ft.dk_video
This script allows you to download and concatenate video segments from an M3U8 file, saving them as an MP4 video file. It uses Python for downloading the segments and concatenating them using ffmpeg.

Prerequisites
Before you begin, ensure you have the following installed on your system:

Python 3.x: Make sure Python is installed on your system. You can download it from python.org.
ffmpeg: This is required to concatenate the video segments. You can download ffmpeg from ffmpeg.org.
Installation
Clone the repository to your local machine:

bash
Copy code
git clone https://github.com/fellowjamess/ft.dk_video.git
cd ft.dk_video
Install the required Python packages:

bash
Copy code
pip install -r requirements.txt
Usage
To download a video from an M3U8 URL, follow these steps:

Prepare the M3U8 URL:

Obtain the URL of the M3U8 file you want to download. It should end with .m3u8.

Run the Batch Script:

Double-click on run_download.bat to run it.

Follow the prompts to enter the necessary details:

URL of M3U8: Paste or enter the URL of the M3U8 file.
Title of the file: (Optional) Enter the output file name for the saved MP4 video. If not specified, the default name ft_video.mp4 will be used.
Start time: (Optional) Enter the start time in HH:MM
format. If not specified, the video will start from the beginning.
End time: (Optional) Enter the end time in HH:MM
format. If not specified, the entire video will be downloaded.
Wait for the Process to Complete:

The script will download the video segments and concatenate them into an MP4 file. Progress will be displayed in the console.

Output:

Once the process is complete, the MP4 video will be saved in the same directory as ft.dk.bat.

Example
bash
Copy code
$ cd path/to/your/repository
$ ft.dk.bat
plaintext
Copy code
URL of M3U8: https://example.com/video.m3u8
Title of the file (default: ft_video.mp4):
Start time (default: 00:00:00):
End time (default: end of video):
Notes
ffmpeg: If ffmpeg is not recognized as a command, make sure it is added to your system's PATH environment variable.
Python: Ensure Python is installed and added to your system's PATH.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Directory Structure
Copy code
your-repository/
│
├── ft.dk.bat
├── ft.dk_video.py
├── README.md
├── LICENSE
└── requirements.txt
Files
ft.dk.bat: Batch script to run the Python script with user input.
ft.dk_video.py: Python script that handles downloading and concatenating video segments.
README.md: This file, containing instructions on how to use the scripts.
LICENSE: License information for the project.
requirements.txt: List of Python dependencies for the project.
