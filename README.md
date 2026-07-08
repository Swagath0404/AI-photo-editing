# 🤖 AI-Based Photo Editing Application

## Overview
The AI-Based Photo Editing Application is a desktop/web application developed using Python and Streamlit. It combines traditional image editing features with AI-powered image enhancement to improve image quality and provide an interactive editing experience.

---

## Features

- User Registration & Login
- AI-based Image Enhancement
- Brightness Adjustment
- Contrast Adjustment
- Saturation Control
- Sharpness Adjustment
- Image Rotation
- Grayscale Filter
- Invert Filter
- Undo Functionality
- Redo Functionality
- Save Edited Images

---

## Technologies Used

### Programming Language
- Python

### Framework
- Streamlit

### AI / Machine Learning
- TensorFlow
- OpenCV DNN Super Resolution

### Image Processing
- OpenCV
- Pillow
- NumPy

---

## Project Structure

AI-Photo-Editor/

│── app.py

│── s2_model_training.py

│── s3_image_enhancement.py

│── models/

│      └── EDSR_x2.pb

│── dataset/

│── output/

│── users.txt

│── requirements.txt

│── README.md

│── .gitignore

---

## Installation

1. Clone the repository

```
git clone <repository-url>
```

2. Move to project directory

```
cd AI-Photo-Editor
```

3. Install dependencies

```
pip install -r requirements.txt
```

4. Run the application

```
streamlit run app.py
```

---

## AI Model

The application uses:

- TensorFlow
- OpenCV Super Resolution (EDSR x2)

for AI-based image enhancement.

---

## Dataset

The model is trained using paired low-quality and enhanced images.

Dataset structure:

dataset/

├── input/

└── enhanced/

---

## Output

Edited images are saved inside:

output/

---

## Future Enhancements

- Face Beautification
- Background Removal
- Cartoon Filter
- AI Object Removal
- Batch Image Editing
- Cloud Storage

---

## Contributors

- Your Friend's Name

---

## License

This project is developed for educational purposes.