import re

# Palabras reservadas y paréntesis a reconocer
keywords = {"for", "do", "while", "if", "else"}
parentesis = {"(": "Paréntesis de apertura", ")": "Paréntesis de cierre"}

# Función para analizar el código
def lexer(code):
    # Separar el código en tokens usando expresiones regulares
    tokens = re.findall(r'\b\w+\b|[(){}]', code)
    
    for token in tokens:
        if token in keywords:
            print(f"Palabra reservada encontrada: {token}")
        elif token in parentesis:
            print(f"{parentesis[token]} encontrado: {token}")
        else:
            print(f"Error léxico: {token}")

# Ejemplo de código a analizar
codigo = "for (i = 0; i < 10; i++) { do_something(); } else { do_other(); }"

# Llamada al analizador léxico
lexer(codigo)
