import sys
import csv
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog
from PyQt5.QtGui import QPixmap, QColor , QFont
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer

image_path = ""
image_name = ""

class PneumoniaDiagnosisApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pneumonia Diagnosis")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Image layout
        self.image_layout = QHBoxLayout()
        self.main_layout.addLayout(self.image_layout)

        # Labels for images
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(300, 300)
        self.image_layout.addWidget(self.image_label)

        self.gradcam_label = QLabel(self)
        self.gradcam_label.setFixedSize(300, 300)
        self.image_layout.addWidget(self.gradcam_label)

        # Button and text layout
        self.bottom_layout = QVBoxLayout()
        self.main_layout.addLayout(self.bottom_layout)

        # Prediction text label
        self.prediction_label = QLabel(self)
        self.prediction_label.setAlignment(QtCore.Qt.AlignCenter)
        self.prediction_label.setFont(QFont("Arial", 16))
        self.bottom_layout.addWidget(self.prediction_label)

        # Report text label
        self.report_label = QLabel(self)
        self.report_label.setAlignment(QtCore.Qt.AlignCenter)
        self.report_label   .setFont(QFont("Arial", 13))
        self.bottom_layout.addWidget(self.report_label)

        # Buttons
        select_image_button = QPushButton("Select Image", self)
        select_image_button.setFixedWidth(300)
        select_image_button.setFixedHeight(30)
        select_image_button.clicked.connect(self.browse_image)
        self.bottom_layout.addWidget(select_image_button, alignment=QtCore.Qt.AlignCenter)

        predict_button = QPushButton("Predict Image", self)
        predict_button.setFixedWidth(300)
        predict_button.setFixedHeight(30)
        predict_button.clicked.connect(self.predict_image)
        self.bottom_layout.addWidget(predict_button, alignment=QtCore.Qt.AlignCenter)

        gradcam_button = QPushButton("Gradcam", self)
        gradcam_button.setFixedWidth(300)
        gradcam_button.setFixedHeight(30)
        gradcam_button.clicked.connect(self.display_gradcam)
        self.bottom_layout.addWidget(gradcam_button, alignment=QtCore.Qt.AlignCenter)

        generate_report_button = QPushButton("Generate Report", self)
        generate_report_button.setFixedWidth(300)
        generate_report_button.setFixedHeight(30)
        generate_report_button.clicked.connect(self.generate_report)
        self.bottom_layout.addWidget(generate_report_button, alignment=QtCore.Qt.AlignCenter)

        # Load CSV data
        self.csv_data = self.load_csv_data("dummy_data.csv")

        # Processing GIF
        self.processing_label = QLabel(self)
        self.processing_pixmap = QPixmap("processing.gif")
        self.processing_label.setPixmap(self.processing_pixmap)
        self.processing_label.setAlignment(QtCore.Qt.AlignCenter)
        self.processing_label.hide()
        self.main_layout.addWidget(self.processing_label)

    def load_csv_data(self, filename):
        data = {}
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data[row['image_name']] = {
                    'Prediction': row['Prediction'],
                    'gradcam_filepath': row['gradcam_filepath'],
                    'Report': row['Report']
                }
        return data

    def browse_image(self):
        global image_path, image_name
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)", options=options)
        if filename:
            image_path = filename
            image_name = os.path.basename(filename)
            self.display_image(image_path)

    def display_image(self, filename):
        pixmap = QPixmap(filename)
        pixmap = pixmap.scaledToWidth(300)
        self.image_label.setPixmap(pixmap)

    def predict_image(self):
        if not image_path:
            return

        self.processing_label.show()
        QTimer.singleShot(2000, self.print_prediction)

    def print_prediction(self):
        if image_name in self.csv_data:
            prediction = self.csv_data[image_name]['Prediction']
            self.prediction_label.setText(f"Prediction: {prediction}")  # Set prediction text
            if prediction == "Positive":
                self.prediction_label.setStyleSheet("color: red;")
            elif prediction == "Normal":
                self.prediction_label.setStyleSheet("color: green;")
        self.processing_label.hide()

    def display_gradcam(self):
        if not image_path:
            return

        self.processing_label.show()
        QTimer.singleShot(10000, self.show_gradcam)

    def show_gradcam(self):
        if image_name in self.csv_data and self.csv_data[image_name]['Prediction'] == "Positive":
            gradcam_path = self.csv_data[image_name]['gradcam_filepath']
            self.display_gradcam_image(gradcam_path)
        elif image_name in self.csv_data and self.csv_data[image_name]['Prediction'] == "Normal":
            self.display_blue_overlay()
        self.processing_label.hide()

    def display_gradcam_image(self, filename):
        pixmap = QPixmap(filename)
        pixmap = pixmap.scaledToWidth(300)
        self.gradcam_label.setPixmap(pixmap)

    def display_blue_overlay(self):
        blue_pixmap = QPixmap(300, 300)
        blue_pixmap.fill(QColor(0, 0, 0, 128))  # Transparent blue overlay
        self.gradcam_label.setPixmap(blue_pixmap)

    def generate_report(self):
        if not image_path:
            return

        self.processing_label.show()
        QTimer.singleShot(12000, self.print_report)

    def print_report(self):
        if image_name in self.csv_data:
            report = self.csv_data[image_name]['Report']
            self.report_label.setText(f"Report: {report}")  # Set report text
        self.processing_label.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PneumoniaDiagnosisApp()
    window.show()
    sys.exit(app.exec_())
