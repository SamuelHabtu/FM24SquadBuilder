class Formation:
    def __init__(self):

        self.forward_line = None
        self.attacking_mf_line = None
        self.midfield_line = None
        self.defensive_mf_line = None
        self.defensive_line = None
        self.lines = []

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


def interpretLine(line):
    result = 0
    for i in range(len(line)):
        if line[i] == "1":
            result += 2**i
    return result

if __name__ == "__main__":

    test = formation()