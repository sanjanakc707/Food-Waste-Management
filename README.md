# Food Spoilage Prediction & Management

## Overview

This project leverages machine learning to predict the spoilage timeline of various food items based on factors like category, storage conditions, temperature, and days since purchase. It aims to help users manage their food inventory efficiently, reduce waste, and promote sustainability by suggesting what to do with expired food.

---

## Features

- **Spoilage Prediction**: Estimates the number of days until a food item spoils.
- **Reuse Classification**: Categorizes expired items into 'feed', 'compost', or 'discard' based on spoilage severity.
- **Synthetic Dataset Generation**: Creates a diverse dataset simulating real-world food storage scenarios.
- **Model Training**: Uses Random Forest models for regression and classification.
- **Web Interface**: Users can input food data and get predictions through a web app.

---

## Technologies Used

### Backend
- **Flask (Python)**: Handles server-side logic, connects the machine learning models with the web interface, and sends predictions to users.

### Database
- **Joblib files**: Stores trained models (`regressor.joblib` and `classifier.joblib`) and encoders (`encoders.joblib`).  
- Can be extended to **SQLite, PostgreSQL, or Firebase** to store user data, food inventory, or prediction history.

### AI/ML Tools
- **Scikit-learn (sklearn)**:  
  - **RandomForestRegressor** → Predicts days until spoilage.  
  - **RandomForestClassifier** → Predicts reuse action (feed, compost, discard).  
  - **LabelEncoder** → Converts text labels into numerical values for models.
- **NumPy & Pandas**: Used for generating synthetic datasets and processing data.
- **Joblib**: Saves and loads trained models and encoders for easy integration into the web app.

---

## Setup & Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Food-Waste-Management.git
   cd Food-Waste-Management
