import sys
from PyPDF2 import PdfFileReader, PdfFileWriter
from PIL import Image
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel, QFileDialog, QInputDialog, QLineEdit
from PyQt5.QtCore import Qt

class GIFConverter(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GIF Converter")
        self.setGeometry(100, 100, 400, 150)
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)

        self.image_paths = []

        # Create layout for input
        self.input_layout = QGridLayout()
        self.input_layout.setSpacing(10)
        self.layout.addLayout(self.input_layout)

        self.input_label = QLabel("Select files to convert:")
        self.input_layout.addWidget(self.input_label, 0, 0, 1, 3)
        
        self.open_button = QPushButton('Open')
        self.open_button.clicked.connect(self.open_files)
        self.input_layout.addWidget(self.open_button, 1, 0, 1, 1)

        self.convert_button = QPushButton('Convert to GIF')
        self.convert_button.clicked.connect(self.convert_to_gif)
        self.input_layout.addWidget(self.convert_button, 1, 1, 1, 1)

        self.save_button = QPushButton('Save to file')
        self.save_button.clicked.connect(self.save_to_file)
        self.input_layout.addWidget(self.save_button, 1, 2, 1, 1)

    def open_files(self):
        # Open files dialog
        files, _ = QFileDialog.getOpenFileNames(
            caption="Select files",
            directory=str(Path.home()),
            filter=f"Image Files (*.jpg *.png *.bmp *.gif *.webp *.tiff *.psd *.svg);;PDF File (*.pdf);;HEIC Image (*.heic)"
        )

        # Add file paths to list
        self.image_paths = files

    def convert_to_gif(self):
        if len(self.image_paths) > 0:
            output_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save GIF As",
                str(Path.home()),
                "GIF Files (*.gif)"
            )
            
            if not output_path:
                return

            # Ensure .gif extension
            if not output_path.lower().endswith('.gif'):
                output_path += '.gif'

            images = []

            # Open each file and add to list
            for image_path in self.image_paths:
                try:
                    with Image.open(image_path) as img:
                        # Convert to RGB if necessary
                        if img.mode not in ('RGB', 'RGBA'):
                            img = img.convert('RGB')
                        images.append(img.copy())  # Make a copy to keep in memory
                except Exception as e:
                    print(f"Error opening {image_path}: {e}")

            # Create GIF from images
            if len(images) > 0:
                try:
                    # Save with duration=500 milliseconds per frame
                    images[0].save(
                        output_path,
                        save_all=True,
                        append_images=images[1:],
                        duration=500,
                        loop=0
                    )
                    print(f"GIF successfully created at: {output_path}")
                except Exception as e:
                    print(f"Error creating GIF: {e}")

    def save_to_file(self):
        if not self.image_paths:
            print("No images selected!")
            return

        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save GIF As",
            str(Path.home()),
            "GIF Files (*.gif)"
        )

        if not output_path:
            return

        # Ensure .gif extension
        if not output_path.lower().endswith('.gif'):
            output_path += '.gif'

        # Create GIF from images
        images = []
        try:
            for image_path in self.image_paths:
                with Image.open(image_path) as img:
                    if img.mode not in ('RGB', 'RGBA'):
                        img = img.convert('RGB')
                    images.append(img.copy())

            if images:
                images[0].save(
                    output_path,
                    save_all=True,
                    append_images=images[1:],
                    duration=500,
                    loop=0
                )
                print(f"GIF successfully saved to: {output_path}")
            else:
                print("No valid images to create GIF!")
        except Exception as e:
            print(f"Error creating GIF: {e}")

def main():
    app = QApplication(sys.argv)

    converter = GIFConverter()
    converter.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
