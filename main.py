import os
from player import Player
from formation import Formation

def getTeam(team_name):

    players = []
    with open(f"teams/{team_name}", "r", encoding= "utf-8") as file:
        lines = file.readlines()
        
        # Process the header to get attribute names
        lines = [line.strip() for line in lines if line.strip() and '---' not in line]
        headers = [header.strip() for header in lines[0].split("|") if header.strip()]
        headers = headers[1:]  # Skip 'Name' column in headers
        for line in lines[1:]:
            values = [value.strip() for value in line.split("|") if value.strip()]
            if len(values) == len(headers) + 1:  # Ensure there are enough values
                name = values[0]
                attributes = {headers[i]: int(values[i+1]) for i in range(len(headers))}
                players.append(Player(name=name, attributes=attributes))
    
    return players

def main():
    team_files = []
    #gather all files within the teams folder
    for entry in os.listdir('./teams'):
        team_files.append(entry)
    print("Which team do you want to optimize for your tactic(If you don't see the team you want to use make sure the file is in the teams folder)?")
    for i in range(len(team_files)):
        print(f"{i + 1}: {team_files[i]}")
    team_file_name = team_files[int(input(": ")) - 1]
    roster = getTeam(team_file_name)
    for player in roster:
        print(f"Name: {player.name}, Attributes: {player.attributes}")



if __name__ == "__main__":
    main()
