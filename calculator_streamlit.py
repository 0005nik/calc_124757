# %%
import streamlit as st
from sly import Lexer, Parser

# 🎨 Custom Style
st.markdown("""
    <style>
    body {
        background-color: #fffefc;
    }
    .stTextInput > div > div > input {
        background-color: #fff8dc;
        color: #2c3e50;
        border: 2px solid #f4a261;
        font-size: 18px;
    }
    .stSelectbox > div {
        background-color: #fefae0 !important;
    }
    .stButton > button {
        background-color: #f4a261;
        color: white;
        font-weight: bold;
        font-size: 16px;
    }
    .stAlert > div {
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# 🧠 Lexer
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

# 🧠 Parser
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
                if len(stack) < 2:
                    return "❌ Error: Invalid Expression"
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
                if len(stack) < 2:
                    return "❌ Error: Invalid Expression"
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

    def simple_calculator(self, num1, num2, operation):
        try:
            num1, num2 = float(num1), float(num2)
            if operation == '+':
                return num1 + num2
            elif operation == '-':
                return num1 - num2
            elif operation == '*':
                return num1 * num2
            elif operation == '/':
                return num1 / num2 if num2 != 0 else "💥 Error: Division by zero"
        except ValueError:
            return "❌ Error: Invalid Input"

# 🧮 Streamlit UI
st.markdown("<h1 style='text-align:center;'>🧮✨ PLC Multi-Mode Calculator 🎈</h1>", unsafe_allow_html=True)
st.markdown("##### 💡 Choose a calculator mode to begin:")

# Mode Selector
calc_mode = st.selectbox("🧭 Select Mode", ["Simple Calculator", "Infix Notation", "Prefix Notation", "Postfix Notation"])

parser = CalcParser()

# 🧮 Mode: Simple Calculator
if calc_mode == "Simple Calculator":
    num1 = st.text_input("🔢 Enter first number:")
    num2 = st.text_input("🔢 Enter second number:")
    operation = st.selectbox("➕ Choose Operation", ["+", "-", "*", "/"])

    if st.button("🎯 Calculate"):
        result = parser.simple_calculator(num1, num2, operation)
        st.success(f"🧾 **Result**: `{result}`")

# 📘 Mode: Infix, Prefix, Postfix
else:
    expression = st.text_input("🧮 Enter Expression:")

    if st.button("🎯 Calculate"):
        try:
            if calc_mode == "Infix Notation":
                lexer = CalcLexer()
                tokens = iter(lexer.tokenize(expression))
                result = parser.parse(tokens)
                st.success(f"📘 **Infix Result**: `{result}`")

            elif calc_mode == "Postfix Notation":
                result = parser.parse_postfix(expression)
                st.success(f"📦 **Postfix Result**: `{result}`")

            elif calc_mode == "Prefix Notation":
                result = parser.parse_prefix(expression)
                st.success(f"🪄 **Prefix Result**: `{result}`")

        except Exception as e:
            st.error(f"🚫 Oops! Something went wrong: `{e}`")

st.markdown("---")
st.markdown("💬 _Supports: `Infix (e.g. 3 + 4)`, `Prefix (+ 3 4)`, and `Postfix (3 4 +)`_")
st.markdown("🔔 _Numbers only. For negative or decimal support, consider expanding the grammar._")
