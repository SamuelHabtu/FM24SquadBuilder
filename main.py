import os
import sys
import players
import formation
def getTeam(team_name):
    with open(f"teams/{team_name}", "r") as file:
        team_data = file.read()
    print(team_data.split("|"))


def main():
    team_files = []
    #gather all files within the teams folder
    for entry in os.listdir('./teams'):
        team_files.append(entry)
    print("Which team do you want to optimize for your tactic(If you don't see the team you want to use make sure the file is in the teams folder)?")
    for i in range(len(team_files)):
        print(f"{i + 1}: {team_files[i]}")
    team = team_files[int(input(": ")) - 1]
    getTeam(team)



if __name__ == "__main__":
    main()
