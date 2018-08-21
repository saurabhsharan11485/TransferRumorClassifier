import pymysql

def PlayerInsert():

    db = pymysql.connect(host="localhost",user="root",password="Torres@09",db="DWD_Project")
    cur = db.cursor()
    filehandler = open("playerdata.txt", 'r', encoding="utf-8")
    lines = filehandler.readlines()
    count = 0
    for line in lines:
        templist = line.split(" - ")
        count+=1
        if (templist[1].find(",") != -1):
            tempstr = "".join(templist[1])
            plnamelist = tempstr.split(",")
            plnamelist[1] = plnamelist[1].replace(" ", "")
            templist[1] = plnamelist[1] + " " + plnamelist[0]
        try:
            cur.execute("""INSERT INTO Players(ID, Player_Mapping, Player_Name, Club, Club_Changed) VALUES (%s,%s,%s,%s,%s)""",(str(count),templist[0],templist[1], templist[2], templist[3]))
            db.commit()
            print("Success")
        except Exception as e:
            print(e)
    db.close()

