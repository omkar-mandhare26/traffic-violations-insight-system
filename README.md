# Traffic Violations Insight System

## Project Objective

The objective of this project is to transform a **large, raw traffic violations dataset** into a **clean, structured, and query-optimized analytics system**, and surface **actionable insights** through **Exploratory Data Analysis (EDA)** and an **interactive Streamlit dashboard**.

This project simulates a real-world analytics workflow used by **transport authorities, police departments, and urban planners** to analyze traffic violations, identify risk patterns, and support data-driven policy decisions.

---

## Project Execution Flow

Follow the steps below **in order** to successfully run the project end-to-end.

---

## Step 1: Download the Dataset

Download the dataset from the link below:

```
https://drive.google.com/drive/folders/1ZoS_lQQXKwJf-hfp--eLB-hPK5kKIC6k
```

### Dataset Placement

After downloading, place the dataset inside the following directory:

```
./dataset/
```

This step is mandatory, as all data processing notebooks expect the dataset at this location.

---

## Step 2: Clone the Repository

Clone the GitHub repository and move into the project directory:

```bash
git clone https://github.com/omkar-mandhare26/traffic-violations-insight-system.git
cd traffic-violations-insight-system
```

---

## Step 3: Environment Setup

### Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows
```

---

### Install Project Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

---

## Step 4: Environment Configuration

Create a `.env` file using the provided `.env.example` and update it with your database credentials:

```env
DB_HOST="your_DB_HOST"
DB_PORT="your_DB_PORT"
DB_USER="your_DB_USER"
DB_PASSWORD="your_DB_PASSWORD"
DB_NAME="your_DB_NAME"
```

This configuration is required for database connectivity during data ingestion and dashboard execution.

---

## Step 5: Data Cleaning & Database Ingestion

Run the data cleaning notebook:

```
python data_cleaning.ipynb
```

### What This Step Does

This notebook:

* Cleans and standardizes raw traffic violation data
* Handles inconsistencies and formatting issues
* Inserts the cleaned data into the configured SQL database

This step must be completed **before running the dashboard**.

---

## Step 6: Run the Streamlit Dashboard

Once the database is populated, launch the Streamlit application:

```bash
streamlit run app.py
```

---

## Step 7: Access the Dashboard

The interactive dashboard will be available at:

```
http://localhost:8501
```

You can now explore traffic violation trends, patterns, and insights through the visual analytics interface.

---
