import streamlit as st
import matplotlib.pyplot as plt
import os
from advisor_logic import CareerAdvisorLogic

# Cache the logic module so loading models is fast
@st.cache_resource
def load_logic():
    # Only load if models exist
    if os.path.exists('best_model.pkl'):
        return CareerAdvisorLogic()
    return None

def plot_bar_chart(matched, missing):
    fig, ax = plt.subplots(figsize=(6, 4))
    categories = ['Matched Skills', 'Missing Skills']
    counts = [len(matched), len(missing)]
    ax.bar(categories, counts)
    ax.set_ylabel('Count')
    ax.set_title('Skills Breakdown')
    return fig

def plot_pie_chart(match_score):
    fig, ax = plt.subplots(figsize=(6, 6))
    labels = ['Matched', 'Missing']
    sizes = [match_score, max(0, 100 - match_score)]
    # Explode the matched slice slightly
    explode = (0.1, 0) if sizes[1] > 0 else (0, 0)
    ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    ax.set_title('Skill Match')
    return fig

def main():
    st.set_page_config(page_title="Job Suitability Skill Gap Analysis", layout="wide")
    
    st.title("🎯 Job Suitability Skill Gap Analysis")
    st.markdown("Discover the best job roles for you, analyze your skill gaps, and get a structured learning path! 🚀")
    st.markdown("---")
    
    logic = load_logic()
    if not logic:
        st.warning("Models are not trained yet. Please run `python data_generator.py` and `python model_trainer.py` to generate the system.")
        return

    st.header("1. Input Your Profile")
    
    col1, col2 = st.columns(2)
    with col1:
        skills_input = st.text_area("Your Skills (comma separated)", "python, sql, git, communication")
        education_input = st.selectbox("Education Level", ["btech", "bsc", "mtech", "mba", "diploma"])
        
    with col2:
        experience_input = st.slider("Years of Experience", min_value=0, max_value=10, value=2)
        st.write("") # spacing
        st.write("") 
        analyze_btn = st.button("🔍 Analyze Career", use_container_width=True)
        
    if analyze_btn:
        if not skills_input.strip():
            st.error("Please enter some skills!")
            return
            
        # Job Prediction
        top_jobs = logic.predict_top_jobs(skills_input, education_input, experience_input)
        
        st.markdown("---")
        st.header("2. Career Predictions")
        
        st.subheader("Top 3 Predicted Job Roles")
        for i, (job, prob) in enumerate(top_jobs):
            st.metric(f"#{i+1}: {job.title()}", f"{prob*100:.1f}% Confidence")
            
        st.markdown("---")
        st.header("3. Skill Gap Analysis & Learning Paths")
        
        # Use Streamlit tabs to organize the 3 jobs neatly
        tabs = st.tabs([f"#{i+1}: {job.title()}" for i, (job, _) in enumerate(top_jobs)])
        
        for i, ((job, prob), tab) in enumerate(zip(top_jobs, tabs)):
            with tab:
                st.subheader(f"Skill Gap Analysis for '{job.title()}'")
                matched, missing, match_score = logic.analyze_skill_gap(skills_input, job)
                
                # Metrics row
                m1, m2, m3 = st.columns(3)
                m1.metric("Match Score", f"{match_score:.1f}%")
                m2.metric("Matched Skills", len(matched))
                m3.metric("Missing Skills", len(missing))
                
                # Visualization Row
                st.write("**Visualizations**")
                v1, v2 = st.columns(2)
                with v1:
                    st.pyplot(plot_bar_chart(matched, missing))
                with v2:
                    st.pyplot(plot_pie_chart(match_score))
                    
                # detailed lists
                st.write("**Skill Details**")
                st.success(f"**Matched Skills:** {', '.join(matched) if matched else 'None'}")
                
                # Missing skills & Learning path
                st.markdown("---")
                st.subheader(f"Structured Learning Path for {job.title()}")
                
                if len(missing) == 0:
                    st.balloons()
                    st.success("🎉 You have all the core skills for this role! Great job.")
                else:
                    missing_importance = logic.get_skill_importance(job, missing)
                    ordered_missing = logic.get_learning_path(job, missing)
                    
                    # Map importance to color
                    color_map = {'High': '🔴 High', 'Medium': '🟡 Medium', 'Low': '🟢 Low'}
                    
                    st.write("Follow this ordered learning path to land your dream job:")
                    
                    for index, step in enumerate(ordered_missing):
                        # find importance
                        imp = "Medium"
                        for m_dict in missing_importance:
                            if m_dict['skill'] == step:
                                imp = m_dict['importance']
                                break
                                
                        st.markdown(f"**Step {index+1}:** `{step}` - Priority: {color_map.get(imp, imp)}")

if __name__ == "__main__":
    main()
