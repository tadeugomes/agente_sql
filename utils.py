import streamlit as st
import base64

def add_logo():
    """Add a logo to the sidebar"""
    st.sidebar.markdown(
        """
        <div style="text-align: center; margin-bottom: 20px;">
            <h1 style="color: #1E3A8A; font-size: 1.5rem;">SQL Agent</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

def local_css(file_name):
    """Load local CSS"""
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def inject_custom_css():
    """Inject custom CSS"""
    try:
        local_css("static/css/style.css")
    except:
        st.write("CSS file not found. Using default styles.")

def get_table_download_link(df, filename="data.csv", text="Download data as CSV"):
    """Generate a link to download the dataframe as a CSV file"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href
