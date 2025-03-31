import streamlit as st
from sly import Lexer, Parser

# Lexer (Lexical Analysis)
class CalcLexer(Lexer):
    tokens = {NUMBER, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN}
    ignore = ' \t'

    # Token definitions
    NUMBER = r'\d+'
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
    )

    @_('expr')
    def statement(self, p):
        return p.expr

    @_('')
    def statement(self, p):
        return None  # Handles empty input

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

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return p.NUMBER

# Streamlit UI Design
st.set_page_config(page_title="Calculator", page_icon="🧮", layout="centered")

st.markdown("""
<style>
body {
    background: linear-gradient(to right, #667eea, #764ba2);
    color: #FFFFFF;
    font-family: 'Segoe UI', sans-serif;
}
.stApp {
    background-color: rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    padding: 30px;
    margin: 0 auto;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}
h1, .stMarkdown {
    text-align: center;
    color: #ffffff;
}
.stTextInput>div>div>input {
    font-size: 18px;
    text-align: center;
    background-color: rgba(255,255,255,0.1);
    color: #ffffff;
    border: 2px solid #ffffff33;
    border-radius: 10px;
    padding: 12px;
}
.stButton>button {
    background-color: #ffffff33;
    color: #fff;
    font-size: 18px;
    border-radius: 10px;
    padding: 10px 24px;
    border: none;
    cursor: pointer;
    transition: 0.3s ease;
}
.stButton>button:hover {
    background-color: #ffffff55;
}
.stAlert {
    font-size: 18px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("🧮 Simple PLC Calculator")
st.markdown("Type any arithmetic expression and hit **Calculate**")

expression = st.text_input("Expression", placeholder="e.g., 3 + 5 * (2 - 1)")

if st.button("Calculate"):
    lexer = CalcLexer()
    parser = CalcParser()
    try:
        tokens = iter(lexer.tokenize(expression))
        result = parser.parse(tokens)
        st.success(f"✅ Result: {result}")
    except Exception as e:
        st.error(f"🚫 Error: {e}")
