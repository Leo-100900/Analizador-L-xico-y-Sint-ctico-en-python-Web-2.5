import re

# Palabras clave y símbolos que se van a reconocer
keywords = {"for", "do", "while", "if", "else", "(", ")"}

# Función para analizar el código
def lexer(code):
    # Separar el código en palabras (tokens) usando expresiones regulares
    tokens = re.findall(r'\b\w+\b|[(){}]', code)
    
    for token in tokens:
        if token in keywords:
            print(f"Token encontrado: {token}")
        else:
            print(f"Error léxico: {token}")

# Ejemplo de código a analizar
codigo = "for (i = 0; i < 10; i++) { do_something(); } else { do_other(); }"

# Llamada al analizador léxico
lexer(codigo)
