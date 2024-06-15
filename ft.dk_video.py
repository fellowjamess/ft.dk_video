import os
import sys
import argparse
import requests
from subprocess import call
from tqdm import tqdm
import shutil

def validate_m3u8_url(m3u8_url):
    """
    Validates the M3U8 URL.

    Args:
        m3u8_url (str): The URL of the M3U8 file.

    Raises:
        ValueError: If the provided M3U8 URL is invalid.
    """
    if not m3u8_url.endswith('.m3u8'):
        raise ValueError("Invalid M3U8 URL. Please provide a valid URL ending with .m3u8")

def create_segments_directory():
    """Creates a directory to save the segments."""
    os.makedirs('segments', exist_ok=True)

def download_m3u8_file(m3u8_url):
    """
    Downloads the M3U8 file.

    Args:
        m3u8_url (str): The URL of the M3U8 file.

    Returns:
        str: The content of the M3U8 file.
    """
    try:
        response = requests.get(m3u8_url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error downloading M3U8 file: {e}")
        sys.exit(1)

def parse_m3u8_file(m3u8_content):
    """
    Parses the M3U8 file and collects segment URLs and durations.

    Args:
        m3u8_content (str): The content of the M3U8 file.

    Returns:
        list: A list of tuples containing segment URLs and their durations.
    """
    segment_urls = []
    current_segment = {}
    
    for line in m3u8_content.splitlines():
        if line.startswith('#EXTINF:'):
            duration = float(line.split(':')[1].split(',')[0])
            current_segment['duration'] = duration
        elif not line.startswith('#'):
            current_segment['url'] = line.strip()
            segment_urls.append(current_segment)
            current_segment = {}
    
    return segment_urls

def download_segments(segment_urls, start_time=None, end_time=None):
    """
    Downloads segments with a single progress bar.

    Args:
        segment_urls (list): A list of segment URLs.
        start_time (str): Start time in HH:MM:SS format.
        end_time (str): End time in HH:MM:SS format.

    Returns:
        list: A list of downloaded segment file paths.
    """
    segment_files = []
    total_duration = sum([segment['duration'] for segment in segment_urls])
    current_time = 0.0
    
    if start_time:
        start_time = convert_time_to_seconds(start_time)
    else:
        start_time = 0
    
    if end_time:
        end_time = convert_time_to_seconds(end_time)
    else:
        end_time = total_duration

    duration_to_download = end_time - start_time

    with tqdm(total=duration_to_download, unit='s', unit_scale=True, desc='Downloading', ascii=True) as progress_bar:
        for segment in segment_urls:
            segment_url = segment['url']
            segment_duration = segment['duration']
            segment_name = os.path.join('segments', segment_url.split('/')[-1].split('?')[0])
            
            if current_time + segment_duration < start_time:
                current_time += segment_duration
                continue
            if current_time > end_time:
                break

            segment_files.append(segment_name)

            try:
                segment_response = requests.get(segment_url, stream=True)
                segment_response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Error downloading segment {segment_url}: {e}")
                sys.exit(1)

            with open(segment_name, 'wb') as segment_file:
                for chunk in segment_response.iter_content(chunk_size=1024):
                    if chunk:
                        segment_file.write(chunk)
            
            current_time += segment_duration
            progress_bar.update(segment_duration)

    return segment_files

def create_concat_file(segment_files):
    """
    Creates a text file for ffmpeg to concatenate segments.

    Args:
        segment_files (list): A list of downloaded segment file paths.

    Returns:
        str: The path to the concat file.
    """
    concat_file = 'segments.txt'
    with open(concat_file, 'w') as f:
        for segment in segment_files:
            f.write(f"file '{os.path.abspath(segment)}'\n")
    return concat_file

def combine_segments(concat_file, output_file):
    """
    Combines segments using ffmpeg and re-encodes them.

    Args:
        concat_file (str): The path to the concat file.
        output_file (str): The output file name for the saved MP4 video.
    """
    try:
        call(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', concat_file, '-fflags', '+igndts', '-c:v', 'libx264', '-c:a', 'aac', output_file])
    except FileNotFoundError:
        print("Error: ffmpeg command not found. Make sure ffmpeg is installed and added to your PATH.")
        sys.exit(1)

def cleanup_files(segment_files, concat_file):
    """
    Cleans up segment files and the concat file.

    Args:
        segment_files (list): A list of downloaded segment file paths.
        concat_file (str): The path to the concat file.
    """
    shutil.rmtree('segments')
    os.remove(concat_file)

def convert_time_to_seconds(time_str):
    """
    Converts a time string in HH:MM:SS format to seconds.

    Args:
        time_str (str): Time string in HH:MM:SS format.

    Returns:
        float: Time in seconds.
    """
    h, m, s = map(float, time_str.split(':'))
    return h * 3600 + m * 60 + s

def download_video(m3u8_url, output_file='ft_video.mp4', start_time=None, end_time=None):
    """
    Downloads a video from an M3U8 URL and saves it as an MP4 file.

    Args:
        m3u8_url (str): The URL of the M3U8 file.
        output_file (str): Output file name for the saved MP4 video.
        start_time (str): Start time in HH:MM:SS format.
        end_time (str): End time in HH:MM:SS format.
    """
    # Validate M3U8 URL (commented out because it's not working for all cases)
    # validate_m3u8_url(m3u8_url)

    create_segments_directory()

    m3u8_content = download_m3u8_file(m3u8_url)

    segment_urls = parse_m3u8_file(m3u8_content)

    segment_files = download_segments(segment_urls, start_time, end_time)

    concat_file = create_concat_file(segment_files)

    combine_segments(concat_file, output_file)

    cleanup_files(segment_files, concat_file)

    print(f"\nVideo saved as {output_file} and temporary files cleaned up.")

if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(description="Download and concatenate video segments from an M3U8 file.")
    parser.add_argument('m3u8_url', metavar='m3u8_url', type=str,
                        help='URL of the M3U8 file')
    parser.add_argument('output_file', metavar='output_file', type=str, nargs='?', default='ft_video.mp4',
                        help='Output file name for the saved MP4 video (default: ft_video.mp4)')
    parser.add_argument('--start', metavar='start_time', type=str, default=None,
                        help='Start time in HH:MM:SS format (default: start of video)')
    parser.add_argument('--end', metavar='end_time', type=str, default=None,
                        help='End time in HH:MM:SS format (default: end of video)')

    args = parser.parse_args()

    try:
        download_video(args.m3u8_url, args.output_file, args.start, args.end)
    except ValueError as ve:
        print(f"Error: {ve}")
        sys.exit(1)
  
