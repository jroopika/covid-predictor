# 🦠 COVID-19 Risk Predictor 🌐

This is a full-featured Flask web application that predicts the risk of COVID-19 based on symptoms using a trained Machine Learning model. It supports user login/signup, saves prediction history, and visualizes symptoms using a pie chart.

## 🔧 Features

- ✅ **User Registration & Login** with Flask-Login
- 🔐 **Client-side and Server-side validation** for email and password
- 📊 **COVID-19 Risk Prediction** using a Decision Tree model
- 📈 **Pie Chart Visualization** of symptoms using Chart.js
- 📁 **Stores prediction history** in SQLite (with timestamps)
- 👤 **User Dashboard** to view all previous predictions
- 🎨 **Modern, Responsive UI** with Bootstrap + Custom CSS
- 🔒 **Session management** (Logout disables back button access)

---

## 📂 Project Structure
covid_symptom_checker/
│
├── app.py # Main Flask app
├── train_model.py # Script to train & save model
├── model/
│ ├── data.csv # Dataset used for training
│ └── covid_model.pkl # Trained model
│
├── templates/
│ ├── landing.html # Cute landing page
│ ├── login.html
│ ├── register.html
│ ├── index.html # Prediction + chart
│ └── dashboard.html # Prediction history
│
├── static/
│ └── style.css # All CSS styles (form, chart, dashboard)
│
├── requirements.txt
└── README.md

---

## 💾 Dataset (`model/data.csv`)

Sample CSV used:
```csv
Fever,Tiredness,Dry-Cough,Difficulty-in-Breathing,Sore-Throat,Age,COVID-19
1,1,1,0,1,25,1
0,1,0,0,0,30,0
1,0,1,1,1,45,1
0,0,0,0,0,22,0
1,1,1,1,1,60,1
0,0,1,0,0,18,0
1,1,0,1,1,50,1
0,0,0,0,1,28,0

How to Run the Project
1. Clone the repo
git clone https://github.com/jroopika/covid-predictor
cd covid-predictor
2. Create virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
3. Install required packages
pip install -r requirements.txt
4. Train the ML model
python train_model.py
5. Run the Flask app
python app.py
6. Open in Browser
Visit: http://127.0.0.1:5000

## 🔐 Validations
Email validation using RegEx (client-side)

Password strength (min 6 characters + includes letters & digits)

Session logout disables back button access

Each user sees their own prediction history only


📜 License
MIT License – free for personal/academic use.

Created By
Roopika Juluru- roopikajuluru4@gmail.com


About the Project
Built as a full-stack academic + passion project using:

Python + Flask (backend)
SQLite + SQLAlchemy (storage)
HTML/CSS + Bootstrap (frontend)
ML model: Decision Tree (trained using scikit-learn)

Feel free to ⭐ star the repo and suggest improvements!
---


