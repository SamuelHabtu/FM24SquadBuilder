from role import Role
import json

class Formation:
    def __init__(self):

        self.forward_line = None
        self.attacking_mf_line = None
        self.midfield_line = None
        self.defensive_mf_line = None
        self.defensive_line = None
        self.lines = []
        #this list will be where all of the roles are stored(and players will get fit into)
        self.positions = dict({})
        self.roles = self.addRoles()

    def inputFormation(self):

        print("What formation are you using?")
        print("NOTE: you have to give me this line by line from top to bottom, so for example if you are running a 442")
        print("It would look like this:")
        print("01010\n00000\n11011\n00000\n11011")
        print("0 means a player is NOT in this spot and 1 means they are")
        print("Lets start with the Forward line: (- ST(L) ST ST(R) -) from left to right:")
        forward_line = input(": ")
        print("Now give me the Attacking mid field Line: (AML AMC(L) AMC AMC(R) AMR)")
        attacking_mf_line = input(": ")
        print("Now give me the Midfield line: (ML MC(L) MC MC(R) MR )")
        midfield_line = input(": ")
        print("Now give me the Defensive midfield line: (WBL DM(L) DM DM(R) WBR)")
        defensive_mf_line = input(": ")
        print("Finally your Defensive Line: (LB DC(L) DC DC(R) RB)")
        defensive_line = input(": ")
        self.forward_line = interpretLine(forward_line)
        self.attacking_mf_line = interpretLine(attacking_mf_line)
        self.midfield_line = interpretLine(midfield_line)
        self.defensive_mf_line = interpretLine(defensive_mf_line)
        self.defensive_line = interpretLine(defensive_line)
        self.lines = [
            self.forward_line, 
            self.attacking_mf_line, 
            self.midfield_line, 
            self.defensive_mf_line, 
            self.defensive_line
            ]


    def displayFormation(self):
        print("Here is your formations basic positions: ")
        for line in self.lines:
            print(line)

    def addRoles(self, file_name = "baseweights.json"):
        
        file = open(f'data/{file_name}')
        role_duty_weights = json.load(file)
        roles = dict({})

        for role in role_duty_weights:
            temp_role, temp_duty = role.split("-")
            roles[role] = Role(temp_role, temp_duty, role_duty_weights[role])
        #Setting the key and important Attributes for each role:
        #Goalie Roles:
        roles["GoalKeeper-Defend"].updateWeights(["Aer", "Cmd", "Com", "Han", "Kic", "Ref", "Ant", "Con", "Pos", "Agi"], ["1v1", "Thr", "Dec"])
        roles["SweeperKeeper-Defend"].updateWeights(["Cmd", "Kic", "1v1", "Ref", "Ant", "Con", "Pos", "Agi"], ["Aer", "Com", "Fir", "Han", "Pas", "TRO", "Thr", "Cmp", "Dec", "Vis"])
        roles["SweeperKeeper-Support"].updateWeights(["Cmd", "Kic", "1v1", "TRO", "Ant", "Cmp", "Con", "Pos", "Agi"], ["Aer", "Com", "Fir", "Han", "Pas", "Thr", "Vis", "Acc"])
        roles["SweeperKeeper-Attack"].updateWeights(["Cmd", "Kic", "1v1", "TRO", "Ant", "Cmp", "Con", "Pos", "Agi"], ["Aer", "Com", "Fir", "Han", "Pas", "Thr", "Vis", "Acc", "Ecc"])

        #LRFB Roles:
        roles["FullBack-Defend"].updateWeights(["Mar", "Tck", "Ant", "Con", "Pos"], ["Cro", "Pas", "Tea", "Wor", "Pac", "Sta"])
        roles["FullBack-Support"].updateWeights([], [])
        roles["FullBack-Attack"].updateWeights([], [])
        roles["NoNonsenseFullBack-Defend"].updateWeights([], [])
        roles["InvertedFullBack-Defend"].updateWeights([], [])


        #CD Roles:

        #WBLR Roles:

        #DM Roles:

        #MLR Roles:

        #MC Roles:

        #AMLR Roles:

        #AMC Roles:

        #FWD Roles:

        return roles

        
def interpretLine(line):
    result = 0
    for i in range(len(line)):
        if line[i] == "1":
            result += 2**i
    return result

if __name__ == "__main__":

    test = Formation()
