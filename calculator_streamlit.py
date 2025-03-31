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
    precedence = (('left', PLUS, MINUS), ('left', TIMES, DIVIDE), ('right', 'UMINUS'))

    @_('expr') def statement(self, p): return p.expr
    @_('') def statement(self, p): return None
    @_('expr PLUS expr')   def expr(self, p): return p.expr0 + p.expr1
    @_('expr MINUS expr')  def expr(self, p): return p.expr0 - p.expr1
    @_('expr TIMES expr')  def expr(self, p): return p.expr0 * p.expr1
    @_('expr DIVIDE expr') def expr(self, p): return p.expr0 / p.expr1 if p.expr1 != 0 else "Error: Division by zero"
    @_('MINUS expr %prec UMINUS') def expr(self, p): return -p.expr
    @_('LPAREN expr RPAREN') def expr(self, p): return p.expr
    @_('NUMBER') def expr(self, p): return p.NUMBER

    def parse_postfix(self, expr):
        stack = []
        tokens = expr.split()
        for token in tokens:
            if token.lstrip('-').isdigit():
                stack.append(int(token))
            elif token in ('+', '-', '*', '/'):
                if len(stack) < 2: return "Error"
                b, a = stack.pop(), stack.pop()
                stack.append(a + b if token == '+' else a - b if token == '-' else a * b if token == '*' else a / b if b != 0 else "Error: Division by zero")
        return stack[0] if stack else "Error"

    def parse_prefix(self, expr):
        stack = []
        tokens = expr.split()[::-1]
        for token in tokens:
            if token.lstrip('-').isdigit():
                stack.append(int(token))
            elif token in ('+', '-', '*', '/'):
                if len(stack) < 2: return "Error"
                a, b = stack.pop(), stack.pop()
                stack.append(a + b if token == '+' else a - b if token == '-' else a * b if token == '*' else a / b if b != 0 else "Error: Division by zero")
        return stack[0] if stack else "Error"

# --- Streamlit UI ---
st.set_page_config(page_title="Fast Button Calculator", layout="centered")
st.title("🧮 Fast & Clear Calculator")

# State
if "expression" not in st.session_state:
    st.session_state.expression = ""

# Display (wider + scrollable if long)
st.text_area("Expression", value=st.session_state.expression, key="expr_display", height=80, disabled=True)

# Button logic
def append_to_expr(char):
    st.session_state.expression += char

def backspace():
    st.session_state.expression = st.session_state.expression[:-1]

def clear_expr():
    st.session_state.expression = ""

# Buttons grid
button_rows = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", "(", ")", "+"]
]

for row in button_rows:
    cols = st.columns(4)
    for i, btn in enumerate(row):
        if cols[i].button(btn, use_container_width=True):
            append_to_expr(btn)

# Bottom row
bottom_cols = st.columns([1, 1, 1])
if bottom_cols[0].button("AC"): clear_expr()
if bottom_cols[1].button("⌫"): backspace()

# Parser
parser = CalcParser()
lexer = CalcLexer()

# Evaluation buttons
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
