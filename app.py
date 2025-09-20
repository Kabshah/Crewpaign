import streamlit as st
import subprocess
import sys
import os
from datetime import datetime
import asyncio
import nest_asyncio

# Apply nest_asyncio to fix event loop issues
nest_asyncio.apply()
# Page configuration
st.set_page_config(
    page_title="Crewpaign - AI Marketing Crew",
    page_icon="📈",
    layout="centered"
)

# Custom CSS - DARK THEME FIX
st.markdown("""
<style>
    body {
        background-color: #0e1117;
        color: #ffffff;
    }
    .main-header {
        font-size: 3rem;
        color: #ffffff;
        text-align: center;
        margin-bottom: 1rem;
    }
    .welcome-text {
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        color: #dcdcdc;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ffffff;
        margin-bottom: 1rem;
        text-align: center;
    }
    .input-container {
        background-color: #1e1e1e;
        padding: 25px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.6);
        color: #ffffff;
    }
    .input-title {
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 8px;
        color: #00bfff; /* light blue accent */
    }
    .success-box {
        background-color: #155724;
        color: #d4edda;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #721c24;
        color: #f8d7da;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .custom-button {
        background-color: #00bfff !important;
        color: white !important;
        font-weight: bold !important;
        width: 100% !important;
        font-size: 1.2rem !important;
        padding: 12px !important;
        border-radius: 8px !important;
        border: none !important;
    }
    .feature-card {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.6);
        text-align: center;
        color: #ffffff;
    }
    .how-to-use {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 8px;
        margin: 20px 0;
        color: #ffffff;
    }
    .footer {
        text-align: center;
        margin-top: 30px;
        padding: 15px;
        color: #aaaaaa;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Welcome section and tagline
st.markdown("""
<div style='text-align: center; margin: 20px 0;'>
    <h2 style="color:white;">Welcome to Crewpaign!</h2>
    <p class="welcome-text">Your AI-powered marketing crew that creates complete marketing strategies in minutes!</p>
</div>
""", unsafe_allow_html=True)

# Features in cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>📊 Market Research</h3>
        <p>Comprehensive analysis of your target market and competitors</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>✍️ Content Creation</h3>
        <p>Engaging blog posts, social media content, and scripts</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>🔍 SEO Optimization</h3>
        <p>Search engine optimized content for better visibility</p>
    </div>
    """, unsafe_allow_html=True)

# How to use section
st.markdown("""
<div class="how-to-use">
    <h3>📝 How to Use:</h3>
    <ol>
        <li><strong>Fill in your product details</strong> in the form below</li>
        <li><strong>Click 'Launch Marketing Campaign'</strong> button</li>
        <li><strong>Watch your AI crew work!</strong> - It will analyze and create strategies</li>
        <li><strong>Review and download the results</strong> for your marketing campaign</li>
    </ol>
</div>
""", unsafe_allow_html=True)

# Input form
with st.form("marketing_inputs"):
    st.markdown('<div class="sub-header">📋 Campaign Details</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="input-title">Product Name</div>', unsafe_allow_html=True)
        product_name = st.text_input("Product Name", "AI powered excel automation tool", label_visibility="collapsed")

        st.markdown('<div class="input-title">Target Audience</div>', unsafe_allow_html=True)
        target_audience = st.text_input("Target Audience", "Small and Medium Enterprises (SMEs)", label_visibility="collapsed")

    with col2:
        st.markdown('<div class="input-title">Budget</div>', unsafe_allow_html=True)
        budget = st.text_input("Budget", "Rs. 50,000", label_visibility="collapsed")

        st.markdown('<div class="input-title">Current Date</div>', unsafe_allow_html=True)
        current_date = st.date_input("Current Date", datetime.now(), label_visibility="collapsed")

    st.markdown('<div class="input-title">Product Description</div>', unsafe_allow_html=True)
    product_description = st.text_area(
        "Product Description",
        "A tool that automates repetitive tasks in Excel using AI, saving time and reducing errors.",
        label_visibility="collapsed", height=100
    )

    # Advanced options
    with st.expander("Advanced Options"):
        col3, col4 = st.columns(2)
        with col3:
            verbose_mode = st.checkbox("Verbose Mode", value=True)
        with col4:
            planning_enabled = st.checkbox("Enable Planning", value=True)

    # Run button
    run_crew = st.form_submit_button("🚀 Launch Marketing Campaign", use_container_width=True)

# If form is submitted
if run_crew:
    inputs = {
        "product_name": product_name,
        "target_audience": target_audience,
        "product_description": product_description,
        "budget": budget,
        "current_date": current_date.strftime("%Y-%m-%d")
    }

    st.markdown('<div class="sub-header">🎬 Running Marketing Crew...</div>', unsafe_allow_html=True)
    progress_bar = st.progress(0)
    status_text = st.empty()

    progress_bar.progress(20)
    status_text.text("Initializing marketing crew...")

    try:
        from crew import TheMarketingCrew

        progress_bar.progress(40)
        status_text.text("Setting up agents and tasks...")

        crew_instance = TheMarketingCrew()

        progress_bar.progress(60)
        status_text.text("Executing marketing strategy...")

        result = crew_instance.marketingcrew().kickoff(inputs=inputs)

        progress_bar.progress(100)
        status_text.text("Campaign completed successfully!")

        st.markdown('<div class="success-box">✅ Marketing campaign completed successfully!</div>', unsafe_allow_html=True)

        st.subheader("Campaign Results")
        st.write(result)

        st.download_button(
            label="📥 Download Results",
            data=str(result),
            file_name="marketing_campaign_results.txt",
            mime="text/plain"
        )

    except Exception as e:
        progress_bar.progress(100)
        st.markdown(f'<div class="error-box">⚠️ Error: {str(e)}</div>', unsafe_allow_html=True)
        st.error("The marketing crew encountered an error. Please check your inputs and try again.")

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    Built with ❤️ by Kabshah using CrewAI and Streamlit
</div>
""", unsafe_allow_html=True)
