import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import os
from advisor_logic import CareerAdvisorLogic

# Cache the logic module so loading models is fast
@st.cache_resource
def load_logic():
    # Only load if models exist
    if os.path.exists('best_model.pkl'):
        return CareerAdvisorLogic()
    return None

def apply_custom_css():
    st.markdown("""
        <style>
        /* Main background & typography */
        .stApp {
            background-color: #f8f9fa;
        }
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Inter', sans-serif;
            color: #1f2937;
        }
        /* Buttons */
        .stButton>button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(118, 75, 162, 0.3);
            color: white;
        }
        /* Metric Cards */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
            color: #4f46e5;
        }
        /* Containers */
        [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            border-radius: 8px 8px 0 0;
            padding: 10px 16px;
        }
        .stTabs [aria-selected="true"] {
            background-color: white !important;
            border-top: 3px solid #667eea !important;
        }
        /* Viva Explanation Box */
        .viva-box {
            background-color: #eef2ff;
            border-left: 5px solid #4f46e5;
            padding: 1.5rem;
            border-radius: 8px;
            margin-top: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

def plot_bar_chart(matched, missing):
    fig, ax = plt.subplots(figsize=(6, 4))
    categories = ['Matched Skills', 'Missing Skills']
    counts = [len(matched), len(missing)]
    colors = ['#2ecc71', '#e74c3c']
    
    ax.bar(categories, counts, color=colors, edgecolor='none', width=0.6, alpha=0.9)
    ax.set_ylabel('Count')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Add count labels on top
    for i, count in enumerate(counts):
        ax.text(i, count + 0.1, str(count), ha='center', va='bottom', fontweight='bold')
        
    fig.patch.set_alpha(0)  # Transparent background
    ax.set_facecolor('none')
    return fig

def plot_pie_chart(match_score):
    fig, ax = plt.subplots(figsize=(5, 5))
    labels = ['Matched', 'Missing']
    sizes = [match_score, max(0, 100 - match_score)]
    colors = ['#2ecc71', '#e74c3c']
    
    # Donut chart
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors, autopct='%1.1f%%', 
        startangle=90, pctdistance=0.85, textprops={'fontsize': 10, 'weight': 'bold', 'color': 'white'},
        wedgeprops=dict(width=0.4, edgecolor='w')
    )
    
    # Change outer label colors
    for text in texts:
        text.set_color('#1f2937')
        
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    fig.patch.set_alpha(0)
    ax.set_facecolor('none')
    return fig


def main():
    st.set_page_config(page_title="Career Advisor AI", layout="wide", page_icon="🎯")
    apply_custom_css()
    
    # Header Section
    with st.container():
        col1, col2 = st.columns([1, 11])
        with col1:
            st.image("https://cdn-icons-png.flaticon.com/512/1006/1006363.png", width=80) 
        with col2:
            st.title("Job Suitability & Skill Gap Analysis")
            st.markdown("Discover the best job roles for your profile, precisely analyze your skill gaps, and get a structured learning path! 🚀")
    
    st.markdown("---")
    
    logic = load_logic()
    if not logic:
        st.error("⚠️ **Models are not trained yet.** Please run `data_generator.py` and `model_trainer.py` to initialize the AI system.")
        return

    # Input Section
    st.markdown("### 📄 1. Profile Details")
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            skills_input = st.text_area("Your Skills (comma separated)", "python, sql, git, communication", height=110)
        with col2:
            education_input = st.selectbox("Education Level", ["btech", "bsc", "mtech", "mba", "diploma"])
            experience_input = st.slider("Years of Experience", min_value=0, max_value=10, value=2)
            
        st.write("") 
        analyze_btn = st.button("🚀 Analyze My Career Matches", use_container_width=True)
        
    if analyze_btn:
        if not skills_input.strip():
            st.warning("Please enter some skills to proceed!")
            return
            
        with st.spinner("Analyzing your profile..."):
            top_jobs = logic.predict_top_jobs(skills_input, education_input, experience_input)
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🎯 2. Career Predictions")
        
        # Display Top Jobs as metrics
        cols = st.columns(3)
        for i, (job, prob) in enumerate(top_jobs):
            with cols[i]:
                with st.container(border=True):
                    st.metric(label=f"Rank #{i+1}", value=job.title(), delta=f"{prob*100:.1f}% Match", delta_color="normal")
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📊 3. Skill Gap Analysis & Learning Paths")
        
        # Use Streamlit tabs for Jobs
        tabs = st.tabs([f"🌟 {job.title()}" for job, _ in top_jobs])
        
        for i, ((job, prob), tab) in enumerate(zip(top_jobs, tabs)):
            with tab:
                st.markdown(f"#### Deep Dive: {job.title()}")
                matched, missing, match_score = logic.analyze_skill_gap(skills_input, job)
                
                # Metrics row
                m1, m2, m3 = st.columns(3)
                with m1:
                    with st.container(border=True):
                        st.metric("Overall Match Score", f"{match_score:.1f}%")
                        st.progress(match_score / 100)
                with m2:
                    with st.container(border=True):
                        st.metric("Matched Skills", len(matched))
                with m3:
                    with st.container(border=True):
                        st.metric("Missing Skills", len(missing))
                
                # Visuals
                v1, v2 = st.columns(2)
                with v1:
                    with st.container(border=True):
                        st.markdown("**Skills Breakdown**")
                        if not matched and not missing:
                            st.info("No skills data available.")
                        else:
                            st.pyplot(plot_bar_chart(matched, missing), clear_figure=True)
                with v2:
                    with st.container(border=True):
                        st.markdown("**Skill Match Ratio**")
                        if match_score == 0 and len(matched) == 0 and len(missing) == 0:
                            st.info("No match data available.")
                        else:
                            st.pyplot(plot_pie_chart(match_score), clear_figure=True)
                    
                # Details
                st.markdown("#### 🧩 Profile Skills Match")
                if matched:
                    st.success(f"**✅ Your Strengths:** {', '.join(matched)}")
                else:
                    st.warning("⚠️ You don't have any of the core skills for this role yet.")
                
                # Learning path
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f"#### 🛣️ Structured Learning Path for {job.title()}")
                
                if len(missing) == 0:
                    st.balloons()
                    st.success("🎉 Incredible! You already possess all the core skills expected for this role.")
                else:
                    missing_importance = logic.get_skill_importance(job, missing)
                    ordered_missing = logic.get_learning_path(job, missing)
                    
                    st.info("Follow this prioritized learning path to maximize your chances of landing this job.")
                    
                    for index, step in enumerate(ordered_missing):
                        imp = "Medium"
                        for m_dict in missing_importance:
                            if m_dict['skill'] == step:
                                imp = m_dict['importance']
                                break
                                
                        with st.expander(f"📚 Step {index+1}: **{step.upper()}** (Priority: {imp})", expanded=True):
                            st.write(f"Focus on mastering **{step}**. It has a **{imp}** priority for the **{job.title()}** role.")
                            st.write(f"*[Recommended Action]*: Look for practical projects or specialized courses covering '{step}'.")


if __name__ == "__main__":
    main()
