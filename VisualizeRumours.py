from bokeh.plotting import figure,show, save
from bokeh.io import output_file
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6
import pymysql


def Visualize():

    db = pymysql.connect(host="localhost",user="root",password="Torres@09",db="DWD_Project")
    cur = db.cursor()
    cur2 = db.cursor()
    cur3 = db.cursor()
    table_list = ["Articles_Arsenal","Articles_Liverpool","Articles_United","Articles_City"]
    player_name = {"Sanchez" : [] ,"Giroud" : [] ,"Mkhitaryan" : [] , "Aubameyang": [] }
    number_articles_club = []
    club_names = []

    for tname in table_list:
        cur.execute("""SELECT Source, COUNT(Source), sum(Validity) FROM {} GROUP BY Source ORDER BY COUNT(Source) DESC LIMIT 0,6""".format(tname))
        cur2.execute("""SELECT COUNT(*) FROM {} """.format(tname))

        resultlist = list(cur.fetchall())
        resultlist1 = list(cur2.fetchall())
        source_list = []
        valid_articles = []
        number_articles_club.append(resultlist1)
        print(resultlist)
        for sourcecounter in range(0,len(resultlist)):
            source_list.append(resultlist[sourcecounter][0])
            valid_articles.append(resultlist[sourcecounter][2])

        for player in player_name.keys() :
            cur3.execute("""SELECT COUNT(*) FROM {} WHERE Persons LIKE "%{}%" """.format(tname, player))
            resultlist2 = list(cur3.fetchall())
            player_name[player].append(resultlist2[0][0])


        name = tname.split("_")[1]
        output_file(tname + ".html")
        club_names.append(name)

        articlesource = ColumnDataSource(data=dict(newssource=source_list,validart=valid_articles,color=Spectral6))
        rumourhitplot = figure(title="Rumour Validator " + "- " + tname, x_range=source_list, x_axis_label="Sources", y_axis_label="Valid Rumour Articles")
        rumourhitplot.vbar(x="newssource",top="validart",width=0.2, color="color", source=articlesource)

        save(rumourhitplot)

    for player in player_name.keys():
        player_name[player] = sum(player_name[player])

    pname = list(player_name.keys())
    num_articles = list(player_name.values())
    print(player_name)

    total_articles = figure(title="Article per club " , x_range=club_names, x_axis_label="Clubs", y_axis_label="Number of Distinct Articles")
    total_articles.vbar(x=club_names,top=number_articles_club,width=0.6, color=Spectral6)

    player_articles = figure(title="Popular Players " , x_range=pname, x_axis_label="Clubs", y_axis_label="Number of Distinct Articles")
    player_articles.vbar(x=pname,top=num_articles,width=0.6, color=Spectral6)

    output_file("Articles_Frequency_Clubs.html")
    output_file("Player_Frequency.html")
    save(total_articles)
    save(player_articles)
    db.close()
