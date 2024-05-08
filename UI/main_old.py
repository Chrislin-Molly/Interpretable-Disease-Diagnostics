# import sys
# import csv
# import os
# from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog
# from PyQt5.QtGui import QPixmap

# image_path = ""
# image_name = ""

# class PneumoniaDiagnosisApp(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("Pneumonia Diagnosis")
#         self.setGeometry(100, 100, 800, 600)

#         self.central_widget = QWidget()
#         self.setCentralWidget(self.central_widget)
#         self.main_layout = QVBoxLayout()
#         self.central_widget.setLayout(self.main_layout)

#         self.image_label = QLabel(self)
#         self.image_label.setFixedSize(300, 300)
#         self.main_layout.addWidget(self.image_label)

#         self.prediction_label = QLabel(self)
#         self.main_layout.addWidget(self.prediction_label)

#         self.report_label = QLabel(self)
#         self.main_layout.addWidget(self.report_label)

#         select_image_button = QPushButton("Select Image", self)
#         select_image_button.clicked.connect(self.browse_image)
#         self.main_layout.addWidget(select_image_button)

#         predict_button = QPushButton("Predict Image", self)
#         predict_button.clicked.connect(self.predict_image)
#         self.main_layout.addWidget(predict_button)

#         gradcam_button = QPushButton("Gradcam", self)
#         gradcam_button.clicked.connect(self.display_gradcam)
#         self.main_layout.addWidget(gradcam_button)

#         generate_report_button = QPushButton("Generate Report", self)
#         generate_report_button.clicked.connect(self.generate_report)
#         self.main_layout.addWidget(generate_report_button)

#         self.csv_data = self.load_csv_data("dummy_data.csv")

#     def load_csv_data(self, filename):
#         data = {}
#         with open(filename, 'r') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 data[row['image_name']] = {
#                     'Prediction': row['Prediction'],
#                     'gradcam_filepath': row['gradcam_filepath'],
#                     'Report': row['Report']
#                 }
#         return data

#     def browse_image(self):
#         global image_path, image_name
#         options = QFileDialog.Options()
#         filename, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)", options=options)
#         if filename:
#             image_path = filename
#             image_name = os.path.basename(filename)
#             self.display_image(image_path)

#     def display_image(self, filename):
#         pixmap = QPixmap(filename)
#         pixmap = pixmap.scaledToWidth(300)
#         self.image_label.setPixmap(pixmap)

#     def predict_image(self):
#         if not image_path:
#             return

#         if image_name in self.csv_data:
#             prediction = self.csv_data[image_name]['Prediction']
#             self.prediction_label.setText(f"Prediction: {prediction}")  # Set prediction text
#             if prediction == "Positive":
#                 self.prediction_label.setStyleSheet("color: red;")
#             elif prediction == "Normal":
#                 self.prediction_label.setStyleSheet("color: green;")

#     def display_gradcam(self):
#         if not image_path:
#             return

#         if image_name in self.csv_data and self.csv_data[image_name]['Prediction'] == "Positive":
#             gradcam_path = self.csv_data[image_name]['gradcam_filepath']
#             self.display_image(gradcam_path)

#     def generate_report(self):
#         if not image_path:
#             return

#         if image_name in self.csv_data:
#             report = self.csv_data[image_name]['Report']
#             self.report_label.setText(f"Report: {report}")  # Set report text


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = PneumoniaDiagnosisApp()
#     window.show()
#     sys.exit(app.exec_())


# import sys
# import csv
# import os
# from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog
# from PyQt5.QtGui import QPixmap

# image_path = ""
# image_name = ""

# class PneumoniaDiagnosisApp(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("Pneumonia Diagnosis")
#         self.setGeometry(100, 100, 800, 600)

#         self.central_widget = QWidget()
#         self.setCentralWidget(self.central_widget)
#         self.main_layout = QHBoxLayout()
#         self.central_widget.setLayout(self.main_layout)

#         self.image_label = QLabel(self)
#         self.image_label.setFixedSize(300, 300)
#         self.main_layout.addWidget(self.image_label)

#         self.gradcam_label = QLabel(self)
#         self.gradcam_label.setFixedSize(300, 300)
#         self.main_layout.addWidget(self.gradcam_label)

#         self.prediction_label = QLabel(self)
#         self.main_layout.addWidget(self.prediction_label)

#         self.report_label = QLabel(self)
#         self.main_layout.addWidget(self.report_label)

#         select_image_button = QPushButton("Select Image", self)
#         select_image_button.clicked.connect(self.browse_image)

#         predict_button = QPushButton("Predict Image", self)
#         predict_button.clicked.connect(self.predict_image)

#         gradcam_button = QPushButton("Gradcam", self)
#         gradcam_button.clicked.connect(self.display_gradcam)

#         generate_report_button = QPushButton("Generate Report", self)
#         generate_report_button.clicked.connect(self.generate_report)

#         self.button_layout = QVBoxLayout()
#         self.button_layout.addWidget(select_image_button)
#         self.button_layout.addWidget(predict_button)
#         self.button_layout.addWidget(gradcam_button)
#         self.button_layout.addWidget(generate_report_button)

#         self.main_layout.addLayout(self.button_layout)

#         self.csv_data = self.load_csv_data("dummy_data.csv")

#     def load_csv_data(self, filename):
#         data = {}
#         with open(filename, 'r') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 data[row['image_name']] = {
#                     'Prediction': row['Prediction'],
#                     'gradcam_filepath': row['gradcam_filepath'],
#                     'Report': row['Report']
#                 }
#         return data

#     def browse_image(self):
#         global image_path, image_name
#         options = QFileDialog.Options()
#         filename, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)", options=options)
#         if filename:
#             image_path = filename
#             image_name = os.path.basename(filename)
#             self.display_image(image_path)

#     def display_image(self, filename):
#         pixmap = QPixmap(filename)
#         pixmap = pixmap.scaledToWidth(300)
#         self.image_label.setPixmap(pixmap)

#     def predict_image(self):
#         if not image_path:
#             return

#         if image_name in self.csv_data:
#             prediction = self.csv_data[image_name]['Prediction']
#             self.prediction_label.setText(f"Prediction: {prediction}")  # Set prediction text
#             if prediction == "Positive":
#                 self.prediction_label.setStyleSheet("color: red;")
#             elif prediction == "Normal":
#                 self.prediction_label.setStyleSheet("color: green;")

#     def display_gradcam(self):
#         if not image_path:
#             return

#         if image_name in self.csv_data and self.csv_data[image_name]['Prediction'] == "Positive":
#             gradcam_path = self.csv_data[image_name]['gradcam_filepath']
#             self.display_gradcam_image(gradcam_path)

#     def display_gradcam_image(self, filename):
#         pixmap = QPixmap(filename)
#         pixmap = pixmap.scaledToWidth(300)
#         self.gradcam_label.setPixmap(pixmap)

#     def generate_report(self):
#         if not image_path:
#             return

#         if image_name in self.csv_data:
#             report = self.csv_data[image_name]['Report']
#             self.report_label.setText(f"Report: {report}")  # Set report text


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = PneumoniaDiagnosisApp()
#     window.show()
#     sys.exit(app.exec_())


import sys
import csv
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog
from PyQt5.QtGui import QPixmap, QPainter, QColor
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
        self.bottom_layout.addWidget(self.prediction_label)

        # Report text label
        self.report_label = QLabel(self)
        self.bottom_layout.addWidget(self.report_label)

        # Buttons
        select_image_button = QPushButton("Select Image", self)
        select_image_button.clicked.connect(self.browse_image)
        self.bottom_layout.addWidget(select_image_button)

        predict_button = QPushButton("Predict Image", self)
        predict_button.clicked.connect(self.predict_image)
        self.bottom_layout.addWidget(predict_button)

        gradcam_button = QPushButton("Gradcam", self)
        gradcam_button.clicked.connect(self.display_gradcam)
        self.bottom_layout.addWidget(gradcam_button)

        generate_report_button = QPushButton("Generate Report", self)
        generate_report_button.clicked.connect(self.generate_report)
        self.bottom_layout.addWidget(generate_report_button)

        # Load CSV data
        self.csv_data = self.load_csv_data("dummy_data.csv")

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

        if image_name in self.csv_data:
            prediction = self.csv_data[image_name]['Prediction']
            self.prediction_label.setText(f"Prediction: {prediction}")  # Set prediction text
            if prediction == "Positive":
                self.prediction_label.setStyleSheet("color: red;")
            elif prediction == "Normal":
                self.prediction_label.setStyleSheet("color: green;")

    # def display_gradcam(self):
    #     if not image_path:
    #         return

    #     if image_name in self.csv_data and self.csv_data[image_name]['Prediction'] == "Positive":
    #         gradcam_path = self.csv_data[image_name]['gradcam_filepath']
    #         self.display_gradcam_image(gradcam_path)
    def display_gradcam(self):
        if not image_path:
            return

        if image_name in self.csv_data and self.csv_data[image_name]['Prediction'] == "Positive":
            gradcam_path = self.csv_data[image_name]['gradcam_filepath']
            self.display_gradcam_image(gradcam_path)
        elif image_name in self.csv_data and self.csv_data[image_name]['Prediction'] == "Normal":
            self.display_blue_overlay()

    def display_gradcam_image(self, filename):
        pixmap = QPixmap(filename)
        pixmap = pixmap.scaledToWidth(300)
        self.gradcam_label.setPixmap(pixmap)

    def display_blue_overlay(self):
        blue_pixmap = QPixmap(300, 300)
        blue_pixmap.fill(QColor(0, 0, 255, 128))  # Transparent blue overlay
        self.gradcam_label.setPixmap(blue_pixmap)



    def generate_report(self):
        if not image_path:
            return

        if image_name in self.csv_data:
            report = self.csv_data[image_name]['Report']
            self.report_label.setText(f"Report: {report}")  # Set report text


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PneumoniaDiagnosisApp()
    window.show()
    sys.exit(app.exec_())
