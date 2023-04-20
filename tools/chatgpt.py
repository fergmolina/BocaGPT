import openai
from dotenv import load_dotenv
import os
from datetime import datetime

def get_openai_response(messages_array):
    """Send a request to GPT-3.5 to complete a chat from a previous message
    Args:
        messages_array: Array of messages objects to give context to GPT-3.5.
                        This object has the role and the content (Check OpenAI docs for more info)
    Returns: A string with the content of the GPT-3.5 answer
    """

    # Load the environment variables from .env file
    load_dotenv()

    # Retrieve the OpenAI key and env vars
    api_key = os.getenv('OPENAI_API_KEY')

    openai.api_key = api_key

    response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=messages_array
    )

    return(response['choices'][0]['message']['content'])

def get_message_from_openai(next_match_days = 0, matches = [], players = []):
    """Create message to tweet the inicial squad if it is a matchday. If it is a weekday, create a message to tweet about the training of that day.
        If it is a weekday but the next day the team has a match, create a message with info about the following match.
    Args:
        next_match_days: int. Days until next match
        matches: List of matches objects with the info of all the matches of the team
        players: List of players objects with the available players of the team
    Returns: A string with the content of the GPT-3.5 answer
    """

    load_dotenv()

    team = os.getenv('TEAM_NAME')
    bot_name = os.getenv('BOT_NAME')
    team_colors = os.getenv('TEAM_COLORS')

    bot_definition = 'Sos ' + bot_name + ', un bot que simula ser el director tecnico de ' + team
    today = datetime.today().strftime('%Y-%m-%d')

    if next_match_days > 1:
        spell = """Crea un tweet donde se proporcine informacion detallada sobre el entrenamiento del dia de hoy, explicando algun tipo de ejercicio.
                Agrega algun emoji relacionados con futbol o """ + team_colors +  """. Hoy no es dia de partido ya que es """ + str(today) + """\n""" + str(matches)
    if next_match_days == 1:
        spell = """Crea un tweet dando informacion, como el oponente, el horario y el estadio sobre el proximo partido de """ + team + """ que es mañana ya que hoy es """ + str(today) + """.
                Agrega algun emoji relacionados con futbol o """ + team_colors +  """ UNICAMENTE y ningun otro color. \n""" + str(matches)
    elif next_match_days == 0:
        spell = """Crea un tweet armando el equipo titular usando UNICAMENTE los jugadores listados.
                Aclara tambien el esquema tactico a utilizar.
                Agrega algun emoji relacionados con futbol o """ + team_colors +  """.
                El mensaje debe solo contener los apellidos de los jugadores para respetar el MAXIMO debe de 280 caracteres.
                El listado tambien incluye jugadores del segundo equipo por si tenes que complementar. """ +str(players)

    answer = list()

    answer.append(get_openai_response([
        {'role': 'system', 'content': bot_definition},
        {'role':'user','content':spell}
    ]))

    if next_match_days == 0:
        spell = """Crea un tweet armando el banco de suplentes con 12 apellidos usando UNICAMENTE los jugadores listados abajo.
                    Agrega algun emoji relacionados con futbol o """ + team_colors +  """.
                    El listado tambien incluye jugadores del segundo equipo por si tenes que complementar.
                    El mensaje debe solo contener los 12 apellidos de los jugadores para respetar el MAXIMO debe de 280 caracteres.
                    Tene en cuenta de NO incluir los jugadores que ya agregaste como titulares en el siguiente mensaje: """ + str(answer) + """
                    El listado de jugadores completo es """ + str(players)

        answer.append(get_openai_response([
        {'role': 'system', 'content': bot_definition},
        {'role':'user','content':spell}
    ]))

    return answer

def get_match_press_from_openai(last_match):
    """Create a list of 5 questions and 5 answers using GPT-3.5 simulating a end match press conference
    Args:
        last_match: A match object with information about the last match played by the bot team
    Returns: A list of messages (Strings) for tweeting
    """

    load_dotenv()

    team = os.getenv('TEAM_NAME')
    bot_name = os.getenv('BOT_NAME')
    today = datetime.today().strftime('%Y-%m-%d')
    answer = list()

    bot_definition = 'Sos ' + bot_name + ', un bot que simula ser el director tecnico de ' + team

    for i in range(0,5):
        spell= """Crea un tweet con MAXIMO 280 caracteres donde se lea una pregunta del partido recien terminado.
                    Aclara el periodista que hace la pregunta y el medio.
                    La pregunta debe ser bastante corta y no tener mayor informacion.
                    El mensaje generado debe estar listo para copiar y pegar en Twitter, sin ningun titulo o comentario.
                    La pregunta debe ser corta para que ingrese en un tweet.
                    Tene presene que el dia de hoy es """ + str(today) + """
                    Utiliza la información del resultado para armar preguntas y respuestas: """ + str(last_match)


        messages = [{'role': 'system', 'content': bot_definition},
                    {'role':'user','content':spell}]

        answer.append(get_openai_response(messages))
        messages.append({'role':'assistant','content':answer[i]})

        spell = """Crea un tweet con MAXIMO de 280 caracteres respondiendo la pregunta.
                No agregues ninguna información adiciona. Solamente la respuesta literal.
                Si notas que la pregunta tiene algo de malicia, podes responder ironicamente.
                La respuesta debe ser corta para que ingrese en un tweet.
                El mensaje generado debe estar listo para copiar y pegar en Twitter, sin ningun titulo o comentario.
                Sino solamente responde lo que se te pregunta"""
        messages.append({'role':'user','content':spell})

        answer.append(get_openai_response(messages))

    return answer

def get_press_from_openai(matches):
    """Create a question and a answer using GPT-3.5 simulating weekday press conference
    Args:
        matches: A list of matches objects with information about the matches played and not played yet
    Returns: A list of messages (Strings) for tweeting
    """
    load_dotenv()

    team = os.getenv('TEAM_NAME')
    bot_name = os.getenv('BOT_NAME')
    today = datetime.today().strftime('%Y-%m-%d')
    answer = list()

    bot_definition = 'Sos ' + bot_name + ', un bot que simula ser el director tecnico de ' + team

    spell= """Crea un tweet con MAXIMO 280 caracteres donde se lea una pregunta sobre el proximo partido, el entrenamiento o algo del club.
                Aclara el periodista que hace la pregunta y el medio.
                La pregunta debe ser bastante corta y no tener mayor informacion.
                Si el resultado fue negativo, el periodista podra hacer alguna pregunta con malicina.
                El mensaje generado debe estar listo para copiar y pegar en Twitter, sin ningun titulo o comentario.
                Tene presene que el dia de hoy es """ + str(today) + """
                La pregunta debe ser corta para que ingrese en un tweet.
                Utiliza la información del resultado para armar preguntas y respuestas: """ + str(matches)

    messages = [{'role': 'system', 'content': bot_definition},
                {'role':'user','content':spell}]

    answer.append(get_openai_response(messages))
    messages.append({'role':'assistant','content':answer[0]})

    spell = """Crea un tweet con MAXIMO de 280 caracteres respondiendo la pregunta.
                No agregues ninguna información adiciona. Solamente la respuesta literal.
                Si notas que la pregunta tiene algo de malicia, podes responder ironicamente.
                La respuesta debe ser corta para que ingrese en un tweet.
                El mensaje generado debe estar listo para copiar y pegar en Twitter, sin ningun titulo o comentario.
                Sino solamente responde lo que se te pregunta"""
    messages.append({'role':'user','content':spell})

    answer.append(get_openai_response(messages))

    return answer



