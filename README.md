# Job Suitability Skill Gap Analysis

This is a complete, production-quality Machine Learning project that predicts the most suitable job role for a user and provides a detailed skill gap analysis along with a structured learning path.

## Project Structure

* `data_generator.py`: Generates a fully synthetic 5000-row dataset and creates necessary dictionaries (`job_skills`, `learning_path`, `skill_importance`) saved as JSON files.
* `model_trainer.py`: Preprocesses the synthetic dataset, uses TF-IDF for skills, encodes categorical inputs, trains Logistic Regression and Random Forest models, and exports the best model into `.pkl` format.
* `advisor_logic.py`: Contains the business logic integrating the Machine Learning models (for prediction) and Rule-Based logic (for skill gap extraction, calculating match scores, and ordering the learning paths).
* `app.py`: A user-friendly Streamlit web application providing a professional UI layout, including bar and pie charts via matplotlib.

## Instructions to Run

1. **Install Virtual Environment (Optional but recommended)**
```bash
python -m venv venv
.\venv\Scripts\activate
```

2. **Install Requirements**
```bash
pip install -r requirements.txt
```

3. **Generate Data and Dictionaries**
```bash
python data_generator.py
```
*(This will generate `career_data.csv`, `learning_path.json`, and `skill_importance.json`)*

4. **Train the Models**
```bash
python model_trainer.py
```
*(This will read `career_data.csv`, train the models, and output `.pkl` objects)*

5. **Run the Application**
```bash
streamlit run app.py
```

Open the provided Local URL in your browser, enter your career details, and click "Analyze Career" to get your predictions and custom learning path!
