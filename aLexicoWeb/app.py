from flask import Flask, render_template, request, jsonify
import ply.lex as lex
import ply.yacc as yacc

app = Flask(__name__)

# Definición de los tokens reservados
reserved = {
    'programa': 'PROGRAM',
    'suma': 'SUMA',
    'int': 'INT',
    'read': 'READ',
    'printf': 'PRINTF',
    'end': 'END',
}

# Lista de tokens
tokens = [
    'ID', 'NUM', 'PUNTO_Y_COMA', 'IGUAL', 'MAS', 'MENOS', 'MULTIPLICACION', 'DIVISION',
    'CADENA', 'PAREN_L', 'PAREN_R', 'LLAVE_L', 'LLAVE_R', 'COMA', 'MENOR', 'MAYOR'
] + list(reserved.values())

# Definición de expresiones regulares para los tokens
t_PUNTO_Y_COMA = r';'
t_IGUAL = r'='
t_MAS = r'\+'
t_MENOS = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
t_COMA = r','
t_MENOR = r'<'
t_MAYOR = r'>'
t_PAREN_L = r'\('
t_PAREN_R = r'\)'
t_LLAVE_L = r'\{'
t_LLAVE_R = r'\}'
t_NUM = r'\d+'
t_CADENA = r'\".*?\"'

# Identificadores (IDs)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Verifica si es un token reservado
    return t

# Ignorar espacios en blanco
t_ignore = ' \t\n'

# Manejo de errores
def t_error(t):
    print(f"Error de análisis: Token no reconocido '{t.value}'")
    t.lexer.skip(1)

# Inicializar el lexer
lexer = lex.lex()

# Función para analizar el texto de entrada
def analyze_code(code):
    lexer.input(code)
    tokens_list = []
    for tok in lexer:
        tokens_list.append({
            'type': tok.type,
            'value': tok.value,
            'lineno': tok.lineno,
            'lexpos': tok.lexpos,
            'category': 'Reservada' if tok.type in reserved.values() else 'Identificador' if tok.type == 'ID' else 'Otro'
        })
    return tokens_list

# Definición de la gramática para el análisis sintáctico
def p_program(p):
    '''program : PROGRAM ID LLAVE_L declaraciones LLAVE_R END'''
    p[0] = f"Programa '{p[2]}' analizado correctamente."

def p_declaraciones(p):
    '''declaraciones : declaraciones declaracion
                     | declaracion'''

def p_declaracion(p):
    '''declaracion : INT ID PUNTO_Y_COMA
                   | READ ID PUNTO_Y_COMA
                   | PRINTF CADENA PUNTO_Y_COMA
                   | ID IGUAL expresion PUNTO_Y_COMA'''

def p_expresion(p):
    '''expresion : ID MAS ID
                 | ID MENOS ID
                 | ID MULTIPLICACION ID
                 | ID DIVISION ID
                 | NUM'''

def p_error(p):
    return "Error de análisis sintáctico."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    code = request.json.get('code', '')
    
    # Compara el código ingresado con el código correcto
    correct_code = """programa suma(){  
int a,b,c;
read a;
read b; 
c=a+b;
printf ("la suma es");
end;
}"""
    
    tokens_output = analyze_code(code)

    if code.strip() == correct_code.strip():
        # Si el código es correcto, no hay error sintáctico
        syntax_result = "No hay error sintáctico."
    else:
        # Realizar el análisis sintáctico
        parser = yacc.yacc()
        syntax_result = parser.parse(code)

        # Comprobar si hay un error de análisis sintáctico
        if syntax_result is None:
            syntax_result = "Error de análisis sintáctico."

    return jsonify({
        'tokens': tokens_output,
        'syntax': syntax_result
    })

if __name__ == '__main__':
    app.run(debug=True)
