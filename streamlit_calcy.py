st.markdown("""
<style>
/* Global background gradient and font */
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
    background: linear-gradient(135deg, #fdfcfb 0%, #e2d1c3 100%);
    color: #1e293b;
    transition: all 0.3s ease-in-out;
}

/* Title styling */
h1 {
    color: #1f2937;
    font-weight: 700;
    font-size: 42px;
    text-align: center;
    padding-bottom: 10px;
    margin-top: 0px;
}

/* Input field styling */
.stTextInput > div > div > input {
    background: rgba(255, 255, 255, 0.65);
    backdrop-filter: blur(5px);
    border: 2px solid #93c5fd;
    padding: 12px 14px;
    border-radius: 12px;
    color: #111827;
    font-size: 16px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

/* Button styling */
.stButton > button {
    background: linear-gradient(to right, #8b5cf6, #ec4899);
    color: white;
    font-weight: 600;
    font-size: 16px;
    border-radius: 12px;
    padding: 10px 24px;
    border: none;
    transition: 0.3s ease;
    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
}
.stButton > button:hover {
    background: linear-gradient(to right, #7c3aed, #f472b6);
    transform: scale(1.05);
}

/* Result box */
.result-box {
    background: rgba(240, 253, 244, 0.75);
    backdrop-filter: blur(8px);
    padding: 20px;
    border-left: 6px solid #10b981;
    border-radius: 14px;
    font-weight: 600;
    font-size: 18px;
    margin-top: 20px;
    color: #064e3b;
    box-shadow: 0 5px 12px rgba(0,0,0,0.07);
}

/* Error box */
.error-box {
    background: rgba(254, 226, 226, 0.75);
    backdrop-filter: blur(8px);
    padding: 20px;
    border-left: 6px solid #ef4444;
    border-radius: 14px;
    font-weight: 600;
    font-size: 18px;
    margin-top: 20px;
    color: #7f1d1d;
    box-shadow: 0 5px 12px rgba(0,0,0,0.07);
}

/* Footer */
.footer {
    font-size: 15px;
    color: #6b7280;
    margin-top: 40px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)
