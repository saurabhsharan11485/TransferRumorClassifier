import time
import requests
import json
from nltk.tag.stanford import StanfordNERTagger

def ArticleExtraction():
    st = StanfordNERTagger(r"C:\Users\saura\Desktop\stanford-ner-2018-02-27\classifiers\english.all.3class.distsim.crf.ser.gz",
                           r"C:\Users\saura\Desktop\stanford-ner-2018-02-27\stanford-ner.jar")
    club_list = ["Arsenal", "Liverpool", "Manchester United", "Manchester City"]
    club_dict = {"Arsenal" : "footballdata_Arsenal.json",
                 "Liverpool" : "footballdata_Liverpool.json",
                 "Manchester United" : "footballdata_MUtd.json",
                 "Manchester City" : "footballdata_MCity.json"}
    for cname in club_list:
        print("NEW CLUB")
        data_list = []
        try:
            for i in range(1, 40):
                url= "https://newsapi.org/v2/everything?"
                parameters = dict(q='transfer AND football AND ' + cname, from_parameter="2017-12-01", to="2018-01-31",
                                  language='en', pageSize=10, page=i,
                                  apiKey="d3e56214150b4ef6821131c9ef777faa")
                r = requests.get(url, params=parameters)
                footballdata_dict = json.loads(r.text)
                with open(club_dict[cname]) as f:
                    data: object = json.load(f)
                try:
                    newsblocks = footballdata_dict['articles']
                except:
                    continue
                finaltext = ""
                for e in newsblocks:
                    if(e['description'] == ""):
                        continue
                    webaddr = str(e['url'])
                    webtext = str(e['description'])
                    print(webtext)
                    ner_list = (st.tag(webtext.split()))
                    fintuple_dict = {}
                    fintuple_dict['PERSON'] = []
                    fintuple_dict['Source'] = ""
                    for n in range(0, len(ner_list)):
                        if ner_list[n][1] == 'O' or ner_list[n][1] == "LOCATION" or ner_list[n][1] == "ORGANIZATION":
                            ner_list[n] = ""
                    ner_list = list(filter(None, ner_list))
                    if(ner_list == []):
                        continue
                    for n in range(0, len(ner_list)):
                        fintuple_dict["PERSON"].append(ner_list[n][0])

                    if (webaddr.find("www") == -1):
                        webaddr_list = webaddr.split("/")
                        fintuple_dict["Source"] = webaddr_list[2]
                    else:
                        webaddr_list = webaddr.split(".")
                        fintuple_dict["Source"] = webaddr_list[1]

                    data_list.append(fintuple_dict)
                    print(data_list)
                time.sleep(2)
                with open(club_dict[cname], mode='w') as f:
                    json.dump(data_list, f)
        except Exception as e:
            print(e)
    f.close()