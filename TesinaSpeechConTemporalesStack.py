import nltk
import speech_recognition as sr
import spacy

nlp = spacy.load("es_core_news_sm")


nltk.download('punkt')
from nltk.tree import Tree

MY_GRAMMAR = """
    S -> VP | VP NP | NP VP | NP V
    NP -> DET N | ADJ NP | N | PRON | NP PP | 
    VP -> V NP | V NP PP | VP ADV | ADJ VP | V ADV | VP TIEM | V TIEM
    PP -> P NP
    ADJ -> 'grande' | 'pequeño' | 'alto' | 'bajo' | 'suave' | 'fino' | 'áspero' | 'azul' | 'amarillo' | 'café' | 'gris' | 'negro' | 'naranja' | 'rojo' | 'morado' | 'verde' | 'rosa' | 'oscuro' | 'claro'
    DET -> 'el' | 'la' | 'los' | 'las' | 'su'
    N -> 'perro' | 'gato' | 'casa' | 'coche' | 'comida' | 'niño' | 'hombre' | 'mujer' | 'cosa' | 'pelo' | 'ojos' | 'nariz' | 'boca' | 'oreja' | 'frente' | 'cabeza' | 'ceja' | 'brazo' | 'dedos' | 'manos' | 'pecho' | 'abdomen' | 'pies' | 'cerebro' | 'lengua' | 'corazón' | 'pulmones' | 'hígado' | 'riñones' | 'intestinos' | 'apéndice' | 'vagina' | 'ovarios' | 'pene' | 'testículos' | 'barba' | 'bigote'
    V -> 'ejercitar' | 'trabajar' | 'dormir' | 'comer' | 'bailar' | 'estudiar' | 'visitar' | 'caminar' | 'correr' | 'saltar' | 'dibujar' | 'escribir' | 'leer' | 'criticar' | 'bañar' | 'pelear' | 'discutir' | 'dialogar' | 'ordenar' | 'hacer' | 'cocinar' | 'beber' | 'jugar' | 'ver' | 'llamar' | 'robar' | 'esconder' | 'comprar' | 'lavar' | 'limpiar' | 'poner' | 'quitar' | 'cambiar' | 'avisar' | 'ganar' | 'perder' | 'esperar' | 'ir' | 'preparar' | 'tirar' | 'salvar' | 'escapar'    
    P -> 'a' | 'de' | 'en' | 'con' | 'por'
    ADV -> 'bien' | 'mal' | 'rápido' | 'lentamente' | 'siempre' | 'nunca' 
    PRON -> 'yo' | 'tú' | 'él' | 'ella' | 'nosotros' | 'ellos' | 'ustedes' | 'mío' | 'tuyo' | 'suyo' | 'de ella' | 'de ellos' | 'nuestro' | 'de ustedes'
    TIEM -> 'ayer' | 'hoy' | 'mañana' | 'antier' | 'futuro' | 'pasado' | 'ahorita' | 'ya' | 'acaba de pasar' | 'antiguo' | 'horario' | 'próximo' | 'en la mañana' | 'tarde' | 'noche' | 'nuevo' | 'viejo' | 'tiempo'
"""

grammar = nltk.CFG.fromstring(MY_GRAMMAR)
parser = nltk.ChartParser(grammar)
terminals = set(rule.rhs()[0] for rule in grammar.productions() if len(rule.rhs()) == 1 and isinstance(rule.rhs()[0], str))


def modify_sentence(oracion):
    doc = nlp(oracion)

    for token in doc:
        if token.pos_ == 'VERB':
            infinitive = token.lemma_
            break
    print("Infinitivo del verbo: ", infinitive)
    # Reemplazamos el verbo en infinitivo en la oración
    new_text = oracion.replace(token.text, infinitive)

    # Nueva oración a procesar
    print("New oración-> ", new_text)

    tokens = nltk.word_tokenize(new_text.lower(), language='spanish')
    try:
        trees = list(parser.parse(tokens))
        if not trees:
            print("No se pudo reconocer con las reglas gramática.")
            return new_text
    except ValueError:
        print("Error: ValueError. Se mandó algo con una palabra no en la gramática")
        return new_text
    tree = trees[0]
    new_tokens = []
    for subtree in tree.subtrees():
        if subtree.label() == 'DET':
            continue
        elif subtree.label() == 'N':
            new_tokens.append(subtree.leaves()[0])
        elif subtree.label() == 'V':
            new_tokens.append(subtree.leaves()[0])
        elif subtree.label() == 'TIEM' and subtree.leaves()[0] in ['ayer', 'hoy', 'mañana', 'antier', 'futuro', 'pasado', 'ahorita', 'ya', 'acaba de pasar', 'antiguo', 'horario', 'próximo', 'en la mañana', 'tarde', 'noche', 'nuevo', 'viejo', 'tiempo']:
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