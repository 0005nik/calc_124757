import streamlit as st
from sly import Lexer, Parser

# Lexer (Lexical Analysis)
class CalcLexer(Lexer):
    tokens = {NUMBER, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN}
    ignore = ' \t'

    NUMBER = r'-?\d+'
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    LPAREN = r'\('
    RPAREN = r'\)'

    def NUMBER(self, t):
        t.value = int(t.value)
        return t

# Parser (Syntax Analysis)
class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ('right', 'UMINUS'),
    )

    @_('expr')
    def statement(self, p):
        return p.expr

    @_('')
    def statement(self, p):
        return None

    @_('expr PLUS expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr MINUS expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    @_('expr TIMES expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr DIVIDE expr')
    def expr(self, p):
        return p.expr0 / p.expr1 if p.expr1 != 0 else "Error: Division by zero"

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return p.NUMBER

# UI Config
st.set_page_config(page_title="Calculator", page_icon="🧮", layout="centered")

st.markdown("""
<style>
body {
    background: linear-gradient(to right, #a1ffce, #faffd1);
    color: #222;
    font-family: 'Segoe UI', sans-serif;
}
.stApp {
    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 15px;
    padding: 30px;
    margin: 0 auto;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}
h1, .stMarkdown {
    text-align: center;
    color: #1a1a1a;
}
.stTextInput>div>div>input {
    font-size: 18px;
    text-align: center;
    background-color: #ffffff;
    color: #222;
    border: 2px solid #a3d2ca;
    border-radius: 8px;
    padding: 10px;
}
.stButton>button {
    background: #70c1b3;
    color: white;
    font-size: 18px;
    border-radius: 8px;
    padding: 10px 25px;
    border: none;
    cursor: pointer;
    transition: 0.3s ease;
}
.stButton>button:hover {
    background-color: #48b1a5;
}
.stAlert {
    font-size: 18px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# App Title and Input
st.title("🧮 Simple Calculator")
st.markdown("Enter your mathematical expression below and press Calculate.")

expression = st.text_input("Expression", placeholder="e.g., -3 + 5 * (2 - 1)")

if st.button("Calculate"):
    lexer = CalcLexer()
    parser = CalcParser()
    try:
        tokens = iter(lexer.tokenize(expression))
        result = parser.parse(tokens)
        st.success(f"✅ Result: {result}")
    except Exception as e:
        st.error(f"🚫 Error: {e}")
