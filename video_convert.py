#!/usr/bin/env python3
"""
Video Converter - Converts video files between formats with improved error handling and flexibility.
Supports multiple input/output formats, GIF conversion with customizable settings, and batch processing.
"""

import os
import sys
from pathlib import Path
from moviepy.editor import VideoFileClip
from tqdm import tqdm
import argparse

class VideoConverter:
    def __init__(self, input_dir: str = None, output_dir: str = None):
        self.input_dir = Path(input_dir or "input")
        self.output_dir = Path(output_dir or "output")
        
        # Create directories if they don't exist
        self.input_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
        # Supported input formats
        self.supported_formats = {
            '.mp4': 'MP4',
            '.avi': 'AVI',
            '.mov': 'MOV',
            '.mkv': 'MKV',
            '.webm': 'WebM',
            '.flv': 'FLV',
            '.wmv': 'WMV',
            '.m4v': 'M4V'
        }
        
        # Output format options
        self.output_formats = {
            'gif': 'GIF',
            'mp4': 'MP4',
            'avi': 'AVI',
            'mov': 'MOV',
            'webm': 'WebM'
        }

    def get_input_format(self):
        """Get input format from user with validation."""
        while True:
            print("\nAvailable input formats:")
            for i, (ext, name) in enumerate(self.supported_formats.items(), 1):
                print(f"[{i}] {name} ({ext})")
            
            try:
                choice = int(input("\nSelect input format (1-{}): ".format(
                    len(self.supported_formats)
                )).strip())
                if 1 <= choice <= len(self.supported_formats):
                    return list(self.supported_formats.keys())[choice-1]
                else:
                    print(f"Invalid choice. Please select a number between 1 and {len(self.supported_formats)}.")
            except ValueError:
                print("Please enter a valid number.")
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                sys.exit(0)

    def get_output_format(self):
        """Get output format from user."""
        while True:
            print("\nAvailable output formats:")
            for i, (ext, name) in enumerate(self.output_formats.items(), 1):
                print(f"[{i}] {name} (.{ext})")
            
            try:
                choice = int(input("\nSelect output format (1-{}): ".format(
                    len(self.output_formats)
                )).strip())
                if 1 <= choice <= len(self.output_formats):
                    return list(self.output_formats.keys())[choice-1]
                else:
                    print(f"Invalid choice. Please select a number between 1 and {len(self.output_formats)}.")
            except ValueError:
                print("Please enter a valid number.")
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                sys.exit(0)

    def get_gif_settings(self):
        """Get GIF-specific settings from user."""
        settings = {}
        
        # FPS setting
        while True:
            try:
                fps = input("Enter frames per second (default 15, or press Enter to skip): ").strip()
                if fps:
                    settings['fps'] = float(fps)
                else:
                    settings['fps'] = 15
                break
            except ValueError:
                print("Please enter a valid number.")
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                sys.exit(0)
        
        # Size/resolution setting
        print("\nResolution options:")
        print("[1] Keep original size")
        print("[2] Scale down (max width 720px)")
        print("[3] Custom size")
        
        while True:
            try:
                choice = int(input("Select resolution option (1-3, default 1): ").strip() or "1")
                if choice == 1:
                    settings['resize'] = None
                elif choice == 2:
                    settings['resize'] = (720, None)  # Scale width, maintain aspect
                elif choice == 3:
                    width = int(input("Enter width in pixels: ").strip())
                    height = int(input("Enter height in pixels (0 to maintain aspect): ").strip())
                    settings['resize'] = (width, height if height > 0 else None)
                else:
                    print("Please select 1-3.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                sys.exit(0)
        
        return settings

    def get_video_settings(self, output_format: str):
        """Get video-specific settings from user."""
        settings = {}
        
        if output_format == 'gif':
            return self.get_gif_settings()
        
        # For other formats, you could add bitrate, codec, etc.
        return settings

    def get_conversion_mode(self):
        """Get conversion mode from user."""
        while True:
            print("\nConversion modes:")
            print("[1] Convert all files of selected format")
            print("[2] Convert single file manually")
            
            try:
                choice = int(input("\nSelect mode (1-2): ").strip())
                if choice in [1, 2]:
                    return choice
                else:
                    print("Please select 1 or 2.")
            except ValueError:
                print("Please enter a valid number.")
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                sys.exit(0)

    def convert_single_video(self, input_path: Path, output_path: Path, output_format: str, settings: dict):
        """Convert a single video file."""
        if not input_path.exists():
            print(f"Error: File '{input_path}' not found.")
            return False
        
        clip = None
        try:
            # Load video file
            clip = VideoFileClip(str(input_path))
            
            # Apply resizing if specified
            if settings.get('resize'):
                width, height = settings['resize']
                if height is None:
                    # Maintain aspect ratio
                    clip = clip.resize(width=width)
                else:
                    clip = clip.resize((width, height))
            
            # Export based on format
            if output_format == 'gif':
                fps = settings.get('fps', 15)
                clip.write_gif(str(output_path), fps=fps, verbose=False, logger=None)
            else:
                # For other video formats
                clip.write_videofile(str(output_path), verbose=False, logger=None)
            
            return True
        except Exception as e:
            print(f"Error converting {input_path.name}: {e}")
            return False
        finally:
            # Ensure clip is closed to free resources
            if clip is not None:
                clip.close()

    def convert_all_videos(self, input_ext: str, output_format: str, settings: dict):
        """Convert all video files of specified format."""
        input_files = list(self.input_dir.glob(f"*{input_ext}"))
        
        if not input_files:
            print(f"No {input_ext} files found in {self.input_dir}")
            return
        
        print(f"Found {len(input_files)} {input_ext} files to convert.")
        
        success_count = 0
        
        for input_path in tqdm(input_files, desc="Converting"):
            output_filename = f"{input_path.stem}.{output_format}"
            output_path = self.output_dir / output_filename
            
            if self.convert_single_video(input_path, output_path, output_format, settings):
                success_count += 1
        
        print(f"\nConversion complete! {success_count}/{len(input_files)} files converted successfully.")

    def open_directories(self):
        """Open input and output directories in file explorer."""
        try:
            if os.name == 'nt':  # Windows
                os.startfile(str(self.input_dir))
                os.startfile(str(self.output_dir))
            elif os.name == 'posix':  # macOS/Linux
                os.system(f"open {self.input_dir}")
                os.system(f"open {self.output_dir}")
        except Exception as e:
            print(f"Could not open directories: {e}")

    def run(self):
        """Main conversion workflow."""
        print("=== Video Converter ===")
        
        # Open directories for user
        self.open_directories()
        
        # Get user preferences
        input_format = self.get_input_format()
        output_format = self.get_output_format()
        settings = self.get_video_settings(output_format)
        mode = self.get_conversion_mode()
        
        if mode == 1:
            self.convert_all_videos(input_format, output_format, settings)
        else:
            filename = input("Enter filename (without extension): ").strip()
            input_path = self.input_dir / f"{filename}{input_format}"
            output_path = self.output_dir / f"{filename}.{output_format}"
            
            if self.convert_single_video(input_path, output_path, output_format, settings):
                print("Conversion successful!")
            else:
                print("Conversion failed.")
        
        # Open output directory
        try:
            if os.name == 'nt':
                os.startfile(str(self.output_dir))
        except:
            pass

def main():
    parser = argparse.ArgumentParser(description='Convert video files between formats')
    parser.add_argument('--input', '-i', help='Input directory path')
    parser.add_argument('--output', '-o', help='Output directory path')
    
    args = parser.parse_args()
    
    converter = VideoConverter(args.input, args.output)
    converter.run()

if __name__ == "__main__":
    main()
