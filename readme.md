# 🥇 EduPulse AI: Student Success Platform

✨ **Project Mission**:
“The objective of this project is to analyze student academic data and predict future performance and risk levels using machine learning models, and to provide explainable and personalized feedback using generative AI.”

## 🚀 How to Run the Project

### 1. Start the Backend (FastAPI)
```bash
.\venv\Scripts\uvicorn backend.core.main:app --reload --port 8000
```

### 2. Start the Frontend (Streamlit)
```bash
.\venv\Scripts\streamlit run frontend\streamlit_app.py
```

📌 Why this matters:

Keeps project focused

Prevents scope creep

Helps in viva & documentation

✅ STEP 0.2: Define the Stakeholders (WHO uses it?)

Write this clearly:

Student → wants to know performance & how to improve

Teacher → wants to identify weak students early

Admin → wants overall academic insights

📌 This justifies dashboards and features.

✅ STEP 0.3: Lock the INPUT FEATURES (VERY IMPORTANT)

Based on your dataset, finalize exact inputs.

🔹 Inputs (Features):

Attendance percentage

Assignment average score

Quiz average score

Midterm exam score

Previous semester score

❗ Important rule:

These features must NEVER change later
They affect ML, backend, and frontend.

✅ STEP 0.4: Lock the OUTPUTS (What system produces)
🔹 ML Outputs:

Predicted final score (number)

Risk level (Safe / At Risk / Critical)

🔹 GenAI Outputs:

Explanation of prediction

Improvement suggestions

📌 Now your system has a clear purpose.

✅ STEP 0.5: Decide the ML Tasks (Freeze this)

Write this clearly:

Regression task → Predict final score

Classification task → Predict risk level

📌 This decides algorithms, metrics, evaluation.

✅ STEP 0.6: Define Success Criteria (How do we know it works?)

Very important for exams/interviews.

✨ Example success criteria:

Regression model RMSE is reasonably low

Classification accuracy > baseline

Predictions make logical sense

GenAI explanations are understandable

📌 You don’t need perfection, only justification.

✅ STEP 0.7: Freeze Tech Stack (You already chose it 👍)

Write this once and don’t change it:

Frontend → Streamlit

Backend → FastAPI

Database → SQLite

ML → Scikit-learn

GenAI → OpenAI API

✅ STEP 0.8: Define Project Boundaries (What NOT included)

This saves you from overthinking.

❌ Out of scope:

Real-time data streaming

Large-scale cloud deployment

Deep learning models

Real student privacy handling

📌 Saying “out of scope” is a GOOD thing.