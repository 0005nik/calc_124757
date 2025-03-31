# %%
import streamlit as st
from sly import Lexer, Parser

# ---- 🎨 Custom Style ----
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        background-color: #fefce8;
    }

    h1, h3 {
        color: #1e293b;
    }

    .stTextInput > div > div > input {
        background-color: #fff;
        border: 2px solid #fbbf24;
        padding: 10px;
        border-radius: 8px;
        color: #1e293b;
        font-size: 16px;
    }

    .stButton > button {
        background-color: #f59e0b;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 8px 16px;
        font-size: 16px;
        transition: background-color 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #d97706;
    }

    .stMarkdown {
        font-size: 18px;
    }

    .result-box {
        background-color: #ecfccb;
        padding: 16px;
        border-left: 5px solid #65a30d;
        border-radius: 8px;
        font-weight: bold;
        color: #365314;
    }

    .error-box {
        background-color: #fee2e2;
        padding: 16px;
        border-left: 5px solid #dc2626;
        border-radius: 8px;
        font-weight: bold;
        color: #991b1b;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

    def parse_postfix(self, expr):
        stack = []
        tokens = expr.split()
        for token in tokens:
            if token.isdigit():
                stack.append(int(token))
            elif token in ('+', '-', '*', '/'):
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    stack.append(a / b if b != 0 else "💥 Error: Division by zero")
        return stack[0] if stack else "❌ Error: Invalid Expression"

    def parse_prefix(self, expr):
        stack = []
        tokens = expr.split()[::-1]
        for token in tokens:
            if token.isdigit():
                stack.append(int(token))
            elif token in ('+', '-', '*', '/'):
                a = stack.pop()
                b = stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    stack.append(a / b if b != 0 else "💥 Error: Division by zero")
        return stack[0] if stack else "❌ Error: Invalid Expression"

# ---- 🎨 Streamlit UI ----
st.markdown("<h1 style='text-align:center;'>🧮 PLC Calculator 🎈</h1>", unsafe_allow_html=True)
st.markdown("### 💬 Enter an expression (Infix, Prefix, or Postfix):")

expression = st.text_input("🔢 Your Expression")

if st.button("🚀 Calculate"):
    lexer = CalcLexer()
    parser = CalcParser()
    try:
        if ' ' in expression:
            if expression.strip().startswith(('+', '-', '*', '/')):
                result = parser.parse_prefix(expression)
                st.markdown(f"<div class='result-box'>🧠 <strong>Prefix Result</strong>: {result}</div>", unsafe_allow_html=True)
            else:
                result = parser.parse_postfix(expression)
                st.markdown(f"<div class='result-box'>📦 <strong>Postfix Result</strong>: {result}</div>", unsafe_allow_html=True)
        else:
            tokens = iter(lexer.tokenize(expression))
            result = parser.parse(tokens)
            st.markdown(f"<div class='result-box'>📘 <strong>Infix Result</strong>: {result}</div>", unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f"<div class='error-box'>🚫 Something went wrong: {e}</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("🧑‍💻 _Supports Infix (`2+3`), Prefix (`+ 2 3`), and Postfix (`2 3 +`)_")
st.markdown("💖 Made for Math Enthusiasts with ✨")
