import streamlit as st
from sly import Lexer, Parser

# ---------- Lexer ----------
class CalcLexer(Lexer):
    tokens = {NUMBER, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN}
    ignore = ' \t'

    # Regular expressions
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

# ---------- Parser ----------
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

    # Evaluate Postfix
    def parse_postfix(self, expr):
        stack = []
        tokens = expr.split()
        for token in tokens:
            if token.lstrip('-').isdigit():
                stack.append(int(token))
            elif token in ('+', '-', '*', '/'):
                if len(stack) < 2:
                    return "Error"
                b, a = stack.pop(), stack.pop()
                try:
                    result = a + b if token == '+' else a - b if token == '-' else a * b if token == '*' else a / b
                except ZeroDivisionError:
                    return "Error: Division by zero"
                stack.append(result)
        return stack[0] if stack else "Error"

    # Evaluate Prefix
    def parse_prefix(self, expr):
        stack = []
        tokens = expr.split()[::-1]
        for token in tokens:
            if token.lstrip('-').isdigit():
                stack.append(int(token))
            elif token in ('+', '-', '*', '/'):
                if len(stack) < 2:
                    return "Error"
                a, b = stack.pop(), stack.pop()
                try:
                    result = a + b if token == '+' else a - b if token == '-' else a * b if token == '*' else a / b
                except ZeroDivisionError:
                    return "Error: Division by zero"
                stack.append(result)
        return stack[0] if stack else "Error"

# ---------- Streamlit App ----------
st.set_page_config(page_title="🧮 Calculator", layout="centered")
st.title("🧮 Multi-Mode Calculator (Infix / Prefix / Postfix)")

# Expression state
if "expression" not in st.session_state:
    st.session_state.expression = ""

# Display expression (multiline supported)
st.text_area("Expression", value=st.session_state.expression, height=75, key="display", disabled=True)

# Button logic
def append(char):
    st.session_state.expression += char

def clear():
    st.session_state.expression = ""

def backspace():
    st.session_state.expression = st.session_state.expression[:-1]

# Number + operator buttons
rows = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", "(", ")", "+"],
]

for row in rows:
    cols = st.columns(4)
    for i, btn in enumerate(row):
        if cols[i].button(btn, use_container_width=True):
            append(btn)

# Control buttons: AC, ⌫
ctrl_cols = st.columns([1, 1, 2])
if ctrl_cols[0].button("AC"):
    clear()
if ctrl_cols[1].button("⌫"):
    backspace()

# Evaluation buttons: Infix / Prefix / Postfix
parser = CalcParser()
lexer = CalcLexer()
eval_cols = st.columns(3)

if eval_cols[0].button("🧠 Infix", use_container_width=True):
    try:
        tokens = iter(lexer.tokenize(st.session_state.expression))
        result = parser.parse(tokens)
        st.success(f"Infix Result: {result}")
    except Exception as e:
        st.error(f"Error: {e}")

if eval_cols[1].button("🔁 Postfix", use_container_width=True):
    try:
        result = parser.parse_postfix(st.session_state.expression)
        st.success(f"Postfix Result: {result}")
    except Exception as e:
        st.error(f"Error: {e}")

if eval_cols[2].button("🔃 Prefix", use_container_width=True):
    try:
        result = parser.parse_prefix(st.session_state.expression)
        st.success(f"Prefix Result: {result}")
    except Exception as e:
        st.error(f"Error: {e}")
