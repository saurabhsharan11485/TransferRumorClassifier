from DWD_Project import Players as pextract
from DWD_Project import PlayerData_Insert as pinsert
from DWD_Project import ArticleExtraction as aextract
from DWD_Project import ArticleData_Insert as ainsert
from DWD_Project import Comparison as comp
from DWD_Project import VisualizeRumours as vis

if __name__ == "__main__":

    pextract.PlayerExtraction()
    pinsert.PlayerInsert()
    aextract.ArticleExtraction()
    ainsert.ArticleDBInsert()
    comp.compare()
    vis.Visualize()
    print("Project completed")
