import streamlit as st
from sly import Lexer, Parser

# Lexer
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

# Parser
class CalcParser(Parser):
    tokens = CalcLexer.tokens
    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ('right', 'UMINUS'),
    )

    @_('expr')
    def statement(self, p): return p.expr

    @_('')
    def statement(self, p): return None

    @_('expr PLUS expr')
    def expr(self, p): return p.expr0 + p.expr1

    @_('expr MINUS expr')
    def expr(self, p): return p.expr0 - p.expr1

    @_('expr TIMES expr')
    def expr(self, p): return p.expr0 * p.expr1

    @_('expr DIVIDE expr')
    def expr(self, p): return p.expr0 / p.expr1 if p.expr1 != 0 else "Error: Division by zero"

    @_('MINUS expr %prec UMINUS')
    def expr(self, p): return -p.expr

    @_('LPAREN expr RPAREN')
    def expr(self, p): return p.expr

    @_('NUMBER')
    def expr(self, p): return p.NUMBER

    def parse_postfix(self, expr):
        stack = []
        tokens = expr.split()
        for token in tokens:
            if token.lstrip('-').isdigit():
                stack.append(int(token))
            elif token in ('+', '-', '*', '/'):
                if len(stack) < 2: return "Error: Invalid Expression"
                b = stack.pop(); a = stack.pop()
                stack.append(eval(f"{a}{token}{b}") if token != '/' or b != 0 else "Error: Division by zero")
        return stack[0] if stack else "Error"

    def parse_prefix(self, expr):
        stack = []
        tokens = expr.split()[::-1]
        for token in tokens:
            if token.lstrip('-').isdigit():
                stack.append(int(token))
            elif token in ('+', '-', '*', '/'):
                if len(stack) < 2: return "Error: Invalid Expression"
                a = stack.pop(); b = stack.pop()
                stack.append(eval(f"{a}{token}{b}") if token != '/' or b != 0 else "Error: Division by zero")
        return stack[0] if stack else "Error"

# --- Streamlit UI ---
st.set_page_config(page_title="🧮 Button-Based Calculator", layout="centered")
st.title("🧮 Calculator with Buttons")
st.caption("Supports Infix, Prefix, Postfix")

# Session State Setup
if "expression" not in st.session_state:
    st.session_state.expression = ""

# Expression Display
st.text_input("Expression", value=st.session_state.expression, key="display", disabled=True)

# Button Layout
cols = st.columns(4)
buttons = [
    ("7", "8", "9", "/"),
    ("4", "5", "6", "*"),
    ("1", "2", "3", "-"),
    ("0", "(", ")", "+")
]

for row in buttons:
    cols = st.columns(4)
    for i, label in enumerate(row):
        if cols[i].button(label):
            st.session_state.expression += label

# Second row: Clear and Delete
cols2 = st.columns([1, 1, 1])
if cols2[0].button("AC"):
    st.session_state.expression = ""
elif cols2[1].button("⌫"):
    st.session_state.expression = st.session_state.expression[:-1]

# Mode Buttons
parser = CalcParser()
mode_cols = st.columns(3)

if mode_cols[0].button("🧠 Infix"):
    try:
        lexer = CalcLexer()
        tokens = iter(lexer.tokenize(st.session_state.expression))
        result = parser.parse(tokens)
        st.success(f"Infix Result: {result}")
    except Exception as e:
        st.error(f"Error: {e}")

if mode_cols[1].button("🔃 Prefix"):
    try:
        result = parser.parse_prefix(st.session_state.expression)
        st.success(f"Prefix Result: {result}")
    except Exception as e:
        st.error(f"Error: {e}")

if mode_cols[2].button("🔁 Postfix"):
    try:
        result = parser.parse_postfix(st.session_state.expression)
        st.success(f"Postfix Result: {result}")
    except Exception as e:
        st.error(f"Error: {e}")
