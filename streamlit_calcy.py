# %%
import streamlit as st
from sly import Lexer, Parser

# ---- 🎨 Custom Style ----
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        background: linear-gradient(to right, #fffbe6, #fdf2f8);
    }

    h1 {
        color: #0f172a;
        text-shadow: 1px 1px 0px #facc15;
    }

    .stTextInput > div > div > input {
        background-color: #fff;
        border: 2px solid #a78bfa;
        padding: 12px;
        border-radius: 10px;
        color: #1e293b;
        font-size: 16px;
    }

    .stButton > button {
        background: linear-gradient(to right, #f59e0b, #ec4899);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        transition: 0.2s ease;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
    }

    .stButton > button:hover {
        background: linear-gradient(to right, #eab308, #d946ef);
        transform: scale(1.03);
    }

    .result-box {
        background: linear-gradient(to right, #d1fae5, #a7f3d0);
        padding: 16px;
        border-left: 5px solid #10b981;
        border-radius: 10px;
        font-weight: bold;
        color: #064e3b;
    }

    .error-box {
        background: linear-gradient(to right, #fee2e2, #fecaca);
        padding: 16px;
        border-left: 5px solid #ef4444;
        border-radius: 10px;
        font-weight: bold;
        color: #991b1b;
    }

    .footer {
        font-size: 15px;
        color: #6b7280;
        margin-top: 30px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- 🧠 Lexer & Parser (เหมือนเดิม) ----
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

# ---- 🌈 Streamlit UI ----
st.markdown("<h1 style='text-align:center;'>🧮 PLC Calculator 🎈</h1>", unsafe_allow_html=True)
st.markdown("### 🎨 Try Infix (2+3), Prefix (+ 2 3), or Postfix (2 3 +):")

expression = st.text_input("🔢 Enter your Expression:")

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
        st.markdown(f"<div class='error-box'>🚫 Error: {e}</div>", unsafe_allow_html=True)

st.markdown("<div class='footer'>💖 Coded with love — Have fun computing!</div>", unsafe_allow_html=True)
