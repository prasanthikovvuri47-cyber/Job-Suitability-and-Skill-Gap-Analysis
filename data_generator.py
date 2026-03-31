import pandas as pd
import numpy as np
import json
import random

def generate_data():
    np.random.seed(42)
    random.seed(42)
    
    # Define prefixes and suffixes to generate 100+ job roles
    areas = ['Data', 'Frontend', 'Backend', 'Full Stack', 'Cloud', 'DevOps', 'Machine Learning', 
             'Security', 'Database', 'Mobile', 'AI', 'Network', 'UI/UX', 'Product', 'QA', 
             'System', 'Game', 'Embedded', 'Blockchain', 'Web3', 'Hardware', 'Firmware', 
             'AR/VR', 'Business', 'Marketing', 'GenAI', 'MLOps', 'Data Science', 'SRE',
             'Robotics', 'IoT', 'Prompt Engineering', 'Cybersecurity', 'Cloud Native']
    roles = ['Engineer', 'Developer', 'Analyst']
    
    job_roles = []
    for area in areas:
        for role in roles:
            job_roles.append(f"{area} {role}")
    # Base skills map
    base_skills = {
        'Data': ['sql', 'python', 'excel', 'tableau', 'statistics', 'pandas', 'numpy'],
        'Frontend': ['html', 'css', 'javascript', 'react', 'vue', 'angular', 'typescript'],
        'Backend': ['python', 'java', 'nodejs', 'c++', 'sql', 'django', 'spring'],
        'Full Stack': ['javascript', 'react', 'nodejs', 'mongodb', 'sql', 'express', 'git'],
        'Cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'linux', 'networking'],
        'DevOps': ['docker', 'kubernetes', 'jenkins', 'ci/cd', 'linux', 'bash', 'ansible'],
        'Machine Learning': ['python', 'tensorflow', 'pytorch', 'scikit-learn', 'math', 'mlflow'],
        'AI': ['python', 'pytorch', 'nlp', 'deep learning', 'keras', 'opencv', 'transformers'],
        'Security': ['linux', 'networking', 'cryptography', 'penetration testing', 'firewalls', 'kali linux'],
        'Network': ['tcp/ip', 'cisco', 'dns', 'routing', 'switching', 'linux', 'wireshark'],
        'Database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'database design', 'nosql'],
        'Mobile': ['java', 'kotlin', 'swift', 'flutter', 'react native', 'ios', 'android'],
        'UI/UX': ['figma', 'sketch', 'adobe xd', 'wireframing', 'prototyping', 'css'],
        'Product': ['agile', 'scrum', 'jira', 'product management', 'communication', 'user research'],
        'QA': ['selenium', 'cypress', 'testing', 'postman', 'java', 'python', 'jira'],
        'System': ['c', 'c++', 'linux', 'kernel', 'bash', 'os concepts', 'networking'],
        'Game': ['c++', 'c#', 'unity', 'unreal engine', '3d math', 'graphics', 'rendering'],
        'Embedded': ['c', 'c++', 'microcontrollers', 'rtos', 'electronics', 'assembly', 'iot'],
        'Blockchain': ['solidity', 'smart contracts', 'ethereum', 'web3', 'cryptography', 'rust'],
        'Web3': ['javascript', 'react', 'web3.js', 'ethers.js', 'solidity', 'blockchain'],
        'Hardware': ['electronics', 'verilog', 'vhdl', 'fpga', 'circuit design', 'c'],
        'Firmware': ['c', 'c++', 'assembly', 'microcontrollers', 'debugging', 'rtos'],
        'AR/VR': ['c#', 'c++', 'unity', 'unreal engine', '3d modeling', 'mathematics'],
        'Business': ['excel', 'sql', 'business analysis', 'communication', 'tableau', 'power bi'],
        'Marketing': ['seo', 'content strategy', 'google analytics', 'social media', 'communication', 'crm'],
        'GenAI': ['langchain', 'openai api', 'prompt engineering', 'huggingface', 'rag', 'vector databases', 'llm', 'python'],
        'MLOps': ['mlflow', 'kubeflow', 'airflow', 'model monitoring', 'docker', 'dvc', 'ci/cd', 'python'],
        'Data Science': ['r', 'statistics', 'a/b testing', 'feature engineering', 'hypothesis testing', 'python', 'tableau', 'sql'],
        'SRE': ['slo', 'sla', 'incident management', 'prometheus', 'grafana', 'chaos engineering', 'linux', 'python'],
        'Robotics': ['ros', 'python', 'c++', 'sensor fusion', 'kinematics', 'matlab', 'linux'],
        'IoT': ['arduino', 'raspberry pi', 'mqtt', 'c', 'sensors', 'edge computing', 'python', 'networking'],
        'Prompt Engineering': ['chatgpt', 'prompt design', 'llm fine-tuning', 'openai', 'langchain', 'python', 'nlp'],
        'Cybersecurity': ['ethical hacking', 'wireshark', 'kali linux', 'splunk', 'siem', 'owasp', 'networking', 'linux'],
        'Cloud Native': ['terraform', 'helm', 'istio', 'argocd', 'microservices', 'kubernetes', 'docker', 'service mesh']
    }
    
    # Generic skills for filling
    generic_skills = ['git', 'agile', 'problem solving', 'communication', 'teamwork', 'leadership', 'project management']

    learning_path_dict = {}
    skill_importance_dict = {}
    
    # Generate dictionaries for each job
    for job in job_roles:
        area = job.split(' ')[0]
        if area not in base_skills:
            area = job.split(' ')[0] + ' ' + job.split(' ')[1] if len(job.split(' ')) > 2 else 'Frontend'
            if area not in base_skills:
                area = random.choice(list(base_skills.keys()))
                
        core_skills = base_skills[area].copy()
        
        # Add some randomness per role
        additional = random.sample(generic_skills, k=3)
        # Learning path: sort core skills first, then additional
        learning_path = core_skills + [s for s in additional if s not in core_skills]
        learning_path_dict[job] = learning_path
        
        # Skill importance
        importance = {}
        for i, skill in enumerate(learning_path):
            if i < len(core_skills) // 2:
                importance[skill] = 'High'
            elif i < len(core_skills):
                importance[skill] = 'Medium'
            else:
                importance[skill] = 'Low'
        skill_importance_dict[job] = importance

    # Generate 5000 rows with some synthetic noise
    data = []
    educations = ['btech', 'bsc', 'mtech', 'mba', 'diploma']
    
    # Global irrelevant skills pool to introduce realistic noise
    irrelevant_skills_pool = [
        'photography', 'cooking', 'yoga', 'driving', 'public speaking', 
        'event planning', 'scuba diving', 'first aid', 'french', 'spanish',
        'knitting', 'woodworking', 'calligraphy', 'poker', 'chess'
    ]

    for _ in range(5000):
        target_job = random.choice(job_roles)
        req_skills = learning_path_dict[target_job]
        core_skills_list = req_skills[:len(req_skills)//2 + 1]  # the most important skills
        
        # Always include at least 2 core (high-importance) skills to ensure signal
        must_have = random.sample(core_skills_list, k=min(2, len(core_skills_list)))
        
        # Then optionally add more skills from the full required list
        remaining = [s for s in req_skills if s not in must_have]
        num_extra = random.randint(0, len(remaining))
        extra = random.sample(remaining, k=num_extra)
        user_skills_list = must_have + extra
        
        # TASK: Add 1-4 irrelevant skills (60% chance) to increase noise
        if random.random() < 0.6:
            num_irr = random.randint(1, 4)
            user_skills_list.extend(random.sample(irrelevant_skills_pool, k=num_irr))
            
        # Add generic skills
        if random.random() > 0.8:
            user_skills_list.append(random.choice(generic_skills))
            
        # Introduce synthetic noise for preprocessing demonstration
        random.shuffle(user_skills_list)
        skills_str = ", ".join(user_skills_list)
        
        noise_chance = random.random()
        if noise_chance < 0.1:
            skills_str = skills_str.upper() # Uppercase noise
        elif noise_chance < 0.2:
            skills_str = skills_str + "!!!" # Special character noise
        elif noise_chance < 0.3:
            skills_str = skills_str.replace("machine learning", "ML").replace("javascript", "JS")
        elif noise_chance < 0.4:
            skills_str = "   " + skills_str + "    " # Extra spaces
        elif noise_chance < 0.5:
            skills_str = skills_str.replace(",", " , ") # Extra spaces around commas
            
        education = random.choice(educations)
        
        # Adjust experience based roughly on education and job reality
        if education in ['mtech', 'mba']:
            exp = random.randint(2, 10)
        else:
            exp = random.randint(0, 10)
            
        # Introduce occasional NaN for preprocessing demonstration (2% chance)
        if random.random() < 0.02:
            skills_str = np.nan
        if random.random() < 0.02:
            exp = np.nan
            
        data.append({
            'skills': skills_str,
            'education': education,
            'experience': exp,
            'job_role': target_job
        })
        
    df = pd.DataFrame(data)
    
    # Intentionally duplicate some random rows to test 'drop_duplicates'
    duplicates = df.sample(n=50, replace=True, random_state=42)
    df = pd.concat([df, duplicates], ignore_index=True)
    
    # Save CSV
    df.to_csv("career_data.csv", index=False)
    print("Created career_data.csv with 5000 rows.")
    
    # Save JSON dicts
    with open("learning_path.json", "w") as f:
        json.dump(learning_path_dict, f, indent=4)
        
    with open("skill_importance.json", "w") as f:
        json.dump(skill_importance_dict, f, indent=4)
        
    print("Created all JSON dictionaries.")

if __name__ == "__main__":
    generate_data()
