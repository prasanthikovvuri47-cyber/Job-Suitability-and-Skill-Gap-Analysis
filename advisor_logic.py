import json
import pickle
import numpy as np

class CareerAdvisorLogic:
    def __init__(self):
        # Load encoders/models
        with open("best_model.pkl", "rb") as f:
            self.model = pickle.load(f)
        with open("tfidf_vectorizer.pkl", "rb") as f:
            self.tfidf = pickle.load(f)
        with open("edu_encoder.pkl", "rb") as f:
            self.edu_encoder = pickle.load(f)
        with open("target_encoder.pkl", "rb") as f:
            self.target_encoder = pickle.load(f)
            
        # Load dictionaries
        with open("learning_path.json", "r") as f:
            self.learning_path = json.load(f)
        with open("skill_importance.json", "r") as f:
            self.skill_importance = json.load(f)
            
    def predict_top_jobs(self, skills_str, education, experience):
        # Clean skills
        skills_clean = skills_str.lower().strip()
        
        # Transform inputs
        sk_tfidf = self.tfidf.transform([skills_clean]).toarray()
        
        # Handle unknown education gracefully
        try:
            edu_enc = self.edu_encoder.transform([education.lower()])[0]
        except:
            edu_enc = 0
            
        X_input = np.hstack((sk_tfidf, [[edu_enc]], [[experience]]))
        
        # Predict probabilities
        probs = self.model.predict_proba(X_input)[0]
        top_3_idx = np.argsort(probs)[-3:][::-1]
        
        top_jobs = []
        for idx in top_3_idx:
            job_name = self.target_encoder.inverse_transform([idx])[0]
            prob = probs[idx]
            top_jobs.append((job_name, prob))
            
        return top_jobs

    def analyze_skill_gap(self, user_skills_str, target_job):
        user_skills = set([s.strip().lower() for s in user_skills_str.split(',') if s.strip()])
        req_skills_list = self.learning_path.get(target_job, [])
        req_skills = set(req_skills_list)
        
        matched_skills = user_skills.intersection(req_skills)
        missing_skills = req_skills.difference(user_skills)
        
        match_score = 0
        if len(req_skills) > 0:
            match_score = (len(matched_skills) / len(req_skills)) * 100
            
        return list(matched_skills), list(missing_skills), match_score

    def get_learning_path(self, target_job, missing_skills):
        ordered_path = self.learning_path.get(target_job, [])
        # Ordered missing skills
        final_path = [skill for skill in ordered_path if skill in missing_skills]
        return final_path
        
    def get_skill_importance(self, target_job, missing_skills):
        importance_map = self.skill_importance.get(target_job, {})
        result = []
        for skill in missing_skills:
            imp = importance_map.get(skill, 'Medium')
            result.append({'skill': skill, 'importance': imp})
        return result
