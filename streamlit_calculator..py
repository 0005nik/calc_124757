# %%
import streamlit as st
from sly import Lexer, Parser

# ---- 🎨 Custom Streamlit Theme ----
st.markdown("""
    <style>
    body {
        background-color: #fff9f0;
    }
    .stTextInput > div > div > input {
        background-color: #fefae0;
        color: #2c3e50;
        border: 2px solid #f9a825;
        font-size: 18px;
        font-weight: bold;
    }
    .stButton > button {
        background-color: #f9a825;
        color: white;
        font-weight: bold;
        font-size: 16px;
    }
    .stAlert > div {
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# ---- 🧠 Lexer ----
class CalcLexer(Lexer):
    tokens = {NUMBER, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN}
    ignore = ' \t'

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

# ---- 🧠 Parser ----
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
        return p.expr0 / p.expr1 if p.expr1 != 0 else "💥 Error: Division by zero"

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return p.NUMBER

# ---- 🧮 Streamlit UI ----
st.markdown("<h1 style='text-align:center;'>🧮 Simple PLC Calculator 🎈</h1>", unsafe_allow_html=True)
st.markdown("### ✍️ _Enter your math expression using infix notation (e.g., 3 + 5 * (2 - 1))_")

expression = st.text_input("🔢 Expression:")

if st.button("✨ Calculate"):
    lexer = CalcLexer()
    parser = CalcParser()
    try:
        tokens = iter(lexer.tokenize(expression))
        result = parser.parse(tokens)
        st.success(f"🎉 **Result**: `{result}`")
    except Exception as e:
        st.error(f"🚫 Oops! Something went wrong: `{e}`")

st.markdown("---")
st.markdown("🤓 _Supports only **infix notation** (with parentheses too!)_ <br>💛 Have fun calculating!", unsafe_allow_html=True)
