📘 README — Multi-Mode Streamlit Calculator
Overview
This is a web-based calculator built using Python, Streamlit, and the SLY (Sly Lex-Yacc) parsing library.
It supports Infix, Prefix, Postfix, and Simple Calculator modes for evaluating arithmetic expressions.

Features
✅ Infix Expression Evaluation using LALR(1) parser

✅ Prefix and Postfix Evaluation using stack-based logic

✅ Simple Calculator for two-number operations

✅ Modern, colorful UI built with Streamlit

✅ Robust error handling for invalid expressions and division by zero

Technologies Used
Python 3.7+

Streamlit

SLY (Sly Lex-Yacc)

Grammar Definition
Tokens:

NUMBER: Integer (supports negative)

PLUS: +

MINUS: -

TIMES: *

DIVIDE: /

LPAREN: (

RPAREN: )

Grammar Rules:

bnf
Copy
Edit
<statement> ::= <expr> | ε
<expr> ::= <expr> + <expr>
         | <expr> - <expr>
         | <expr> * <expr>
         | <expr> / <expr>
         | -<expr>
         | ( <expr> )
         | NUMBER
Setup Instructions
Clone the repository or copy the code

Install dependencies

bash
Copy
Edit
pip install streamlit sly
Run the app

bash
Copy
Edit
streamlit run your_script_name.py
**How to Use
Choose a mode from the dropdown:

Simple Calculator (Enter two numbers and choose an operator)

Infix Notation (e.g., (3 + 4) * 2)

Prefix Notation (e.g., + 3 * 4 2)

Postfix Notation (e.g., 3 4 2 * +)

Input your expression or numbers.

Press Calculate to see the result.

File Structure
bash
Copy
Edit
├── calculator.py           # Main Streamlit application
├── Calculator_Application_Report.docx  # Formal report (theory + explanation)
├── README.md               # Project instructions and details
**
      
