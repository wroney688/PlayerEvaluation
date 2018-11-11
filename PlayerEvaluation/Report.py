import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

class Report:
    DEBUG = True

    def __init__(self):
        self.DataFrame = None
        return 

    def load(self, ifile):
        if (self.DEBUG): print "\033[4;34mLoading Dataset from : ", ifile, "\033[0m"
        self.DataFrame = pd.read_excel(ifile)
        #print type(self.DataFrame)
        #print self.DataFrame
        return
        
    def saveResult(self, ifile, ofname):
        self.load(ifile)
        if (self.DEBUG): print "\033[4;34mSaving Results to: ", ofname, "\033[0m"
        rptfile = open(ofname, 'w+')
        rptfile.write("<html><title>Player Evaluations</title><body>")
        rptfile.write("<h1>Team Summary</h1>")
        rptfile.write(self.outputHeader())
        rptfile.write("<p><table border=\"0\">")
        rptfile.write("<tr><td width=\"50%\">")
        rptfile.write(self.outputTechnical())
        rptfile.write("</td><td width=\"50%\">")
        rptfile.write(self.outputTactical())
        rptfile.write("</td></tr><tr><td width=\"50%\">")
        rptfile.write(self.outputPhysical())
        rptfile.write("</td><td width=\"50%\">")
        rptfile.write(self.outputPsychological())
        rptfile.write("</td></tr></table>")
        rptfile.write("<p style=\"page-break-after: always;\">")
        for player in self.DataFrame.PlayerName.unique():
            rptfile.write(self.outputHeader(player))
            rptfile.write("<p><table border=\"0\">")
            rptfile.write("<tr><td width=\"50%\">")
            rptfile.write(self.outputTechnical(player))
            rptfile.write("</td><td width=\"50%\">")
            rptfile.write(self.outputTactical(player))
            rptfile.write("</td></tr><tr><td width=\"50%\">")
            rptfile.write(self.outputPhysical(player))
            rptfile.write("</td><td width=\"50%\">")
            rptfile.write(self.outputPsychological(player))
            rptfile.write("</td></tr></table><hr>")
            rptfile.write(self.outputCommentary(player))
            rptfile.write("<p style=\"page-break-after: always;\">")
        
        rptfile.write("</body></html>")
        rptfile.close()
        return
        
    def outputHeader(self, player=None):
        fig, bp = plt.subplots(nrows=1, ncols=1)
        fig.set_size_inches(2.5,2.5)
        years = list(self.DataFrame[(self.DataFrame.Rater == "Coach")].BirthYear)
        mine = list(self.DataFrame[(self.DataFrame.Rater == "Coach") & (self.DataFrame.PlayerName == player)].BirthYear)
        period = self.DataFrame.Period[0]
        bp.set_ylim(top=min(years)-2, bottom=max(years)+2)
        bp.violinplot(years, showextrema=False)
        buffer = ""
        if player is not None:
            plt.title("Player vs Team Age")
            buffer = buffer + "<h1 align=center>" + player + ", " + period + "</h1>"
            plt.annotate(player,
                        xy=(1, mine[0]), 
                        xycoords='data')        
        else:
            plt.title("Team Age")
        
        plt.setp(   bp, 
                yticks=[y for y in range(min(years)-2, max(years)+3)])
        p1 = BytesIO()
        plt.tight_layout()
        plt.savefig(p1, format="jpg")
        p1.seek(0)
        p1_png = base64.b64encode(p1.getvalue())
        plt.close(fig)

        buffer = buffer + "<img src=\"data:image/jpg;base64," + p1_png + "\" />"
        return buffer

    def genGraph(self, name, title, cats):
        buffer = ""
        fig, bp = plt.subplots(nrows=1, ncols=1)
        fig.set_size_inches(4.5,3.5)
        plt.title(title)
        
        ratings = ["Needs Improvement",
                 "Poor",
                 "Average",
                 "Very Good",
                 "Excellent"]

        
        plotdata = []
        myratings = []
        coachratings = []
        for cat in cats:
            samps = list(self.DataFrame[self.DataFrame.Rater == "Coach"][cat])
            me = list(self.DataFrame[(self.DataFrame.Rater == "Player") & (self.DataFrame.PlayerName == name)][cat])
            coach = list(self.DataFrame[(self.DataFrame.Rater == "Coach") & (self.DataFrame.PlayerName == name)][cat])
            plotdata.append(samps)
            if len(me) > 0: myratings.append(me)
            else:  myratings.append([0])
            if len(coach) > 0: coachratings.append(coach)
            else:  coachratings.append([0])
        bp.violinplot(plotdata, showextrema=False)
        plt.ylim(0.5, len(ratings)+0.5)
        xt = [x for x in range(1, len(cats)+1)]
        plt.xticks(xt, cats, rotation='vertical')
        plt.yticks([y for y in range(1, len(ratings)+1)], ratings)

        if name is not None:
            bp.scatter(xt, myratings, label="Player", color='r', marker='>')
            bp.scatter(xt, coachratings, label="Coach", color='b', marker='<')
            bp.legend(fontsize='x-small')
            

        p1 = BytesIO()
        plt.tight_layout()
        plt.savefig(p1, format="jpg")
        p1.seek(0)
        p1_png = base64.b64encode(p1.getvalue())
        plt.close(fig)

        buffer = "<img src=\"data:image/jpg;base64," + p1_png + "\" />"
        return buffer
        
    def outputTechnical(self, name=None):
        cats = ["Dribbling",
                "LongPass",
                "ShortPass",
                "Heading",
                "Tackling",
                "Shooting",
                "GroundFirstTouch",
                "AirFirstTouch"]
        return self.genGraph(name, "Technical", cats)
        
    def outputTactical(self, name=None):
        cats = ["DecisionMaking",
                "SpeedOfPlay",
                "FieldVision",
                "1v1Attack",
                "1v1Defend",
                "Positioning",
                "ZonalDefending",
                "Mobility"]
        return self.genGraph(name, "Tactical", cats)
        
    def outputPhysical(self, name=None):
        cats = ["Speed",
                "Agility",
                "Quickness",
                "Strength",
                "Power",
                "Balance",
                "Flexibility",
                "Endurance"]
        return self.genGraph(name, "Physical", cats)
        
    def outputPsychological(self, name=None):
        cats = ["Composure",
                "Commitment",
                "Leadership",
                "Motivation",
                "Focus",
                "Attitude",
                "Determination",
                "Teamwork"]
        return self.genGraph(name, "Psychological", cats)
        
    def outputCommentary(self, name):
        coachcomment = ""
        playercomment = ""
        comments = self.DataFrame.set_index("PlayerName", drop = False).loc[name, ["Rater", "Comments"]].values
        if len(comments.shape) == 1:
                if comments[0] == "Coach":
                    coachcomment = comments[1]
                elif comments[0] == "Player":
                    playercomment = comments[1]
        else:
            for com in comments:
                if com[0] == "Coach":
                    coachcomment = com[1]
                elif com[0] == "Player":
                    playercomment = com[1]
        buffer = "<table>"
        buffer = buffer + "<tr><td>Coach Comments:</td><td>" + coachcomment + "</td><tr>"
        buffer = buffer + "<tr><td>Player Comments:</td><td>" + playercomment + "</td><tr>"
        buffer = buffer + "</table>"
        return buffer
