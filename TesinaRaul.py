import re
import nltk
nltk.download('punkt')
from nltk.parse import EarleyChartParser

# Definimos una función que convierte reglas de gramática en formato string a una lista de tuplas
def convert_grammar(rules):
    grammar = []
    for rule in rules.split('\n'):
        rule = rule.strip()
        if rule:
            lhs, rhs = rule.split(' -> ')
            rhs = [r.strip() for r in rhs.split(' ')]
            grammar.append((lhs, rhs))
    return grammar

# Definimos nuestra gramática personalizada
MY_GRAMMAR = """
S -> NP VP
NP -> Det N | Det N PP
VP -> V NP | V NP PP
PP -> P NP
Det -> 'el' | 'la' | 'un' | 'una'
N -> 'perro' | 'gato' | 'ratón'
V -> 'persigue' | 'come' | 'duerme'
P -> 'en' | 'sobre'
"""

# Define una gramática simple
grammar = nltk.CFG.fromstring("""
S -> NP VP
NP -> Det N | Det N PP
VP -> V NP | V NP PP
PP -> P NP
Det -> 'el' | 'la' | 'un' | 'una'
N -> 'perro' | 'gato' | 'ratón'
V -> 'persigue' | 'come' | 'duerme'
P -> 'en' | 'sobre'
""")

# Convertimos nuestra gramática personalizada en un formato que NLTK pueda entender
GRAMMAR = convert_grammar(MY_GRAMMAR)

# Creamos un parser para nuestra gramática
parser = nltk.ChartParser(grammar)

# Definimos una función que analiza una oración en español y la traduce al inglés utilizando nuestra gramática
def translate(sentence):
    # Tokenizamos la oración en español
    tokens = nltk.word_tokenize(sentence.lower(), language='spanish')
    print(tokens)
    # Analizamos la oración en español utilizando nuestro parser
    trees = list(parser.parse(tokens))
    if not trees:
        return None
    
    # Obtenemos el árbol sintáctico de la primera solución encontrada
    tree = trees[0]
    
    # Generamos la traducción en inglés a partir del árbol sintáctico
    english = tree.label()['SEM']
    
    # Devolvemos la traducción en inglés
    return english

# Ejemplo de uso
sentence = input("Ingrese una oración en español: ")
english = translate(sentence)
if english:
    print("La traducción al inglés es:", english)
else:
    print("No se pudo traducir la oración.")
