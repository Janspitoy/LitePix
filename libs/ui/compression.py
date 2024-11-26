from kivy.uix.screenmanager import Screen
from threading import Thread
import os

from libs.core.compression import compress_image, compress_video
from kivy.clock import mainthread


class CompressionScreen(Screen):
    """Screen for selecting files and performing compression."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def compress_selected(self, instance):
        """Compress the currently selected file."""
        selected_files = self.ids.file_chooser.selection
        if not selected_files:
            self.update_output("No file selected for compression.")
            return

        selected_file = selected_files[0]  # Only process the first selected file
        ext = os.path.splitext(selected_file)[1].lower()

        if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif', '.webp']:
            self.update_output(f"Compressing image: {selected_file}...")
            Thread(target=self.run_compress_image, args=(selected_file,)).start()
        elif ext in ['.mp4', '.mov', '.mkv', '.avi']:
            self.update_output(f"Compressing video: {selected_file}...")
            Thread(target=self.run_compress_video, args=(selected_file,)).start()
        else:
            self.update_output(f"Unsupported file format: {ext}")

    def compress_all(self, instance):
        """Compress all selected files."""
        selected_files = self.ids.file_chooser.selection
        if not selected_files:
            self.update_output("No files selected for compression.")
            return

        self.update_output("Starting compression for all selected files...")
        Thread(target=self.run_compress_all, args=(selected_files,)).start()

    def run_compress_image(self, file_path):
        """Compress a single image."""
        result = compress_image(file_path)
        self.update_output(result)

    def run_compress_video(self, file_path):
        """Compress a single video."""
        result = compress_video(file_path)
        self.update_output(result)

    def run_compress_all(self, file_list):
        """Compress all selected files."""
        for file_path in file_list:
            ext = os.path.splitext(file_path)[1].lower()
            if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif', '.webp']:
                result = compress_image(file_path)
            elif ext in ['.mp4', '.mov', '.mkv', '.avi']:
                result = compress_video(file_path)
            else:
                result = f"Unsupported file format: {file_path}"
            self.update_output(result)

    @mainthread
    def update_output(self, message):
        """Update the output label with the given message and set text color to black."""
        self.ids.output_label.text = message
        self.ids.output_label.text_color = (0, 0, 0, 1)  # Черный цвет текста (RGBA)
