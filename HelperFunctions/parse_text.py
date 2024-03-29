
from HelperFunctions.execute_action import HELP_MESSAGE

"""
PARSE STRUCTURE

add player
@SnappaBot /add @<name> | @SnappaBot /add @me

log score
@SnappaBot /score @<name> @<name> @<name> @<name>, <score_1> <score_2> |
@SnappaBot /score @me @<name> @<name> @<name>, <score_1> <score_2>

get leaderboard
@SnappBot /lb

get player data
@SnappaBot /stats @<name> | @SnappaBot /stats @me

load members
@SnappaBot /loadMembers

get help
@SnappaBot /help

message
@SnappaBot *

error
malformed

none
not mentioning snappabot

"""

BOT_NAME = "SnappaBot"

def parse_text(text : str,
        n : int,
        initial_elo : int,
        initial_wins : int,
        initial_losses : int,
        sender : str
    ):
    """Parses a new message in the groupme

    Parameters
    ----------
    text : str
        Incoming message text
    n : int
        Number of leaderboard entries to return
    initial_elo : int
        initial elo for a player
    initial_wins : int
        initial wins for a player
    initial_losses : int
        initial losses for a player
    sender : str
        person who sent the message

    Returns
    -------
    tuple
        (action, list(string))

        tuple containing a string saying the action in the first index
        and list of parameters in the second index
    """
    bot_handle = "@" + BOT_NAME
    try:
        if len(text) >= len(bot_handle) and text[:len(bot_handle)] == bot_handle:
            #addressing snappa bot
            remaining = text[len(bot_handle):]
            if "/help" in remaining:
                return "get help", []

            elif "/add" in remaining:
                name = remaining[5:].strip(" @")
                if name == "me":
                    return "add player", [sender, initial_elo, initial_wins, initial_losses]
                return "add player", [name.strip(), initial_elo, initial_wins, initial_losses]
            elif "/lb" in remaining:
                return "get leaderboard", [n]
            elif "/score" in remaining:
                data = remaining[7:].strip().split(",")
                names = [name.strip() for name in data[0].strip("@").split("@")]
                score = [int(x) for x in data[1].strip().split("-")]
                if names[0] == "me":
                    names[0] = sender
                return "log score", names + score

            elif "/loadMembers" in remaining:
                return "load members", []

            elif "/stats" in remaining:
                name = remaining[7:].strip(" @")
                if name == "me":
                    return "get player data", [sender]
                return "get player data", [name]
            elif sender != BOT_NAME:
                return "get message", []
            else:
                return "none", []
    except:
        return "error", []
    if bot_handle in text and sender != BOT_NAME:
        return "get message", []
    return "none", []

if __name__ == '__main__':
    for message in [
        "@SnappaBot /help asduvbayi"
        "@SnappaBot /add @Garrett Gordon",
        "@SnappaBot /score @Garrett Gordon @Andrei @Sebastian @Noah, 7-3",
        "@SnappaBot /lb",
        "@SnappaBot /stats @Garrett Gordon",
        "@SnappaBot I love you"
    ]:
        print("\n" + "---"*10)
        print("Parsing:", message)
        action, parameters = parse_text(message, 10, 1500, 0 , 0, "Garrett Gordon")

        print(action)
        print(parameters)
