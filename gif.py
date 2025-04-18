import sys
from PyPDF2 import PdfFileReader, PdfFileWriter
from PIL import Image
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QGridLayout, 
                           QPushButton, QLabel, QFileDialog, QInputDialog, 
                           QLineEdit, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl

class GIFConverter(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GIF Converter")
        self.setGeometry(100, 100, 400, 200)
        
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

        # Status label
        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)

        # Add Buy Me a Coffee link
        self.coffee_button = QPushButton('☕ Buy Me a Coffee')
        self.coffee_button.clicked.connect(self.open_coffee_link)
        self.coffee_button.setStyleSheet("""
            QPushButton {
                background-color: #FFDD00;
                color: #000000;
                border-radius: 5px;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FFE44D;
            }
        """)
        self.layout.addWidget(self.coffee_button)

    def open_coffee_link(self):
        QDesktopServices.openUrl(QUrl("https://buymeacoffee.com/amanos66"))

    def show_message(self, title, message, icon=QMessageBox.Information):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

    def open_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            caption="Select files",
            directory=str(Path.home()),
            filter=f"Image Files (*.jpg *.png *.bmp *.gif *.webp *.tiff *.psd *.svg);;PDF File (*.pdf);;HEIC Image (*.heic)"
        )

        if files:
            self.image_paths = files
            self.status_label.setText(f"Selected {len(files)} files")
        else:
            self.status_label.setText("No files selected")

    def convert_to_gif(self):
        if not self.image_paths:
            self.show_message("Error", "Please select files first!", QMessageBox.Warning)
            return

        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save GIF As",
            str(Path.home()),
            "GIF Files (*.gif)"
        )
        
        if not output_path:
            return

        if not output_path.lower().endswith('.gif'):
            output_path += '.gif'

        try:
            images = []
            for image_path in self.image_paths:
                try:
                    with Image.open(image_path) as img:
                        if img.mode not in ('RGB', 'RGBA'):
                            img = img.convert('RGB')
                        images.append(img.copy())
                except Exception as e:
                    self.show_message("Error", f"Error opening {image_path}: {str(e)}", QMessageBox.Warning)

            if images:
                images[0].save(
                    output_path,
                    save_all=True,
                    append_images=images[1:],
                    duration=500,
                    loop=0
                )
                self.show_message("Success", f"GIF successfully created at:\n{output_path}")
                self.status_label.setText("Conversion completed successfully!")
            else:
                self.show_message("Error", "No valid images to create GIF!", QMessageBox.Warning)
        except Exception as e:
            self.show_message("Error", f"Error creating GIF: {str(e)}", QMessageBox.Critical)

    def save_to_file(self):
        if not self.image_paths:
            self.show_message("Error", "No images selected!", QMessageBox.Warning)
            return

        self.convert_to_gif()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for better cross-platform appearance
    
    converter = GIFConverter()
    converter.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
