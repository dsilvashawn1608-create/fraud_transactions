# fraud_transactions
this is an Ml model that detects anomolies whithin the transactions and detect the fraud transactions.
🏦 Bank Fraud Detection System using Machine Learning

An end-to-end machine learning–based fraud detection system that identifies fraudulent bank transactions using historical data.
The project integrates ML models, a Python backend API, MongoDB for data storage, Redis for performance optimization, and a web-based frontend.

📌 Problem Statement

With the rise of digital banking, fraudulent transactions have increased significantly. Manual detection is inefficient and error-prone.
This project aims to automatically detect suspicious transactions using machine learning classification techniques.

🎯 Objectives

Detect fraudulent bank transactions accurately

Build a real-world ML pipeline (training → testing → deployment)

Expose predictions through a REST API

Store and manage transaction data efficiently

Improve performance using caching

🧠 Machine Learning Approach

Type: Binary Classification

Labels: Fraud / Not Fraud

Train-Test Split: 80% Training, 20% Testing

Models Used

Logistic Regression

Random Forest Classifier (primary model)

Evaluation Metrics

Accuracy

Precision

Recall

Confusion Matrix

🛠️ Tech Stack
Backend

Python

FastAPI

Scikit-learn

Pandas

NumPy

Joblib

Database & Caching

MongoDB

Redis

Frontend

HTML

CSS

JavaScript

Tools

Git & GitHub

VS Code

Docker (optional)

🗂️ Project Structure
bank-fraud-detection/
│
├── backend/
│   ├── main.py              # FastAPI server
│   ├── train_model.py       # Model training script
│   ├── predict.py           # Prediction logic
│   ├── fraud_model.pkl      # Saved ML model
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── database/
│   └── mongodb_setup.py
│
├── requirements.txt
├── README.md
└── .gitignore

⚙️ Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/your-username/bank-fraud-detection.git
cd bank-fraud-detection

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Start Services

Make sure MongoDB and Redis are running locally.

4️⃣ Train the Model
python backend/train_model.py

5️⃣ Run Backend API
uvicorn backend.main:app --reload

6️⃣ Open Frontend

Open frontend/index.html in your browser.

🔌 API Endpoint
Predict Fraud

POST /predict

Request Body (JSON):

{
  "amount": 12000,
  "transaction_type": 1,
  "old_balance": 15000,
  "new_balance": 3000
}


Response:

{
  "fraud": true
}

📈 Results

Achieved reliable accuracy on test data

Random Forest performed better than Logistic Regression

Redis significantly reduced repeated prediction latency

🔮 Future Enhancements

Real-time transaction streaming

Deep learning models

User authentication

Dashboard with analytics & graphs

Cloud deployment (AWS / GCP)

👤 Author

Shawn D’silva
BSc Cyber Security (Honors in Computer Science)

📜 License

This project is for academic and learning purposes.
