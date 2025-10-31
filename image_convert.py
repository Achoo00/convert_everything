#!/usr/bin/env python3
"""
Image Converter - Converts images to various formats with improved error handling and flexibility.
"""

import os
import sys
from pathlib import Path
from PIL import Image
from tqdm import tqdm
import argparse

class ImageConverter:
    def __init__(self, input_dir: str = None, output_dir: str = None):
        self.input_dir = Path(input_dir or "input")
        self.output_dir = Path(output_dir or "output")
        
        # Create directories if they don't exist
        self.input_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
        # Supported input formats
        self.supported_formats = {
            '.webp': 'WebP',
            '.jpg': 'JPEG', 
            '.jpeg': 'JPEG',
            '.jfif': 'JPEG',
            '.png': 'PNG',
            '.bmp': 'BMP',
            '.tiff': 'TIFF',
            '.gif': 'GIF'
        }
        
        # Output format options
        self.output_formats = {
            'png': 'PNG',
            'jpg': 'JPEG',
            'jpeg': 'JPEG',
            'webp': 'WebP',
            'bmp': 'BMP'
        }

    def get_input_format(self):
        """Get input format from user with validation."""
        while True:
            print("\nAvailable input formats:")
            for i, (ext, name) in enumerate(self.supported_formats.items(), 1):
                print(f"[{i}] {name} ({ext})")
            
            try:
                choice = int(input("\nSelect input format (1-8): ").strip())
                if 1 <= choice <= len(self.supported_formats):
                    return list(self.supported_formats.keys())[choice-1]
                else:
                    print("Invalid choice. Please select a number between 1 and 8.")
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
                choice = int(input("\nSelect output format (1-5): ").strip())
                if 1 <= choice <= len(self.output_formats):
                    return list(self.output_formats.keys())[choice-1]
                else:
                    print("Invalid choice. Please select a number between 1 and 5.")
            except ValueError:
                print("Please enter a valid number.")
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

    def convert_single_image(self, filename: str, input_ext: str, output_ext: str):
        """Convert a single image file."""
        input_path = self.input_dir / f"{filename}{input_ext}"
        output_path = self.output_dir / f"{filename}.{output_ext}"
        
        if not input_path.exists():
            print(f"Error: File '{input_path}' not found.")
            return False
            
        try:
            with Image.open(input_path) as img:
                # Convert to RGB if necessary (for JPEG output)
                if output_ext.lower() in ['jpg', 'jpeg'] and img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                elif output_ext.lower() == 'png' and img.mode == 'P':
                    img = img.convert('RGBA')
                
                img.save(output_path, self.output_formats[output_ext])
            return True
        except Exception as e:
            print(f"Error converting {filename}: {e}")
            return False

    def convert_all_images(self, input_ext: str, output_ext: str):
        """Convert all images of specified format."""
        input_files = list(self.input_dir.glob(f"*{input_ext}"))
        
        if not input_files:
            print(f"No {input_ext} files found in {self.input_dir}")
            return
        
        print(f"Found {len(input_files)} {input_ext} files to convert.")
        
        success_count = 0
        for input_path in tqdm(input_files, desc="Converting"):
            filename = input_path.stem
            if self.convert_single_image(filename, input_ext, output_ext):
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
        print("=== Image Converter ===")
        
        # Open directories for user
        self.open_directories()
        
        # Get user preferences
        input_format = self.get_input_format()
        output_format = self.get_output_format()
        mode = self.get_conversion_mode()
        
        if mode == 1:
            self.convert_all_images(input_format, output_format)
        else:
            filename = input("Enter filename (without extension): ").strip()
            if self.convert_single_image(filename, input_format, output_format):
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
    parser = argparse.ArgumentParser(description='Convert images between formats')
    parser.add_argument('--input', '-i', help='Input directory path')
    parser.add_argument('--output', '-o', help='Output directory path')
    
    args = parser.parse_args()
    
    converter = ImageConverter(args.input, args.output)
    converter.run()

if __name__ == "__main__":
    main()
