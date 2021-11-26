
from SnappaLeaderboard import SnappaLeaderboard
from SnappaLeaderboardTextGenerator import generate_leaderboard_string, generate_score_log_string
from Databases.GoogleSheetsDatabase import GoogleSheetsDatabase
from Databases.DictionaryDatabase import DictionaryDatabase
from tabulate import tabulate
from elosports.elo import Elo

INITIAL_ELO = 1500
INITIAL_ELO_Ws_Ls = [1500,0,0]


def addPlayerTest1(db):
    """Add a player and verify that the leaderboard was updated

    Returns
    -------
    Boolean
        True if behaves correctly, False otherwise

    """
    print("Testing add player...")
    leaderboard = SnappaLeaderboard(db)
    name = "Garrett"
    name2 = "Andrei"
    data1 = [["Garrett", INITIAL_ELO, 0,0]]
    data2 = [["Garrett", INITIAL_ELO, 0,0], ["Andrei", INITIAL_ELO, 0, 0]]
    n = 2
    response = leaderboard.add_player(name, *INITIAL_ELO_Ws_Ls)
    if response != "Player Garrett successfully added to the database!":
        return False

    lb = leaderboard.get_leaderboard(n)

    #TEST1

    if lb != generate_leaderboard_string(data1, n):
        return False

    leaderboard.add_player(name2, *INITIAL_ELO_Ws_Ls )
    lb2 = leaderboard.get_leaderboard(n)
    if lb2 != generate_leaderboard_string(data2, n):
        return False

    leaderboard.add_player("Noah", *INITIAL_ELO_Ws_Ls)
    leaderboard.add_player("Sebastian", *INITIAL_ELO_Ws_Ls)

    return True



def logScoreTest1(db):
    """Add two scores and verify that the leaderboard was properly updated

    Returns
    -------
    Boolean
        True if behaves correctly, False otherwise

    """
    print("Testing Log Score...")
    names1 = ["Garrett", "Andrei", "Noah", "Sebastian"]
    names2 = ["Garrett", "Sebastian", "Andrei", "Noah"]
    leaderboard = SnappaLeaderboard(db, k = 10)
    leaderboard.set_k(40) #k to 100 - will fail if changed

    response = leaderboard.log_score(*names1, 7, 5)
    data = [
        ["Andrei", 1, 1520, 20],
        ["Garrett", 2, 1520, 20],
        ["Noah", 3, 1480, -20],
        ["Sebastian", 4, 1480, -20]
    ]
    print(response)
    expected = tabulate(data, headers = ["Name", "New Rank", "New ELO", "ELO Change"])
    if response!= expected:
        return False


    data2 = [
        ["Andrei", 1, 1537, 17],
        ["Garrett", 2, 1537, 17],
        ["Noah", 3, 1463, -17],
        ["Sebastian", 4, 1463, -17]
    ]
    response = leaderboard.log_score(*names1, 7, 5)
    print(response)
    expected = tabulate(data2, headers = ["Name", "New Rank", "New ELO", "ELO Change"])
    if response!= expected:
        return False


    data3 = [
        ["Garrett", 1, 1557, 20],
        ["Andrei", 2, 1517, -20],
        ["Sebastian", 3, 1483, 20],
        ["Noah", 4, 1443, -20]
    ]
    response = leaderboard.log_score(*names2, 7, 5)
    print(response)
    expected = tabulate(data3, headers = ["Name", "New Rank", "New ELO", "ELO Change"])
    if response!= expected:
        return False

    return True


def getPlayerHistoryTest1(db):
    """Adds players, log some games then verifies a correct player
    history

    Returns
    -------
    Boolean
        True if behaves correctly, False otherwise


    """
    print("Testing Player History...")
    slb = SnappaLeaderboard(db)
    print(slb.generate_message())
    return True

if __name__ == '__main__':

    ### GOOGLE SHEETS TEST ####
    # db = GoogleSheetsDatabase(test = True)

    ### NAIVE DATABASE TEST ###
    db = DictionaryDatabase()

    print("\n")
    print("Testing Snappa Leaderboard...\n")
    for name, test in [
            ["Add Player Test 1", addPlayerTest1],
            ["Log Score Test 1", logScoreTest1],
            ["Get Player History Test 1", getPlayerHistoryTest1]]:
        if test(db):
            print(str(name) + " passed!")
        else:
            print(str(name) + " failed!")
