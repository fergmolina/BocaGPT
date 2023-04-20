from tools.scrapping import get_players_full_roster, get_matches, get_last_match
from tools.utils import next_match_days, get_execution
from tools.chatgpt import get_message_from_openai, get_match_press_from_openai, get_press_from_openai
from tools.tweet import tweet, check_messages
from time import sleep
from dotenv import load_dotenv
import os


def main(event, context):
    """Main function of the bot
    Args:
        event: Not used. Just added because of Google Cloud (you can remove this one)
        context: Not used. Just added because of Google Cloud (you can remove this one)
    Returns:
        An array of the tweets created by the bot and a 200 if OK
        If it fails, it will return 400 and the exception
    """
    try:
        matches = get_matches()
        days_for_next_match = next_match_days(matches)
        execution = get_execution()

        if execution == 1: # Execution of 10 am
            if days_for_next_match == 0: # If next match is today, check the available players
                players = get_players_full_roster()
            else:
                players = []

            wrong_messages = True
            while wrong_messages:
                tweets_msg = get_message_from_openai(days_for_next_match, matches, players)
                wrong_messages = check_messages(tweets_msg)


        elif execution == 2 and days_for_next_match > 0:
                wrong_messages = True
                while wrong_messages:
                    tweets_msg = get_press_from_openai(matches)
                    wrong_messages = check_messages(tweets_msg)
        elif execution == 3 and days_for_next_match == 0:
            match = get_last_match()

            load_dotenv()
            bot_name = os.getenv("BOT_NAME")

            tweet('Comienza la conferencia de prensa del manager @'+str(bot_name)+' luego del partido #'+str(bot_name))
            sleep(2)
            wrong_messages = True
            while wrong_messages:
                tweets_msg = get_match_press_from_openai(match)
                wrong_messages = check_messages(tweets_msg)


        tweet_id = 0

        for tweet_msg in tweets_msg:
            sleep(2) # To avoid any twitter API issues posting tweets too quickly
            if tweet_id == 0:
                tweet_id = tweet(tweet_msg)
            else:
                _ = tweet(tweet_msg,tweet_id)
                tweet_id = 0


        return (tweets_msg, 200)

    except Exception as e:
        return ("error - " + str(e), 400)


if __name__ == "__main__":
    main('','')