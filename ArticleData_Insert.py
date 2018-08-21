import pymysql
import json

def ArticleDBInsert():

    db = pymysql.connect(host="localhost",user="root",password="Torres@09",db="DWD_Project")
    cur = db.cursor()
    file_list = ["footballdata_Arsenal.json","footballdata_Liverpool.json","footballdata_MUtd.json","footballdata_MCity.json"]
    table_list = ["Articles_Arsenal","Articles_Liverpool","Articles_United","Articles_City"]
    for i in range(0,len(file_list)):
        tf = 0
        count=0
        with open(file_list[i]) as json_data:
            article_dict = json.load(json_data)
        for j in range(0, len(article_dict)):
            try:
                pstring = " ".join(article_dict[j]["PERSON"])
                print(pstring)
                count +=1
                cur.execute("""INSERT INTO {} (`AID`, `Persons`, `Source`, `Validity`) VALUES (%s,%s,%s,%s);""".format(table_list[i]),(str(count),pstring,article_dict[j]["Source"],tf))
                db.commit()
                print("Success")
            except Exception as e:
                print(e)
                continue
    db.close()