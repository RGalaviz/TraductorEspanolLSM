import nltk
import speech_recognition as sr

nltk.download('punkt')
from nltk.tree import Tree

MY_GRAMMAR = """
    S -> NP VP | VP
    NP -> DET N | ADJ NP | N | PRON | NP PP
    VP -> V NP | V NP PP | VP ADV | ADJ VP
    PP -> P NP
    ADJ -> 'grande' | 'pequeño' | 'alto' | 'bajo' | 'suave' | 'fino' | 'áspero' | 'azul' | 'amarillo' | 'café' | 'gris' | 'negro' | 'naranja' | 'rojo' | 'morado' | 'verde' | 'rosa' | 'oscuro' | 'claro'
    DET -> 'el' | 'la' | 'los' | 'las' | 'su'
    N -> 'perro' | 'gato' | 'casa' | 'coche' | 'comida' | 'niño' | 'hombre' | 'mujer' | 'cosa' | 'pelo' | 'ojos' | 'nariz' | 'boca' | 'oreja' | 'frente' | 'cabeza' | 'ceja' | 'brazo' | 'dedos' | 'manos' | 'pecho' | 'abdomen' | 'pies' | 'cerebro' | 'lengua' | 'corazón' | 'pulmones' | 'hígado' | 'riñones' | 'intestinos' | 'apéndice' | 'vagina' | 'ovarios' | 'pene' | 'testículos' | 'barba' | 'bigote'
    V -> 'come' | 'corre' | 'duerme' | 'conduce' | 'ama' | 'canta' | 'baila' | 'habla' | 'es'
    P -> 'a' | 'de' | 'en' | 'con' | 'por'
    ADV -> 'bien' | 'mal' | 'rápido' | 'lentamente' | 'siempre' | 'nunca'
    PRON -> 'yo' | 'tú' | 'él' | 'ella' | 'nosotros' | 'ellos' | 'ustedes' | 'mío' | 'tuyo' | 'suyo' | 'de ella' | 'de ellos' | 'nuestro' | 'de ustedes'
"""

grammar = nltk.CFG.fromstring(MY_GRAMMAR)
parser = nltk.ChartParser(grammar)

def modify_sentence(oracion):
    tokens = nltk.word_tokenize(oracion.lower(), language='spanish')
    trees = list(parser.parse(tokens))
    if not trees:
        return None
    tree = trees[0]
    new_tokens = []
    for subtree in tree.subtrees():
        if subtree.label() == 'Det':
            continue
        elif subtree.label() == 'N':
            new_tokens.append(subtree.leaves()[0])
        elif subtree.label() == 'V':
            new_tokens.append(subtree.leaves()[0])
    return ' '.join(new_tokens)

def listen_and_process():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Diga algo:")
        audio = r.listen(source)
    try:
        print("Google Speech Recognition cree que has dicho: " + r.recognize_google(audio, language='es-ES'))
        modified_sentence = modify_sentence(r.recognize_google(audio, language='es-ES'))
        if modified_sentence:
            print("La oración modificada es:", modified_sentence)
        else:
            print("No se pudo modificar la oración.")
    except sr.UnknownValueError:
        print("Google Speech Recognition no pudo entender el audio.")
    except sr.RequestError as e:
        print("No se puede acceder al servicio de reconocimiento de voz de Google Speech Recognition; {0}".format(e))

listen_and_process()
