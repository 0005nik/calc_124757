#  Calculator

## Overview
This is a simple yet powerful calculator built using Streamlit and SLY (Simple Lex-Yacc). The calculator supports:
- **Basic Arithmetic Operations** (Addition, Subtraction, Multiplication, Division)
- **Infix Notation** (Standard mathematical expressions like `3 + 4 * 5`)
- **Postfix Notation** (Reverse Polish Notation, e.g., `3 4 5 * +`)
- **Prefix Notation** (Polish Notation, e.g., `+ 3 * 4 5`)

## Features
- Accepts mathematical expressions in infix, prefix, and postfix notations.
- Automatically detects the notation based on input format.
- Uses SLY (Simple Lex-Yacc) for lexical and syntax analysis.
- Implements a stack-based approach for evaluating prefix and postfix expressions.
- Provides a user-friendly interface using Streamlit with an interactive button-based layout.
- Supports integer and floating-point calculations, including positive and negative values.
- Handles errors like division by zero gracefully.

## How It Works
### 1. Basic Calculator:
- Enter expressions like `3 + 5`, `10 - 2`, `6 * 7`, `8 / 2`.
- Click "Calculate" to see the result.
- Supports positive and negative integers.

### 2. Infix Notation:
- Example: `3 + 4 * 5` (evaluates as `3 + (4 * 5) = 23`).
- Standard operator precedence applies.

### 3. Postfix Notation:
- Example: `3 4 5 * +` (evaluates as `3 + (4 * 5) = 23`).
- Uses a stack to process operands and operators.

### 4. Prefix Notation:
- Example: `+ 3 * 4 5` (evaluates as `3 + (4 * 5) = 23`).
- Uses a reversed stack processing method.

## Grammar of the Language
The calculator application implements a custom grammar to parse and evaluate mathematical expressions. The grammar can be expressed in Backus-Naur Form (BNF) or Extended BNF (EBNF):
```
Expression  ::= Term ("+" | "-") Term)*
Term        ::= Factor ("*" | "/") Factor)*
Factor      ::= Number | "(" Expression ")"
Number      ::= [-]?[0-9]+ ("." [0-9]+)?
```
This grammar supports basic arithmetic operations such as addition, subtraction, multiplication, and division, along with parentheses for operator precedence. It also supports negative numbers.

## Type of the Parser
The project employs a **Bottom-Up (LR) parser** using **SLY (Simple Lex-Yacc)**. The parser follows an LALR(1) parsing technique, which is commonly used for expression evaluation in programming languages. The lexer tokenizes input expressions, generating tokens like `NUMBER`, `PLUS`, `MINUS`, `MULTIPLY`, and `DIVIDE`, which are then processed by the parser.

## Method of Translation and Integration of Parser and Translation
The translation method follows these steps:

1. **Lexical Analysis**:
   - The lexer processes the input and converts it into a series of tokens.
   - Example: Input `3 + 5` → Tokens: `NUMBER(3)`, `PLUS`, `NUMBER(5)`

2. **Parsing**:
   - The parser processes the tokenized input using LALR(1) parsing techniques.
   - The grammar rules define how tokens are grouped into expressions.
   - Example: `NUMBER(3) PLUS NUMBER(5)` → Expression → `Term + Term`

3. **Semantic Actions and Translation**:
   - The parser includes embedded actions to compute results.
   - Example: `3 + 5` is parsed and then evaluated as `3 + 5 = 8`.

4. **Integration with Streamlit**:
   - The parsed and evaluated expressions are integrated into the Streamlit UI.
   - Streamlit provides an interactive interface where users input expressions, which are then processed and displayed.

## Expected Outputs
| Notation | Expression | Evaluates To |
|----------|------------|-------------|
| Infix    | `3 + 4 * 5` | `23` |
| Postfix  | `3 4 5 * +` | `23` |
| Prefix   | `+ 3 * 4 5` | `23` |
| Basic    | `-5 + 3`    | `-2` |
| Basic    | `10 / -2`   | `-5` |

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/0005nik/calc_124757.git
   cd calculator
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the application:
   ```sh
   streamlit run app.py
   ```
Certainly! Here's a clear **"How to Use"** section you can add to your README (or use separately in documentation or a guide):

---

## 📗 How to Use the Calculator

This calculator is interactive and easy to use. Once the application is running, you’ll see a clean, user-friendly interface built with Streamlit.

### Step-by-Step Instructions

### 1. **Launch the Application**
- Open terminal or command prompt
- Run:
  ```bash
  streamlit run app.py
  ```
- This will open the app in your default web browser

---

### 2. **Choose Calculation Mode**
At the top of the interface, you’ll find a dropdown labeled:

```
Select Calculation Mode
```

Choose from:
- `Simple Calculator`
- `Infix Notation`
- `Postfix Notation`
- `Prefix Notation`

---

### 3. **Input Your Expression**
#### If you chose:

#### ✅ Simple Calculator:
- Two text fields will appear:
  - First Number
  - Second Number
- Choose an operation (`+`, `-`, `*`, `/`) from the dropdown
- Click the **"Calculate"** button to see the result

#### ✅ Infix Notation:
- Enter a math expression like:
  ```
  (3 + 4) * 5 - 2
  ```
- Then click **"Calculate"**

#### ✅ Postfix Notation:
- Enter a space-separated expression like:
  ```
  3 4 5 * +
  ```
- Then click **"Calculate"**

#### ✅ Prefix Notation:
- Enter a space-separated expression like:
  ```
  + 3 * 4 5
  ```
- Then click **"Calculate"**

---

### 4. **View the Result**
- If the expression is valid, the result will appear in a highlighted success box.
- If there's an error (e.g. division by zero or syntax error), an error message will be shown instead.

---

### 5. **Try More Expressions**
- Modify the expression or switch modes to evaluate more types.
- All interactions are instant and responsive in real-time thanks to Streamlit.

---

Let me know if you’d like this “How to Use” section added directly to your Word report or embedded into the code as a docstring.
## Future Improvements
- Add history tracking for calculations.
- Support for additional scientific operations.
- Mobile-friendly UI improvements.
