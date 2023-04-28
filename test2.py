import nltk
from nltk import CFG
from nltk.parse import RecursiveDescentParser

# Definir la gramática personalizada
gramatica = CFG.fromstring("""
    S -> NP VP
    NP -> DET N
    VP -> V NP
    DET -> 'el' | 'la' | 'los' | 'las'
    N -> 'perro' | 'gato' | 'casa' | 'coche' | 'comida'
    V -> 'come' | 'corre' | 'duerme' | 'conduce'
""")

# La primera línea S -> NP VP establece que la categoría sintáctica "S" (sintagma nominal) se puede construir a partir 
# de la combinación de un sintagma nominal "NP" (que puede contener un determinante y un sustantivo) y un sintagma verbal "VP" (que puede contener un verbo y un sintagma nominal).

# La segunda línea NP -> DET N establece que un sintagma nominal (NP) puede ser un determinante (DET) seguido por un sustantivo (N).

# La tercera línea VP -> V NP establece que un sintagma verbal (VP) puede ser un verbo (V) seguido por un sintagma nominal (NP).

# Las siguientes tres líneas establecen que los determinantes (DET), sustantivos (N) y verbos (V) son símbolos terminales, es decir, 
# palabras concretas en el lenguaje que no se pueden descomponer en partes más pequeñas.

# Crear un objeto RecursiveDescentParser con la gramática personalizada
parser = RecursiveDescentParser(gramatica)

# Definir una oración para analizar
oracion = "el perro come la comida"

# Pasar la oración al analizador sintáctico (parser) y obtener el árbol sintáctico resultante
arbol = list(parser.parse(oracion.split()))

# Imprimir el árbol sintáctico resultante
print(arbol[0])
