# calc_124757

## Overview
This is a simple yet powerful calculator built using Streamlit and SLY (Simple Lex-Yacc). The calculator supports:

1. **Basic Arithmetic Operations** (Addition, Subtraction, Multiplication, Division)
2. **Infix Notation** (Standard mathematical expressions like `3 + 4 * 5`)
3. **Postfix Notation** (Reverse Polish Notation, e.g., `3 4 5 * +`)
4. **Prefix Notation** (Polish Notation, e.g., `+ 3 * 4 5`)
5. **Error Handling** for invalid expressions and division by zero.

## Features
- Accepts mathematical expressions in **infix, prefix, and postfix notations**.
- Automatically detects the notation based on input format.
- Uses **SLY (Simple Lex-Yacc)** for lexical and syntax analysis.
- Implements a **stack-based approach** for evaluating prefix and postfix expressions.
- Provides a **user-friendly interface** using Streamlit.
- Handles **invalid expressions gracefully** with error messages.
- Supports **real-time computation** with a clean and interactive UI.

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/streamlit-calculator.git
   cd streamlit-calculator
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
Run the Streamlit application using:
```sh
streamlit run app.py
```

## How It Works
1. **Basic Calculator:**
   - Enter expressions like `3 + 5`, `10 - 2`, `6 * 7`, `8 / 2`.
   - Click "Calculate" to see the result.

2. **Infix Notation:**
   - Example: `3 + 4 * 5` (evaluates as `3 + (4 * 5) = 23`).

3. **Postfix Notation:**
   - Example: `3 4 5 * +` (evaluates as `3 + (4 * 5) = 23`).
   - Uses a stack to process operands and operators.

4. **Prefix Notation:**
   - Example: `+ 3 * 4 5` (evaluates as `3 + (4 * 5) = 23`).
   - Uses a reversed stack processing method.

5. **Error Handling:**
   - Invalid expressions return meaningful error messages.
   - Division by zero is prevented with a warning message.

## Example Calculations
| Notation  | Expression    | Evaluates To |
|-----------|--------------|--------------|
| Infix     | `3 + 4 * 5`  | `23`         |
| Postfix   | `3 4 5 * +`  | `23`         |
| Prefix    | `+ 3 * 4 5`  | `23`         |
| Postfix   | `3 5 4 + *`  | `27`         |
| Prefix    | `* 3 + 5 4`  | `27`         |

## Technologies Used
- **Python**
- **Streamlit** (for UI)
- **SLY** (for lexical and syntax analysis)



