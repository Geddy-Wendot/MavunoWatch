![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![License](https://img.shields.io/badge/license-Private-red)
![Streamlit](https://img.shields.io/badge/Built%20With-Streamlit-ff4b4b)
![ML Model](https://img.shields.io/badge/Model-RandomForest-green)
![Status](https://img.shields.io/badge/status-MVP%20Complete-brightgreen)


# 🌾 MavunoWatch - AI-Powered Kenyan Agricultural Intelligence System

**MavunoWatch** is an AI-driven food production monitoring and prediction system tailored for Kenya's counties. Built by [Geddy Wendot](https://github.com/Geddy-Wendot) under **Trivium Technology Group**, this MVP forecasts crop yield trends, detects food production risks, and empowers policy-makers and farmers with actionable intelligence.



## 🧠 Features

- 📂 Upload CSV datasets for food production
- 🧹 Auto-cleans data and generates new features
- 📊 Trains machine learning models (Random Forest)
- 📈 Predicts crop yield per hectare
- 🖥️ Interactive dashboard via Streamlit
- ✅ Fully modular and reproducible architecture


## 🖼️ Dashboard Preview

![Dashboard Screenshot](.Screenshot 2025-06-20 194404.png/)


## 📦 Folder Structure

mavunowatch/
├── data/ # Raw agricultural data (CSV)
├── notebooks/ # Jupyter notebooks (EDA, experiments)
├── src/ # Python scripts
│ ├── data_cleaning.py # Data preprocessing & feature engineering
│ ├── model_training.py # ML training & evaluation
├── models/ # Saved .pkl model files
├── dashboard/ # Streamlit frontend
│ └── dashboard.py
├── requirements.txt # Project dependencies
├── README.md # You’re reading this
└── .gitignore




## 🗂️ Sample Dataset

```csv
County,Year,Crop,Production_Tons,Area_Ha,Rainfall_mm,Market_Price_KES
Bungoma,2020,Maize,184000,32000,1100,42
Uasin Gishu,2020,Wheat,61000,19000,980,55
Meru,2021,Beans,90000,21000,1120,68
Trans Nzoia,2022,Maize,212000,34000,1050,45
Kirinyaga,2022,Rice,47000,8000,1200,70
🚀 Run Locally
1. Clone & Navigate

git clone https://github.com/Geddy-Wendot/MavunoWatch.git
cd MavunoWatch
2. Create & Activate Virtual Environment

python -m venv venv
venv\Scripts\activate   # On Windows
3. Install Dependencies

pip install -r requirements.txt
4. Train Model

python src/model_training.py
5. Run Dashboard

streamlit run dashboard/dashboard.py
📊 Tech Stack
Python – Core language

Pandas / NumPy – Data manipulation

Scikit-learn / joblib – Model training & persistence

Streamlit – Dashboard frontend

Jupyter – EDA & exploration

🔐 License


© 2025 Geddy Wendot / Trivium Technology Group. All rights reserved.
Unauthorized use, reproduction, or modification is strictly prohibited.
💼 Author & Credits
👤 Geddy Wendot
🛡 Cyber-AI Architect & Founder
🌐 Trivium Technology Group
🐙 GitHub: @Geddy-Wendot

Engineering Africa’s Digital Future, one algorithm at a time.


