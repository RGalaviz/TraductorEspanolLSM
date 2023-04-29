import nltk
import speech_recognition as sr
import spacy
import tkinter as tk
import vlc
import os

nlp = spacy.load("es_core_news_sm")


nltk.download('punkt')
from nltk.tree import Tree

# crear la ventana
window = tk.Tk()
window.geometry("500x500")

# inicializar el reproductor de VLC
instance = vlc.Instance()
player = instance.media_player_new()
media_list = vlc.MediaList()

"DET N V P DET L"
"NP VP"
"DET N V "
MY_GRAMMAR = """
    S -> VP | VP NP | NP VP | NP V | NP ADJ
    NP -> N ADJ | DET N | ADJ NP | N | PRON | NP PP | L | DET L | P | P NP | P TIEM 
    VP -> V NP | V NP PP | VP NP ADJ | ADJ VP | V ADV | VP TIEM | V TIEM 
    PP -> P NP 
    ADJ -> "cero" | "uno" | "dos" | "tres" | "cuatro" | "cinco" | "seis" | "siete" | "ocho" | "nueve" | "diez" | "once" | "doce" | "trece" | "catorce" | "quince" | "dieciséis" | "diecisiete" | "dieciocho" | "diecinueve" | "veinte" | "treinta" | "cuarenta" | "cincuenta" | "sesenta" | "setenta" | "ochenta" | "noventa" | "cien" | "doscientos" | "trescientos" | "cuatrocientos" | "quinientos" | "seiscientos" | "setecientos" | "ochocientos" | "novecientos" | "mil" | "diez mil" | "cien mil" | "un millón" | 'chaparro' | 'gordo' | 'flaco' | 'guapo' | 'feo' | 'rubio' | 'moreno' | 'pelirrojo' | 'pecoso' | 'grande' | 'pequeño' | 'alto' | 'bajo' | 'sobre'| 'abajo' | 'adentro' | 'afuera' | 'enfrente' | 'atrás' | 'esférico' | 'plano' |'suave' | 'fino' | 'áspero' | 'azul' | 'amarillo' | 'café' | 'gris' | 'negro' | 'naranja' | 'rojo' | 'morado' | 'verde' | 'rosa' | 'oscuro' | 'claro'
    DET -> 'el' | 'la' | 'los' | 'las' | 'su' | 'mi'
    N -> 'mes' | 'pelo' | 'ojos' | 'nariz' | 'boca' | 'oreja' | 'frente' | 'cabeza' | 'ceja' | 'hombro' | 'brazo' | 'dedos' | 'manos' | 'pecho' | 'abdomen' | 'pies' | 'cerebro' | 'lengua' | 'corazon' | 'pulmones' | 'higado' | 'riñones' | 'intestino' | 'apendice' | 'vagina' | 'ovarios' | 'pene' | 'testiculos' | 'barba' | 'bigote' | "maestro" | "mesero" | "arquitecto" | "doctor" | "ingeniero" | "abogado" | "psicologo" | "empresario" | "policia" | "soldador" | "enfermero" | "carpintero" | "carro" | "pelota" | "telefono" | "dinero" | "ropa" | "juguete" | "plato" | "estufa" | "bicicleta" | "jabon" | "sacapuntas" | "llave" | "espejo" | "computadora" | "papel" | "zapato" | "mesa" | "silla" | "sombrero" | "tenis" | "puerta" | "calceta" | "cuaderno" | "lapiz" | "toalla" | "vaso" | "pluma" |  'hombre' | 'mujer' | 'sobrino' | 'suegro' | 'compadre' | 'ahijado' | 'amante' | 'abuelo' | 'hijo' | 'primo' | 'nuera' | 'comadre' | 'novio' | 'soltero' | 'papá' | 'nieto' | 'hermano' | 'yerno' | 'padrino' | 'padrastro' | 'casado' | 'mamá' | 'tio' | 'cuñado' | 'madrina' | 'madrastra' | 'esposo' | 'viudo'
    L -> 'parque' | 'cine' | 'escuela' | 'biblioteca' | 'oficina' | 'casa' | 'baño' | 'salon' | 'calle' | 'laguna' | 'presa' | 'mar' | 'alberca' | 'campo' | 'fabrica' | 'restaurante' | 'tienda' | 'museo' | 'iglesia' | 'hospital' | 'centro'
    V -> 'ejercitar' | 'trabajar' | 'dormir' | 'comer' | 'bailar' | 'estudiar' | 'visitar' | 'caminar' | 'correr' | 'saltar' | 'dibujar' | 'escribir' | 'leer' | 'criticar' | 'bañar' | 'pelear' | 'discutir' | 'dialogar' | 'ordenar' | 'hacer' | 'cocinar' | 'beber' | 'jugar' | 'ver' | 'llamar' | 'robar' | 'esconder' | 'comprar' | 'lavar' | 'limpiar' | 'poner' | 'quitar' | 'cambiar' | 'avisar' | 'ganar' | 'perder' | 'esperar' | 'ir' | 'preparar' | 'tirar' | 'salvar' | 'escapar'    
    P -> 'a' | 'de' | 'en' | 'con' | 'por'
    ADV -> 'bien' | 'mal' | 'rápido' | 'lentamente' | 'siempre' | 'nunca'  | 'fuerte' | 'débil'
    PRON -> 'yo' | 'tú' | 'él' | 'ella' | 'nosotros' | 'ellos' | 'ustedes' | 'mío' | 'tuyo' | 'suyo' | 'de ella' | 'de ellos' | 'nuestro' | 'de ustedes'
    TIEM -> 'enero' | 'febrero' | 'marzo' | 'abril' | 'mayo' | 'junio' | 'julio' | 'agosto' | 'septiembre' | 'octubre' | 'noviembre' | 'diciembre' | 'semana' | 'lunes' | 'martes' | 'miercoles' | 'jueves' | 'viernes' | 'sabado' | 'domingo' | 'ayer' | 'hoy' | 'mañana' | 'antier' | 'futuro' | 'pasado' | 'ahorita' | 'ya' | 'acaba de pasar' | 'antiguo' | 'horario' | 'próximo' | 'en la mañana' | 'tarde' | 'noche' | 'nuevo' | 'viejo' | 'tiempo'
"""

grammar = nltk.CFG.fromstring(MY_GRAMMAR)
parser = nltk.ChartParser(grammar)
terminals = set(rule.rhs()[0] for rule in grammar.productions() if len(rule.rhs()) == 1 and isinstance(rule.rhs()[0], str))

def process_sentance(tokens,oracion):
    try:
        trees = list(parser.parse(tokens))
        if not trees:
            print("No se pudo reconocer con las reglas gramática.")
            return oracion
        else: 
            return trees
    except ValueError:
        print("Error: ValueError. Se mandó algo con una palabra no en la gramática")
        return oracion

def modify_sentence(oracion):
    doc = nlp(oracion)
    infinitive = None
    for token in doc:
        if token.pos_ == 'VERB':
            infinitive = token.lemma_
            break
    print("Infinitivo del verbo: ", infinitive)
    if infinitive:
        print("El infinitivo fue encontrado, reemplazaré el infinitivo en la frase original")
        # Reemplazamos el verbo en infinitivo en la oración
        oracion = oracion.replace(token.text, infinitive)
        # Nueva oración a procesar
        print("New oración-> ", oracion)
        tokens = nltk.word_tokenize(oracion.lower(), language='spanish')
        
    else:
        print("El infinitivo no fue encontrado, usaré la frase original")
        tokens = nltk.word_tokenize(oracion.lower(), language='spanish')
    
    possibleResult = process_sentance(tokens,oracion)

    if not isinstance(possibleResult,list):
        return process_sentance(tokens,oracion)
    else:
        trees = possibleResult

    tiempo = None
    lugar = None
    sustantivo = None
    adjetivo = None
    verbo = None

    tree = trees[0]
    new_tokens = []
    for subtree in tree.subtrees():
        print("label actual ->  ", subtree.label())
        if subtree.label() == 'DET':
            continue
        elif subtree.label() == 'TIEM' and subtree.leaves()[0] in ['ayer', 'hoy', 'mañana', 'antier', 'futuro', 'pasado', 'ahorita', 'ya', 'acaba de pasar', 'antiguo', 'horario', 'próximo', 'en la mañana', 'tarde', 'noche', 'nuevo', 'viejo', 'tiempo', 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']:
            print(subtree.leaves()[0])
            tiempo = subtree.leaves()[0]
        elif subtree.label() == 'L':
            print(subtree.leaves()[0])
            lugar = subtree.leaves()[0]
        elif subtree.label() == 'N':
            print(subtree.leaves()[0])
            sustantivo = subtree.leaves()[0]
        elif subtree.label() == 'ADJ':
            print(subtree.leaves()[0])
            adjetivo = subtree.leaves()[0]
        elif subtree.label() == 'V':
            verbo = subtree.leaves()[0]
    # Generar resultado en orden "Tiempo LUGAR SUSTANTIVO VERBO"
    new_tokens.append(tiempo)
    new_tokens.append(lugar)
    new_tokens.append(sustantivo)
    new_tokens.append(adjetivo)
    new_tokens.append(verbo)

    # Eliminar elementos nulos o vacíos de la lista
    new_tokens = list(filter(None, new_tokens))

    return ' '.join(new_tokens)

# función para reproducir un video
def play_video(video_path):
    # crear el objeto media
    media = instance.media_new(video_path)
    # asignar la media al reproductor
    player.set_media(media)
    # reproducir el video
    player.play()

# función para reproducir la lista de videos
def play_video_list(video_list):
    # reproducir cada video de la lista
    for video in video_list:
        media = instance.media_new(video)
        media_list.add_media(media)

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
            tokens = modified_sentence.split()
            video_list = []
            for token in tokens:
                print("./videos/"+ token +".mp4")
                video_list.append("./videos/"+token+".mp4")
            # reproducir la lista de videos
            play_video_list(video_list)
            # iniciar el bucle de eventos de la ventana
            window.mainloop()
        else:
            print("No se pudo modificar la oración.")
    except sr.UnknownValueError:
        print("Google Speech Recognition no pudo entender el audio.")
    except sr.RequestError as e:
        print("No se puede acceder al servicio de reconocimiento de voz de Google Speech Recognition; {0}".format(e))

listen_and_process()