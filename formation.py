class formation:
    def __init__(self):
        print("What formation are you using?")
        print("NOTE: you have to give me this line by line from top to bottom, so for example if you are running a 442")
        print("It would look like this:")
        print("01010\n00000\n11011\n00000\n11011")
        print("0 means a player is NOT in this spot and 1 means they are")
        print("Lets start with the Forward line(- ST(L) ST(C) ST(R) -) from left to right:")
        forward_line = input(": ")
        
        self.forward_line = interpretLine(forward_line)
        print(self.forward_line)

def interpretLine(line):
    result = 0
    for i in range(len(line)):
        if line[i] == "1":
            result += 2**i
    return result

if __name__ == "__main__":

    test = formation()