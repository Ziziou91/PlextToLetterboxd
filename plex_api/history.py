"""Plex api watch history functionality."""
import sys
import xml.etree.ElementTree as ET
from utils.ui import get_user_selection, draw_table, draw_movie_table
from .client import get_plex_response
from .user import get_users

def get_watch_history(ipaddress: str, token: str, accountID: str, librarySectionID: str) -> str:
    """Return list of media watched by a given user in a library.
    
    Args:
        token: The Plex authentication token
        accountID: The account ID to get history for
        librarySectionID: The library section ID to get history from
        
    Returns:
        Response object containing watch history data
    """
    url = f"http://{ipaddress}:32400/status/sessions/history/all?accountId={accountID}&librarySectionID={librarySectionID}&X-Plex-Token="
    history_response = get_plex_response(url, token)

    return history_response

def print_watch_history(ipaddress: str, token: str, librarySectionID: str) -> None: 
    user_str = get_user_selection()

    if user_str == "mine":
        watch_history_response = get_watch_history(ipaddress, token, 1, librarySectionID)
        root = ET.fromstring(watch_history_response.content)
        
        movies = []

        for child in root:
            movie_data = child.attrib
            movies.append({
                "title": movie_data.get("title"),
                "empty" : "",
                "viewedAt": movie_data.get("viewedAt")
            })

        draw_movie_table(movies)

    elif user_str == "other":
        users = get_users(token)
        draw_table(users)

    elif user_str == "cancel":
        print("Exiting program.")
        sys.exit(0)
