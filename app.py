import streamlit as st

st.set_page_config(
    page_title="Data Transformer",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern look
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 3rem;
    }
    .feature-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 2rem;
        margin: 1rem;
        border-left: 5px solid #1E88E5;
        transition: transform 0.3s;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        padding: 0.75rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    .upload-section {
        background-color: #f0f2f6;
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main Page
st.markdown("<h1 class='main-header'>🔄 Data Transformer</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Transform your Excel data with ease. Concatenate rows or reverse the transformation.</p>", unsafe_allow_html=True)

# Navigation cards
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='feature-card'>
        <h3>📊 Concatenate Data</h3>
        <p>Consolidate rows with the same PartNumber and CompanyName into single rows with concatenated feature data.</p>
        <ul>
            <li>Groups by PartNumber + CompanyName</li>
            <li>Concatenates with "|" delimiter</li>
            <li>Skips blank cells</li>
            <li>Preserves "N/A" text</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Concatenation →", key="concat_btn", use_container_width=True):
        st.switch_page("pages/1_📊_Concatenate.py")

with col2:
    st.markdown("""
    <div class='feature-card'>
        <h3>↩️ Reverse Transformation</h3>
        <p>Convert concatenated data back to original format. Split Feature columns back into separate rows.</p>
        <ul>
            <li>Splits by "|" delimiter</li>
            <li>Restores original column structure</li>
            <li>Multiple rows per PartNumber</li>
            <li>Data integrity preserved</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Reverse →", key="reverse_btn", use_container_width=True):
        st.switch_page("pages/2_↩️_Reverse.py")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #666;'>Built with Streamlit • Data processing tool</p>", unsafe_allow_html=True)
