import nltk
import tkinter as tk
from threading import Thread
import speech_recognition as sr
import spacy
import vlc
import os
# import our library
import torchmetrics

phrases = [
    ["mi mamá visitó el parque", ["pasado parque mamá visitar"]],
    ["el maestro trabaja en la biblioteca", ["biblioteca maestro trabajar"]],
    ["el doctor visitará a la escuela", ["futuro escuela doctor visitar"]],
    ["en diciembre escribí en mi cuaderno", ["pasado diciembre cuaderno yo escribir"]],
    ["en enero visitaré el parque", ["futuro enero parque yo visitar"]],
    ["mi pelo rojo", ["pelo mío rojo"]],
    ["a mí me duele la cabeza", ["yo cabeza doler"]],
    ["mi novia es flaca", ["novia mía flaca"]],
    ["mi abuelo es gordo", ["abuelo mío gordo"]],
    ["a mí me gusta bailar todos los martes", ["todos martes yo bailar gustar"]],
    ["el jueves mi mamá camina en el parque", ["jueves mamá mía parque caminar", "jueves parque mamá mía caminar"]],
    ["mi tío trabaja de psicólogo", ["tío mío psicólogo trabajar"]],
    ["mi hermana cumple años en mayo", ["mayo hermana mía cumpleaños suyo"]],
    ["a mi nieto le gusta dibujar casas", ["nieto mío casa dibujar gustar", "nieto mío gustar casa dibujar"]],
    ["tengo cita médica el 20 de febrero", ["20 de febrero yo cita médica tener", "20 de febrero yo cita médica ir"]],
    ["a mí me gusta leer libros viejos", ["libros viejos yo gustar leer", "libros viejos yo leer gustar"]],
    ["mi papá y mi mamá se separaron ayer", ["ayer papá mío mamá mía separar"]],
    ["yo juego en la escuela con una bonita pelota", ["escuela yo pelota bonita jugar", "escuela pelota bonita yo jugar"]],
    ["la estufa está adentro de la casa", ["casa estufa adentro", "casa ahí estufa adentro"]],
    ["yo entré al cine temprano", ["cine temprano yo entrar", "temprano cine yo entrar", "cine yo entrar temprano", "cine yo entrar temprano entrar"]],
    ["yo compré en la tienda comida", ["pasado tienda comida yo comprar"]],
    ["yo compro en la tienda comida", ["tienda comida yo comprar"]],
    ["mi perro es pequeño", ["perro mío pequeño"]],
    ["el carro de mi papá es grande", ["papá mío carro suyo grande"]],
    ["todos los domingos voy a misa con mi abuela", ["todos domingos misa abuela mía yo ir"]],
    ["antier entraron a robar a mi casa", ["antier casa mía entrar robar"]],
    ["mi hermano estudia para abogado", ["hermano mío abogado él estudiar"]],
    ["el mesero me trajo de comer", ["mesero él comida traer yo", "mesero él comida traer yo comer (direccionales)"]],
    ["a mí me gusta nadar en la alberca", ["alberca yo nadar gustar"]],
    ["a mi prima le gusta pasear en la laguna", ["laguna prima mía pasear gustar", "laguna prima mía gustar pasear"]],
    ["mi abuelo es arquitecto", ["abuelo mío arquitecto"]],
    ["mis amigos y yo fuimos a comer el miércoles en el restaurante", ["pasado miércoles restaurante amigos míos yo comer ir", "pasado miércoles restaurante amigos míos yo ir comer"]],
    ["yo trabajo 40 horas a la semana", ["semana 40 horas yo trabajar"]],
    ["el doctor me revisa el corazón y los pulmones", ["corazón pulmón mío doctor revisar"]],
    ["el doctor me revisó el corazón y los pulmones", ["pasado corazón pulmón mío doctor revisar"]],
    ["el carro verde",["carro verde"]],
    ["mi casa azul",["casa mía azul"]],
    ["ellos comieron ayer",["ayer ellos comer"]],
    ["yo mañana juego",["mañana yo jugar"]],
    ["yo cociné ayer",["ayer yo cocinar"]],
    ["me gusta dibujar",["yo dibujar gustar", "yo gustar dibujar", "dibujar yo gustar"]],
    ["él juega carreras",["él carreras jugar"]],
    ["ella bebe agua",["ella agua beber"]],
    ["ustedes hacen apuestas",["ustedes apuestas hacer"]],
    ["prende la estufa", ["tú estufa prender"]],
    ["guarda los juegues",["tú juguetes guardar"]],
    ["corten las naranjas",["ustedes naranjas cortar"]],
    ["ella escribe mucho",["ella escribe mucho"]],
    ["me gusta comer",["yo comer gustar", "yo gustar comer"]],
    ["él maneja mucho",["él maneja mucho","él mucho manejar"]],
    ["yo rompo nueces",["yo nueces romper"]],
    ["yo como arroz",["arror yo comer", "yo arroz comer"]],
    ["tú juegas mucho",["tú jugar mucho"]],
    ["ellos beben tequila",["ellos tequila beber", "tequila ellos beber"]],
    ["ustedes platican poco",["ustedes platicar poco"]],
    ["mi amigo y yo",["amigo mío y yo"]],
    ["el carro es feo",["carro feo"]],
    ["voy a misa siempre",["siempre yo misa ir"]],
    ["yo juego fútbol mucho",["yo futbol jugar mucho"]],
    ["yo abro la puerta",["yo puerta abrir"]],
    ["ella come pan dulce",["pan dulce ella comer", "ella pan dulce comer"]],
    ["Juan baila muy bien",["Juan bailar muy bien"]],
    ["me duele el brazo",["yo brazo doler"]],
    ["María come galletas siempre",["siempre María galletas comer"]],
    ["el perro vino ayer",["ayer perro venir"]],
    ["Lupita corta los árboles",["Lupita árboles cortar"]],
    ["los niños van riendo",["niños reír van"]],
    ["José compra los frijoles",["José frijoles comprar"]],
    ["Toño compra los pantalones",["Toño pantalones comprar"]],
    ["Luis pinta la casa",["Luis casa pintar", "casa Luis pintar"]],
    ["yo prendo la computadora",["yo computadora prender"]],
    ["a mí me vacunaron ayer",["ayer yo vacunar"]],
    ["Juan bota la pelota siempre",["siempre Juan pelotar botar"]],
    ["yo me puse los zapatos",["yo zapatos poner"]],
    ["Jesús fue al cine ayer",["ayer Jesus cine ir"]],
    ["Carmen donó su sangre antier",["antier Carmen sangre suya donar"]],
    ["María irá mañana al hospital",["mañana María hospital ir"]],
    ["yo hago tortillas los Martes",["amigo"]],
    ["yo reviso a mi hija",["yo hija mía revisar"]],
    #Frases de 6 palabras
    ["le hice biberón a mi hija",["hija mía yo biberón hacer"]],
    ["Sofía se baña todos los días",["todos los días Sofía bañar"]],
    ["Jorge come chicharrón todos los Viernes",["todos los Viernes Jorge chicharrón comer"]],
    ["yo trabajo de soldador y construcción",["yo soldador construcción trabajar"]],
    ["Luis compra por internet los carros",["Luis internet carros comprar"]],
    ["mi hija hace berrinche al comer",["hija mía comer berrinche hacer"]],
    ["Juan siempre trabaja en la escuela",["siempre Juan escuela trabajar"]],
    ["yo arreglo las bicicletas de todos",["yo bicicletas de todos arreglar", "yo bicicletas suyas arreglar"]],
    ["mi hija a caminar muy pronto",["hija mía caminar pronto aprender"]],
    ["Tony va al campamento con amigos",["Tony amigos campamente ir"]],
    ["Juan mecánico arregla los carros rojos",["Juan mecánico carros rojos arreglar"]],
    ["en diciempre regalo chocolates y juguetes",["diciembre yo juguetes chocolates regalar", "diciembre yo chocolates juguetes regalar"]],
    #frases de 7 palabras
    ["en febrero siempre regalo flores y chocolates",[""]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    #Frases de 8 palabras
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    #frases de 9 palabras
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    #frases de 12 palbras
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]],
    ["",["amigo"]]
]



# Convertir la lista a un diccionario en minúsculas
phrases_dict = {phrase[0]: phrase[1] for phrase in phrases}

frase = "a mi me gusta nadar en la alberca"
resultado = phrases_dict.get(frase)
print(resultado)

nlp = spacy.load("es_core_news_sm")

# Crear ventana principal
window = tk.Tk()
window.title("Reconocimiento de voz")
window.geometry("400x200")

nltk.download('punkt')
from nltk.tree import Tree

MY_GRAMMAR = """
    S -> VP | VP NP | NP VP | NP V | NP ADJ
    NP -> N ADJ | DET N | ADJ NP | N | PRON | NP PP | L | DET L | P | P NP | P TIEM 
    VP -> V NP | V NP PP | VP NP ADJ | ADJ VP | V ADV | VP TIEM | V TIEM 
    PP -> P NP 
    ADJ -> "cero" | "uno" | "dos" | "tres" | "cuatro" | "cinco" | "seis" | "siete" | "ocho" | "nueve" | "diez" | "once" | "doce" | "trece" | "catorce" | "quince" | "dieciséis" | "diecisiete" | "dieciocho" | "diecinueve" | "veinte" | "treinta" | "cuarenta" | "cincuenta" | "sesenta" | "setenta" | "ochenta" | "noventa" | "cien" | "doscientos" | "trescientos" | "cuatrocientos" | "quinientos" | "seiscientos" | "setecientos" | "ochocientos" | "novecientos" | "mil" | "diez mil" | "cien mil" | "un millón" | 'chaparro' | 'gordo' | 'flaco' | 'guapo' | 'feo' | 'rubio' | 'moreno' | 'pelirrojo' | 'pecoso' | 'grande' | 'pequeño' | 'alto' | 'bajo' | 'sobre'| 'abajo' | 'adentro' | 'afuera' | 'enfrente' | 'atrás' | 'esférico' | 'plano' |'suave' | 'fino' | 'áspero' | 'azul' | 'amarillo' | 'café' | 'gris' | 'negro' | 'naranja' | 'rojo' | 'morado' | 'verde' | 'rosa' | 'oscuro' | 'claro'
    DET -> 'el' | 'la' | 'los' | 'las' | 'su' | 'mi'
    N -> 'mes' | 'pelo' | 'ojos' | 'nariz' | 'boca' | 'oreja' | 'frente' | 'cabeza' | 'ceja' | 'hombro' | 'brazo' | 'dedos' | 'manos' | 'pecho' | 'abdomen' | 'pies' | 'cerebro' | 'lengua' | 'corazon' | 'pulmones' | 'higado' | 'riñones' | 'intestino' | 'apendice' | 'vagina' | 'ovarios' | 'pene' | 'testiculos' | 'barba' | 'bigote' | "maestro" | "mesero" | "arquitecto" | "doctor" | "ingeniero" | "abogado" | "psicologo" | "empresario" | "policia" | "soldador" | "enfermero" | "carpintero" | "carro" | "pelota" | "telefono" | "dinero" | "ropa" | "juguete" | "plato" | "estufa" | "bicicleta" | "jabon" | "sacapuntas" | "llave" | "espejo" | "computadora" | "papel" | "zapato" | "mesa" | "silla" | "sombrero" | "tenis" | "puerta" | "calceta" | "cuaderno" | "lápiz" | "toalla" | "vaso" | "pluma" |  'hombre' | 'mujer' | 'sobrino' | 'suegro' | 'compadre' | 'ahijado' | 'amante' | 'abuelo' | 'hijo' | 'primo' | 'nuera' | 'comadre' | 'novio' | 'soltero' | 'papá' | 'nieto' | 'hermano' | 'yerno' | 'padrino' | 'padrastro' | 'casado' | 'mamá' | 'tio' | 'cuñado' | 'madrina' | 'madrastra' | 'esposo' | 'viudo'
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

# Función para identificar las categorías gramaticales de las palabras
def categorize_words(sentence):
    doc = nlp(sentence)
    categories = {
        "tiempo": [],
        "lugar": [],
        "sustantivo": [],
        "adjetivo": [],
        "verbo": [],
        "posesivo": []
    }

    for token in doc:
        if token.pos_ == "NOUN":
            if token.dep_ == "poss":
                categories["posesivo"].append(token.text)
            else:
                categories["sustantivo"].append(token.text)
        elif token.pos_ == "ADJ":
            categories["adjetivo"].append(token.text)
        elif token.pos_ == "VERB":
            categories["verbo"].append(token.text)
        elif token.pos_ == "ADV" and "temp" in token.tag_:
            categories["tiempo"].append(token.text)
        elif token.pos_ == "ADV" and "loc" in token.tag_:
            categories["lugar"].append(token.text)

    return categories

# Función para formar una nueva oración en base a las categorías
def form_new_sentence(categories):
    tiempo = " ".join(categories["tiempo"])
    lugar = " ".join(categories["lugar"])
    sustantivos = " ".join(categories["sustantivo"])
    posesivos = " ".join(categories["posesivo"])
    adjetivos = " ".join(categories["adjetivo"])
    verbos = " ".join(categories["verbo"])

    new_sentence = f"{tiempo} {lugar} {sustantivos} {posesivos} {adjetivos} {verbos}"
    return new_sentence


def process_sentance(tokens,oracion):
    try:
        trees = list(parser.parse(tokens))
        if not trees:
            print("No se pudo reconocer con las reglas gramática.")
            return oracion , 1
        else: 
            return trees
    except ValueError:
        print("Error: ValueError. Se mandó algo con una palabra no en la gramática")
        return oracion, 1

def modify_sentence(oracion):
    doc = nlp(oracion)
    infinitive = None
    tiempo_verbo = None
    for token in doc:
        if token.pos_ == 'VERB':
            print(token.morph.get('Tense'))
            if token.morph.get('Tense') == ['Past']:
                tiempo_verbo = 'past'
            elif token.morph.get('Tense') == ['Fut']:
                tiempo_verbo = 'future'
            else:
                tiempo_verbo = None
            infinitive = token.lemma_
            break
    
    print("Infinitivo del verbo: ", infinitive)
    print("Tiempo orignal del verbo: ", tiempo_verbo)
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

    tiempoPrefijo = None
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
    
    print("Tiempo verbo: ", tiempo_verbo)
    if tiempo_verbo == 'past':
        tiempoPrefijo = 'pasado'
    elif tiempo_verbo == 'future':
        tiempoPrefijo = 'futuro'
    print("Tiempo verbo: ", tiempo)
    # Generar resultado en orden "TIEMPO LUGAR SUSTANTIVO ADJ VERBO"
    new_tokens.append(tiempoPrefijo)
    new_tokens.append(tiempo)
    new_tokens.append(lugar)
    new_tokens.append(sustantivo)
    new_tokens.append(adjetivo)
    new_tokens.append(verbo)

    # Eliminar elementos nulos o vacíos de la lista
    new_tokens = list(filter(None, new_tokens))

    return ' '.join(new_tokens), 0

# función para reproducir un video
def play_video(video_path, player, instance):
    # crear el objeto media
    media = instance.media_new(video_path)
    # asignar la media al reproductor
    player.set_media(media)
    # reproducir el video
    player.play()

# función para reproducir la lista de videos
def play_video_list(video_list,player,intance):
    status_label.config(text="Reproduciendo...")
    window.geometry("720x480")
    # reproducir cada video de la lista
    for video in video_list:
        # reproducir el video actual
        play_video(video, player,intance)
        # esperar a que termine el video
        while player.get_state() != vlc.State.Ended:
            continue
    player.stop()
    player.release()
    window.geometry("400x200")


def listen_and_process():
    # inicializar el reproductor de VLC
    instance = vlc.Instance(['--rate=1.2',"--playlist-enqueue","--fullscreen","--video-on-top","--video-x=1","--video-y=1","--no-video-deco"])
    player = instance.media_player_new()
    media_list = vlc.MediaList()
    # player.toggle_fullscreen()
    player.video_set_scale(0.5)
    # Obtener el identificador de la ventana del reproductor
    player.set_hwnd(frame.winfo_id())
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Diga algo:")
        audio = r.listen(source)
    try:
        print("Google Speech Recognition cree que has dicho: " + r.recognize_google(audio, language='es-ES'))
        frase = r.recognize_google(audio, language='es-ES')
        modified_sentence, wasAcceptedByGrammar = modify_sentence(r.recognize_google(audio, language='es-ES'))
        video_list = []
        # tokens = modified_sentence.split()
        if wasAcceptedByGrammar==0:
            tokens = modified_sentence.split()
            print("La oración fue aceptada por la gramática : \"", modified_sentence + "\"")
            for token in tokens:
                print("./videos/"+ token +".mp4")
                video_list.append("./videos/"+token+".mp4")
            if(phrases_dict.get(frase)):
                preds = modified_sentence
                target = [phrases_dict.get(frase)]
                ter = torchmetrics.TranslationEditRate()
                print("TER CALCULADO", ter(preds, target))
            # reproducir la lista de videos
            play_video_list(video_list,player,instance)

        else:
            print("No fue aceptada por la gramática, intentando deletrear y/o señas PALABRAS: "+ modified_sentence)
            
            categories = categorize_words(modified_sentence.lower())
            new_sentence = form_new_sentence(categories)
            print("NUEVA ORACIÓN ->" +new_sentence)
            if new_sentence:
                tokens = new_sentence.split()
            else:
                tokens = modified_sentence.split()
            for word in tokens:
                if os.path.exists("./videos/"+word.lower()+".mp4"):
                    print("La palabra existe en los videos, reproduciendo el video de dicha palabra: "+word)
                    video_list.append("./videos/"+word.lower()+".mp4")
                else:
                    print("La palabra no existe en los videos, deletreando..." + word)
                    for char in word:
                        print("./abc/"+ char.lower() +".mp4")
                        video_list.append("./abc/"+char.lower()+".mp4")
            if(phrases_dict.get(frase)):
                #Calcular el Translation Edit Rate 
                preds = new_sentence
                target = [phrases_dict.get(frase)]
                ter = torchmetrics.TranslationEditRate()
                print("TER CALCULADO", ter(preds, target))

            #reproducir la lista de videos
            play_video_list(video_list,player,instance)
            
    except sr.UnknownValueError:
        print("Google Speech Recognition no pudo entender el audio.")
    except sr.RequestError as e:
        print("No se puede acceder al servicio de reconocimiento de voz de Google Speech Recognition; {0}".format(e))

    status_label.config(text="")

# Función para manejar el evento de clic en el botón de micrófono
def handle_microphone_button():
    status_label.config(text="Escuchando...")
    Thread(target=listen_and_process).start()
    

# Crear una etiqueta para mostrar el estado
status_label = tk.Label(window, text="", font=("Arial", 16))
status_label.pack(pady=20)

# Crear un botón con el logo de un micrófono
microphone_button = tk.Button(window, text="🎤", font=("Arial", 20), command=handle_microphone_button)
microphone_button.pack(pady=20)

# Crear un contenedor dentro de la ventana principal
frame = tk.Frame(window)
frame.pack(fill=tk.BOTH, expand=True)
# Establecer una altura específica para el contenedor
frame_height = 500
frame.configure(height=frame_height)

# Iniciar el bucle principal de la ventana
window.mainloop()
