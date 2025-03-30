# %%
import streamlit as st
from sly import Lexer, Parser

# ---- 🎨 Custom Style ----
st.markdown(
    """
    <style>
    .main {
        background-color: #fdf6e3;
        font-family: 'Comic Sans MS', cursive;
    }
    .stTextInput > div > div > input {
        background-color: #fffbe6;
        border: 2px solid #f39c12;
        color: #2c3e50;
    }
    .stButton > button {
        background-color: #f39c12;
        color: white;
        font-weight: bold;
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
st.markdown("<h1 style='text-align:center;'>🧮✨ PLC Calculator 🎈</h1>", unsafe_allow_html=True)
st.markdown("### 💬 Type your math expression below (Infix, Prefix, or Postfix)")

expression = st.text_input("🔢 Your Expression")

if st.button("🚀 Calculate"):
    lexer = CalcLexer()
    parser = CalcParser()
    try:
        if ' ' in expression:
            if expression.strip().startswith(('+', '-', '*', '/')):
                result = parser.parse_prefix(expression)
                st.success(f"🧠 **Prefix Result**: `{result}`")
            else:
                result = parser.parse_postfix(expression)
                st.success(f"📦 **Postfix Result**: `{result}`")
        else:
            tokens = iter(lexer.tokenize(expression))
            result = parser.parse(tokens)
            st.success(f"📘 **Infix Result**: `{result}`")
    except Exception as e:
        st.error(f"🚫 Something went wrong: `{e}`")

st.markdown("---")
st.markdown("🧑‍💻 _Supports Infix like `2+3`, Prefix like `+ 2 3`, and Postfix like `2 3 +`_")
st.markdown("💖 Created with love for math nerds 🎓")

