#!/usr/bin/env python3
"""
Module to extract random frames from MP4 videos.

Usage:
    python extract_frames.py --input <input_folder> --output <output_folder> --frames <N>
"""

import argparse
import os
import random
from pathlib import Path
from moviepy.video.io.VideoFileClip import VideoFileClip
import imageio



def extract_random_frames(video_path, output_folder, num_frames):
    """
    Extract N random frames from a video and save them to the output folder.
    
    Args:
        video_path (str): Path to the MP4 video file
        output_folder (str): Path to the folder where frames will be saved
        num_frames (int): Number of random frames to extract
    """
    video_name = Path(video_path).stem
    
    try:
        video = VideoFileClip(video_path)
    except Exception as e:
        print(f"Error: Could not open video {video_path}: {e}")
        return
    
    duration = video.duration
    fps = video.fps
    total_frames = int(duration * fps)
    
    if total_frames == 0:
        print(f"Error: Video {video_path} has no frames")
        video.close()
        return
    
    if num_frames > total_frames:
        print(f"Warning: {video_name} has only {total_frames} frames, extracting all")
        num_frames = total_frames
    
    frame_indices = sorted(random.sample(range(total_frames), num_frames))
    
    extracted_count = 0
    for idx, frame_num in enumerate(frame_indices):
        try:
            time_sec = frame_num / fps
            frame = video.get_frame(time_sec)
            
            frame_filename = f"{video_name}_frame_{idx + 1:03d}.jpg"
            frame_path = os.path.join(output_folder, frame_filename)
            
            imageio.imwrite(frame_path, frame)
            extracted_count += 1
        except Exception as e:
            print(f"Warning: Could not extract frame {frame_num} from {video_name}: {e}")
    
    video.close()
    print(f"Extracted {extracted_count} frames from {video_name}")


def process_videos(input_folder, output_folder, num_frames):
    """
    Process all MP4 files in the input folder.
    
    Args:
        input_folder (str): Path to folder containing MP4 files
        output_folder (str): Path to output folder for extracted frames
        num_frames (int): Number of random frames to extract per video
    """
    os.makedirs(output_folder, exist_ok=True)
    
    input_path = Path(input_folder)
    if not input_path.is_dir():
        print(f"Error: Input folder {input_folder} does not exist")
        return
    
    mp4_files = list(input_path.glob("*.mp4"))
    
    if not mp4_files:
        print(f"No MP4 files found in {input_folder}")
        return
    
    print(f"Found {len(mp4_files)} MP4 file(s)")
    
    for video_file in mp4_files:
        extract_random_frames(str(video_file), output_folder, num_frames)


def main():
    parser = argparse.ArgumentParser(
        description="Extract random frames from MP4 videos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python extract_frames.py --input ./videos --output ./frames --frames 5
  python extract_frames.py -i ./input -o ./output -f 10
        """
    )
    
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to input folder containing MP4 files"
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Path to output folder where frames will be saved"
    )
    parser.add_argument(
        "--frames", "-f",
        type=int,
        required=True,
        help="Number of random frames to extract from each video"
    )
    
    args = parser.parse_args()
    
    if args.frames <= 0:
        print("Error: Number of frames must be greater than 0")
        return
    
    process_videos(args.input, args.output, args.frames)


if __name__ == "__main__":
    main()
