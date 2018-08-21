import pymysql

def compare():

    db = pymysql.connect(host="localhost",user="root",password="Torres@09",db="DWD_Project")
    cur = db.cursor()
    table_list = ["Articles_Arsenal","Articles_Liverpool","Articles_United","Articles_City"]
    tablevsclub_dict = {
        "Articles_Arsenal" : "Arsenal",
        "Articles_Liverpool" : "Liverpool",
        "Articles_United" : "Manchester United",
        "Articles_City" : "Manchester City"
    }
    total_clubs = []
    cur.execute("""SELECT DISTINCT Club FROM Players""")
    tempclubs = list(cur.fetchall())
    for clubcounter in range(0,len(tempclubs)):
        total_clubs.append(tempclubs[clubcounter][0])
    for i in table_list:
        cur.execute("""SELECT MAX(AID) FROM {}""".format(i))
        temp1 = list(cur.fetchone())
        num_articles = temp1[0]
        print(num_articles)
        while(num_articles > 0):
            try:
                cur.execute("""SELECT Persons, Source, Validity FROM {} WHERE AID = {}""".format(i,num_articles))
                temp2 = list(cur.fetchone())
                player_name = temp2[0]
                name_list = player_name.split()
                print(name_list)
                if(temp2[2] == 1):
                    print("SKIPPED")
                    num_articles -= 1
                    continue
                try:
                    for n in name_list:
                        temp_match = []
                        cur.execute("""SELECT Player_Mapping, Club, Club_Changed FROM Players WHERE Player_Name LIKE '%{}%' """.format(n))
                        matched_list = list(cur.fetchall())
                        match_length = len(matched_list)
                        for ml in range(0,match_length):
                            temp_match.append((matched_list[ml][2]).replace("\n",""))
                        print(temp_match)
                        if("YES" in temp_match) or ("YES\r" in temp_match):
                            finvalidvalue = 1
                            try:
                                cur.execute("""UPDATE {} SET Validity = %s WHERE Persons LIKE %s """.format(i),(finvalidvalue,player_name))
                                db.commit()
                                print("Success")
                                break
                            except Exception as e:
                                db.rollback()
                                print(e)
                except:
                    num_articles -= 1
                    continue
                num_articles -= 1
            except Exception as e:
                print(e)
                num_articles -= 1
                continue
    db.close()