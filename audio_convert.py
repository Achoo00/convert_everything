#!/usr/bin/env python3
"""
Audio Converter - Converts audio files between formats with improved error handling and flexibility.
Supports multiple input/output formats, PCM conversion, and customizable audio parameters.
"""

import os
import sys
import shutil
from pathlib import Path
from pydub import AudioSegment
from tqdm import tqdm
import argparse

class AudioConverter:
    def __init__(self, input_dir: str = None, output_dir: str = None, ffmpeg_path: str = None):
        self.input_dir = Path(input_dir or "input")
        self.output_dir = Path(output_dir or "output")
        
        # Create directories if they don't exist
        self.input_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
        # Supported input formats
        self.supported_formats = {
            '.m4a': 'M4A',
            '.mp3': 'MP3',
            '.wav': 'WAV',
            '.flac': 'FLAC',
            '.ogg': 'OGG',
            '.aac': 'AAC',
            '.wma': 'WMA',
            '.mp4': 'MP4 (audio)'
        }
        
        # Output format options
        self.output_formats = {
            'mp3': 'MP3',
            'wav': 'WAV',
            'm4a': 'M4A',
            'flac': 'FLAC',
            'ogg': 'OGG Vorbis',
            'aac': 'AAC',
            'pcm': 'PCM (Raw)'
        }
        
        # Configure ffmpeg path
        self.ffmpeg_path = self._find_ffmpeg(ffmpeg_path)
        if self.ffmpeg_path:
            ffmpeg_exe = 'ffmpeg.exe' if os.name == 'nt' else 'ffmpeg'
            ffprobe_exe = 'ffprobe.exe' if os.name == 'nt' else 'ffprobe'
            AudioSegment.converter = str(self.ffmpeg_path / ffmpeg_exe)
            AudioSegment.ffprobe = str(self.ffmpeg_path / ffprobe_exe)
        else:
            print("Warning: ffmpeg not found. Some formats may not work.")
            print("Please install ffmpeg or provide path using --ffmpeg flag.")

    def _find_ffmpeg(self, custom_path: str | None) -> Path | None:
        """Find ffmpeg installation on the system."""
        # Check custom path first
        if custom_path:
            ffmpeg_dir = Path(custom_path)
            if (ffmpeg_dir / 'ffmpeg').exists() or (ffmpeg_dir / 'ffmpeg.exe').exists():
                return ffmpeg_dir
        
        # Common Windows paths
        common_paths = [
            Path('C:/ffmpeg/bin'),
            Path('C:/Program Files/ffmpeg/bin'),
            Path(os.environ.get('ProgramFiles', 'C:/Program Files')) / 'ffmpeg' / 'bin',
        ]
        
        # Check system PATH
        ffmpeg_exe = shutil.which('ffmpeg')
        if ffmpeg_exe:
            return Path(ffmpeg_exe).parent
        
        # Check common paths
        for path in common_paths:
            if path.exists():
                ffmpeg_exe = path / ('ffmpeg.exe' if os.name == 'nt' else 'ffmpeg')
                if ffmpeg_exe.exists():
                    return path
        
        return None

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

    def get_audio_settings(self, output_format: str):
        """Get audio processing settings from user."""
        settings = {}
        
        # PCM-specific settings
        if output_format == 'pcm':
            print("\nPCM Settings:")
            print("[1] Unsigned 8-bit (u8)")
            print("[2] Signed 8-bit (s8)")
            print("[3] Signed 16-bit (s16)")
            print("[4] Signed 32-bit (s32)")
            
            while True:
                try:
                    choice = int(input("Select bit depth (1-4): ").strip())
                    pcm_formats = {1: 'u8', 2: 's8', 3: 's16', 4: 's32'}
                    if choice in pcm_formats:
                        settings['pcm_format'] = pcm_formats[choice]
                        break
                    else:
                        print("Please select 1-4.")
                except ValueError:
                    print("Please enter a valid number.")
                except KeyboardInterrupt:
                    print("\nOperation cancelled.")
                    sys.exit(0)
            
            # Sample rate for PCM
            while True:
                try:
                    sample_rate = input("Enter sample rate in Hz (default 16000): ").strip()
                    settings['sample_rate'] = int(sample_rate) if sample_rate else 16000
                    break
                except ValueError:
                    print("Please enter a valid number.")
                except KeyboardInterrupt:
                    print("\nOperation cancelled.")
                    sys.exit(0)
        else:
            # Channel settings
            print("\nAudio Channel Settings:")
            print("[1] Mono (1 channel)")
            print("[2] Stereo (2 channels)")
            print("[3] Keep original")
            
            while True:
                try:
                    choice = int(input("Select channels (1-3, default 3): ").strip() or "3")
                    if choice == 1:
                        settings['channels'] = 1
                    elif choice == 2:
                        settings['channels'] = 2
                    else:
                        settings['channels'] = None  # Keep original
                    break
                except ValueError:
                    print("Please enter a valid number.")
                except KeyboardInterrupt:
                    print("\nOperation cancelled.")
                    sys.exit(0)
        
        # Bitrate for compressed formats
        if output_format in ['mp3', 'm4a', 'aac', 'ogg']:
            while True:
                try:
                    bitrate = input("Enter bitrate in kbps (default 192, or press Enter to skip): ").strip()
                    if bitrate:
                        settings['bitrate'] = bitrate
                    break
                except ValueError:
                    print("Please enter a valid number.")
                except KeyboardInterrupt:
                    print("\nOperation cancelled.")
                    sys.exit(0)
        
        return settings

    def get_naming_mode(self):
        """Get file naming mode."""
        while True:
            print("\nFile Naming:")
            print("[1] Preserve original filenames")
            print("[2] Use numeric counter (0, 1, 2, ...)")
            
            try:
                choice = int(input("Select naming mode (1-2, default 1): ").strip() or "1")
                return choice
            except ValueError:
                print("Please enter 1 or 2.")
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                sys.exit(0)

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

    def convert_single_audio(self, input_path: Path, output_path: Path, output_format: str, settings: dict, preserve_name: bool = True):
        """Convert a single audio file."""
        if not input_path.exists():
            print(f"Error: File '{input_path}' not found.")
            return False
        
        try:
            # Load audio file
            audio = AudioSegment.from_file(str(input_path))
            
            # Apply audio processing settings
            if output_format == 'pcm':
                # Apply PCM-specific settings
                if 'channels' in settings and settings['channels']:
                    audio = audio.set_channels(settings['channels'])
                
                # Set sample width based on PCM format
                pcm_format = settings.get('pcm_format', 'u8')
                if pcm_format in ['u8', 's8']:
                    audio = audio.set_sample_width(1)  # 8-bit
                elif pcm_format == 's16':
                    audio = audio.set_sample_width(2)  # 16-bit
                elif pcm_format == 's32':
                    audio = audio.set_sample_width(4)  # 32-bit
                
                # Export PCM with sample rate
                sample_rate = settings.get('sample_rate', 16000)
                audio.export(
                    str(output_path),
                    format=pcm_format,
                    parameters=['-ar', str(sample_rate)]
                )
            else:
                # Apply channel settings if specified
                if settings.get('channels'):
                    audio = audio.set_channels(settings['channels'])
                
                # Export with format-specific parameters
                export_params = {}
                if 'bitrate' in settings:
                    export_params['bitrate'] = settings['bitrate']
                
                audio.export(str(output_path), format=output_format, **export_params)
            
            return True
        except Exception as e:
            print(f"Error converting {input_path.name}: {e}")
            return False

    def convert_all_audio(self, input_ext: str, output_format: str, settings: dict, naming_mode: int):
        """Convert all audio files of specified format."""
        input_files = list(self.input_dir.glob(f"*{input_ext}"))
        
        if not input_files:
            print(f"No {input_ext} files found in {self.input_dir}")
            return
        
        print(f"Found {len(input_files)} {input_ext} files to convert.")
        
        success_count = 0
        counter = 0
        
        for input_path in tqdm(input_files, desc="Converting"):
            if naming_mode == 1:
                # Preserve filename
                output_filename = f"{input_path.stem}.{output_format}"
            else:
                # Use numeric counter
                output_filename = f"{counter}.{output_format}"
                counter += 1
            
            output_path = self.output_dir / output_filename
            
            if self.convert_single_audio(input_path, output_path, output_format, settings, naming_mode == 1):
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
        print("=== Audio Converter ===")
        
        # Open directories for user
        self.open_directories()
        
        # Get user preferences
        input_format = self.get_input_format()
        output_format = self.get_output_format()
        settings = self.get_audio_settings(output_format)
        naming_mode = self.get_naming_mode()
        mode = self.get_conversion_mode()
        
        if mode == 1:
            self.convert_all_audio(input_format, output_format, settings, naming_mode)
        else:
            filename = input("Enter filename (without extension): ").strip()
            input_path = self.input_dir / f"{filename}{input_format}"
            output_path = self.output_dir / f"{filename}.{output_format}"
            
            if self.convert_single_audio(input_path, output_path, output_format, settings):
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
    parser = argparse.ArgumentParser(description='Convert audio files between formats')
    parser.add_argument('--input', '-i', help='Input directory path')
    parser.add_argument('--output', '-o', help='Output directory path')
    parser.add_argument('--ffmpeg', '-f', help='Path to ffmpeg directory (e.g., C:/ffmpeg/bin)')
    
    args = parser.parse_args()
    
    converter = AudioConverter(args.input, args.output, args.ffmpeg)
    converter.run()

if __name__ == "__main__":
    main()
