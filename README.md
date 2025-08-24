# Melanoma Detection AI Model

This project is an AI model to classify skin moles as **Benign** (non-cancerous) or **Malignant** (cancerous) using deep learning.

---

## Project Structure

melanoma_project/
├── predict.py           # Prediction script
├── my_model.keras       # Trained Keras model
├── requirements.txt     # Required Python libraries
├── README.md            # Project documentation
├── ISIC-images/         # Sample test images
└── reports/             # Optional: evaluation images or reports

---

## How to Install and Run

1. Install required libraries:

pip install -r requirements.txt


2. Run a prediction on a sample image:

python3 predict.py ISIC-images/sample_image.jpg


3. Output example:


1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 70ms/step
Prediction: Benign 


---

## Notes

- Model file: `my_model.keras`  
- Input: Skin mole images (JPG/PNG)  
- Output: Prediction (**Benign** or **Malignant**)

