import streamlit as st
from dotenv import load_dotenv
from streamlit_option_menu import option_menu
import os
import sys


sys.path.append("E:\\hk7\\5.CMPM\\chay thu")
load_dotenv()

import login
import recommend

st.set_page_config(
    page_title="Hotel Recommendation",
    page_icon=":tokyo_tower:"  # Biểu tượng tòa nhà
)

# Google Analytics
st.markdown(
    f"""
        <script async src="https://www.googletagmanager.com/gtag/js?id={os.getenv('analytics_tag')}"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            gtag('js', new Date());
            gtag('config', '{os.getenv("analytics_tag")}');
        </script>
    """, unsafe_allow_html=True
)

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self, selected):
        # Gọi hàm tương ứng với trang đã chọn
        for app in self.apps:
            if app['title'] == selected:
                app['function']()  # Gọi hàm tương ứng

# Chạy ứng dụng
if __name__ == "__main__":
    app = MultiApp()
    app.add_app("🔒 Login", login.main)  
    app.add_app("🕵️ Recommend", recommend.main)  

st.sidebar.markdown("<h2 style='font-size: 24px;'>🏨 Main Menu</h2>", unsafe_allow_html=True)
selected = st.sidebar.selectbox("Choose a page", ["🔒 Login", "🕵️ Recommend"])
    
    # st.sidebar.markdown("## Main Menu")
    # selected = st.sidebar.selectbox("Choose a page", ["Login", "Recommend"])

    # Gọi phương thức run() với trang đã chọn
app.run(selected)