from PIL import Image
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor


def compress_image(input_path):
    """Compress a single image using optimized settings without quality loss."""
    if not os.path.exists(input_path):
        return f"Error: File '{input_path}' not found."

    try:
        # Get the file extension
        filename, ext = os.path.splitext(os.path.basename(input_path))
        ext = ext.lower()

        # Define output path
        output_path = os.path.join(os.path.dirname(input_path), f"{filename}_compressed{ext}")

        with Image.open(input_path) as img:
            # Convert image to RGB if it's not in a standard format like RGBA or P
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            print(f"Compressing {input_path}...")

            # For JPEG images
            if ext in ['.jpg', '.jpeg']:
                img.save(output_path, format='JPEG', quality=85, optimize=True)
                print(f"JPEG image saved to {output_path} with quality 85")

            # For PNG images
            elif ext == '.png':
                # Compress PNG images (convert to P for better compression if needed)
                img = img.convert("P", palette=Image.ADAPTIVE, colors=256)
                img.save(output_path, format='PNG', optimize=True)
                print(f"PNG image saved to {output_path} with optimization")

            # For BMP images
            elif ext == '.bmp':
                img.save(output_path, format='BMP', optimize=True)
                print(f"BMP image saved to {output_path}")

            # For TIFF images
            elif ext == '.tiff':
                img.save(output_path, format='TIFF', optimize=True)
                print(f"TIFF image saved to {output_path}")

            # For GIF images
            elif ext == '.gif':
                img.save(output_path, format='GIF', optimize=True)
                print(f"GIF image saved to {output_path}")

            # For WebP images
            elif ext == '.webp':
                img.save(output_path, format='WEBP', quality=85, optimize=True)
                print(f"WEBP image saved to {output_path}")

            else:
                print(f"Format {ext} is not supported for compression.")
                return f"Unsupported format: {ext}"

        # Check if compression actually reduced the size
        original_size = os.path.getsize(input_path)
        compressed_size = os.path.getsize(output_path)

        if compressed_size >= original_size:
            os.remove(output_path)  # If compression didn't reduce the size, delete the compressed file
            return f"No size reduction for '{input_path}'."

        return f"Image compressed successfully and saved as {output_path} (reduced by {((original_size - compressed_size) / original_size) * 100:.2f}%)"

    except Exception as e:
        return f"Error processing image '{input_path}': {e}"


def compress_video(input_path):
    """Compress a single video using FFmpeg for faster compression."""
    if not os.path.exists(input_path):
        return f"Error: File '{input_path}' not found."

    ffmpeg_command = "ffmpeg"  # Assuming 'ffmpeg' is available in the system PATH

    try:
        filename, ext = os.path.splitext(os.path.basename(input_path))
        output_path = os.path.join(os.path.dirname(input_path), f"{filename}_compressed{ext}")

        # Check if file extension is MOV and adjust the compression if needed
        if ext.lower() == ".mov":
            # Special settings for MOV format compression
            ffmpeg_command_list = [
                ffmpeg_command,
                "-i", input_path,
                "-vcodec", "libx264",
                "-acodec", "aac",
                "-crf", "28",  # Higher value = more compression
                "-preset", "ultrafast",  # Ultra-fast compression (can adjust for trade-off between speed and size)
                "-movflags", "faststart",
                "-threads", "8",  # Increase the number of threads for better performance
                output_path
            ]
        else:
            # General settings for other video formats
            ffmpeg_command_list = [
                ffmpeg_command,
                "-i", input_path,
                "-vcodec", "libx264",
                "-acodec", "aac",
                "-crf", "28",  # Higher value = more compression
                "-preset", "ultrafast",  # Ultra-fast compression
                "-threads", "8",  # Increase the number of threads for better performance
                output_path
            ]

        # Run FFmpeg with subprocess
        process = subprocess.run(
            ffmpeg_command_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Check for errors
        if process.returncode != 0:
            print(f"FFmpeg error for file '{input_path}': {process.stderr}")
            return f"Error processing video '{input_path}': {process.stderr}"

        return f"Video compressed and saved as {output_path}"

    except Exception as e:
        return f"Unexpected error processing video '{input_path}': {e}"


def parallel_image_compress(image_path_list):
    """Compress multiple images in parallel using ThreadPoolExecutor."""
    results = []
    with ThreadPoolExecutor(max_workers=20) as executor:  # You can adjust the number of workers here
        results = list(executor.map(compress_image, image_path_list))
    return results


def parallel_video_compress(video_path_list):
    """Compress multiple videos in parallel using ThreadPoolExecutor."""
    with ThreadPoolExecutor(max_workers=50) as executor:  # 5 threads for optimal performance
        results = list(executor.map(compress_video, video_path_list))
    return results
