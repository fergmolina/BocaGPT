from datetime import datetime  
import pytz

def next_match_days(matches_list):
    """Function that calculates the days to the next match. Can go from 0-inf
    Args:
        matches_list: List of matches objects
    Returns:
        int. Difference of days between the next match and today. Range between 0-inf
    """
    today = datetime.now().date()

    for match in matches_list:
        if match['result'] == '':
            return (datetime.strptime(match['date'], '%Y-%m-%d').date()-today).days
        
def is_evening():
    """Check if is already the evening or not. It is needed because we will have two executions every day
    Args: -
        matches_list: List of matches objects
    Returns: Boolean. True if is evening (past 12 pm) or False if not (less than 12 pm)
    """
    today_hour = datetime.now().time().hour
    return(today_hour>12)

def get_execution():
    """Check what nro of execution is the current. There are 3 executions at the moment (10 am, 19 and 23 GMT-3)
    Args: -
    Returns: int. 1 if it's the execution of 10 am, 2 if 19 and 3 if 23.
    """
    today_hour = datetime.now(pytz.timezone('America/Argentina/Buenos_Aires')).time().hour
    if today_hour == 10:
        return 1
    elif today_hour == 19:
        return 2
    elif today_hour == 23:
        return 3