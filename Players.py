import requests
import json
import time

def PlayerExtraction():

    #Hitting Sportradar API Soccer v3 to extract the players and their current clubs out of the top 96 clubs in Europe
    filehandler = open("playerdata.txt", 'a', encoding="utf-8") #Writing the player data along with corresponding club to text file
    conn =requests.get("https://api.sportradar.us/soccer-xt3/eu/en/tournaments/sr:tournament:679/info.json?api_key=4mc9yuuvfty6432x6bk247wz")
    tournament_dict = json.loads(conn.text)
    tournamentblocks = tournament_dict['groups']
    fintext = ""

    time.sleep(2) #Adding delay between first call and the subsequent continuous calls

    for e in tournamentblocks:
        for i in range(0,4):
            #Using team ID from every group to extract the players of the respective club
            conn2 = requests.get("https://api.sportradar.us/soccer-xt3/eu/en/teams/" + e['teams'][i]['id'] + "/profile.json?api_key=4mc9yuuvfty6432x6bk247wz")
            team_dict = json.loads(conn2.text)
            playerblocks = team_dict['players']
            for f in playerblocks:
                transferred = "NO"
                fintext = f['id'] + " - " + f['name'] + " - " + e['teams'][i]['name'] + "\n"
                time.sleep(2)
                conn3 = requests.get("http://api.sportradar.us//soccer-xt3/eu/en/players/" + f['id'] + "/profile.json?api_key=4mc9yuuvfty6432x6bk247wz")
                player_dict = json.loads(conn3.text)
                pblock = player_dict['roles']
                for r in pblock:
                    try:
                        sd = r['start_date'].split("-")
                        if (sd[0] == "2018"):
                            transferred = "YES"
                        else:
                            transferred = "NO"
                    except:
                        break
                    break
                fintext = f['id'] + " - " + f['name'] + " - " + e['teams'][i]['name'] + " - " + transferred + "\n"
                print(fintext)
                filehandler.write(fintext)
                print("Success")
            time.sleep(2)
    filehandler.close()