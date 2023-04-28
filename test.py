import nltk
nltk.download('punkt')
from nltk.tree import Tree

# Definimos nuestra gramática personalizada
MY_GRAMMAR = """
    S -> NP VP | VP
    NP -> DET N | N | NP PP
    VP -> V NP | V NP PP | VP ADV
    PP -> P NP
    DET -> 'el' | 'la' | 'los' | 'las'
    N -> 'perro' | 'gato' | 'casa' | 'coche' | 'comida' | 'niño' | 'hombre' | 'mujer' | 'cosa'
    V -> 'come' | 'corre' | 'duerme' | 'conduce' | 'ama' | 'canta' | 'baila' | 'habla'
    P -> 'a' | 'de' | 'en' | 'con' | 'por'
    ADV -> 'bien' | 'mal' | 'rápido' | 'lentamente' | 'siempre' | 'nunca'
"""

# La gramática consiste en las siguientes reglas:
#  La regla inicial es S, que puede ser seguida por una NP y una VP o solo por una VP.
#  NP puede ser una determinante (DET) seguida de un sustantivo (N), solo un sustantivo o una NP seguida de una preposición y otra NP (PP).
#  VP puede ser un verbo (V) seguido de una NP, un verbo seguido de una NP y una PP, o una VP seguida de un adverbio (ADV).
#  PP es una preposición (P) seguida de una NP.
#  DET representa determinantes definidos en el idioma español.
#  N representa sustantivos comunes en el idioma español.
#  V representa verbos comunes en el idioma español.
#  P representa preposiciones comunes en el idioma español.
#  ADV representa adverbios comunes en el idioma español.

# Convertimos nuestra gramática personalizada en un formato que NLTK pueda entender
grammar = nltk.CFG.fromstring(MY_GRAMMAR)

# Creamos un parser para nuestra gramática
parser = nltk.ChartParser(grammar)

# Definimos una función que modifica una oración en español utilizando nuestra gramática personalizada
def modify_sentence(oracion):
    # Tokenizamos la oración en español
    tokens = nltk.word_tokenize(oracion.lower(), language='spanish')
    
    # Analizamos la oración en español utilizando nuestro parser
    trees = list(parser.parse(tokens))
    if not trees:
        return None
    
    # Obtenemos el árbol sintáctico de la primera solución encontrada
    tree = trees[0]
    
    # Recorremos los nodos del árbol para generar una nueva versión de la oración siguiendo las reglas de nuestra gramática personalizada
    new_tokens = []
    for subtree in tree.subtrees():
        if subtree.label() == 'Det':
            # Ignoramos los determinantes en la nueva versión de la oración
            continue
        elif subtree.label() == 'N':
            # Si encontramos un sustantivo, lo agregamos a la nueva versión de la oración sin artículo
            new_tokens.append(subtree.leaves()[0])
        elif subtree.label() == 'V':
            # Si encontramos un verbo, lo agregamos a la nueva versión de la oración sin cambio
            new_tokens.append(subtree.leaves()[0])
    print(tree)
    # Devolvemos la nueva versión de la oración
    return ' '.join(new_tokens)

# Ejemplo de uso
#sentence = input("Ingrese una oración en español: ")
oracion = "el perro come la comida"

modified_sentence = modify_sentence(oracion)
if modified_sentence:
    print("La oración modificada es:", modified_sentence)
else:
    print("No se pudo modificar la oración.")
