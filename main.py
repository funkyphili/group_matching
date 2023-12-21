import random
from collections import Counter

playerlist = []
groups = []
teamSize = 5
signups = 23
rounds = 13


class person:

    def __init__(self, name):
        self.name = name
        self.played = []

    def add_played(self, name_list):
        for name in name_list:
            self.played.append(name)

    def amount_played(self, name):
        return self.played.count(name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __lt__(self, other):
        return len(self.played) < len(other.played)

    def amount_of_partners(self):
        return len(self.played)





def update_groupings():
    """
    updates the played with list of each player in each group, then recombines players into the list
    :return:
    """
    global groups, playerlist
    playerlist = []

    for group in groups:

        #extra code to print out sorted groups
        group_print = [int(str(i)) for i in group]
        group_print.sort()
        print(group_print,end="")

        for player in group:
            others = group.copy()
            others.remove(player)
            player.add_played(others)
            playerlist.append(player)
    print("")


def initial_split():
    global groups, playerlist

    for i in range(0, len(playerlist), teamSize):
        x = i
        group = playerlist[x:x + teamSize]
        groups.append(group)


def split_players():
    global groups, playerlist
    groups = []
    current_group = 0
    # calculate required groups
    amount_groups = (len(playerlist) // teamSize) + 1
    for i in range(amount_groups):
        groups.append([])

    # assing byes
    playerlist.sort()  # sort by times played for determining byes
    bye = len(playerlist) % teamSize
    for i in range(bye):
        groups[-1].append(playerlist.pop(-1))


    while playerlist:

        if len(playerlist) == teamSize:  # skip trying to find a group for the last group duh
            groups[current_group] = playerlist
            return

        random.shuffle(playerlist)
        possible_matches = playerlist.copy()
        for enum, entry in enumerate(possible_matches):  # add score to players for partner matching
            possible_matches[enum] = [entry, 0]

        for i in range(teamSize - 1):    # for each teammember
            cur_player = possible_matches.pop(0)[0]   #add to team
            playerlist.remove(cur_player)             #remove from future pairings
            groups[current_group].append(cur_player)   #add to group
            for entry in possible_matches:
                score = cur_player.played.count(entry[0])  #assign a score to other players based on the amount of times the player played with them
                score = score * random.uniform(0.99, 1.01)  # add random jitter to prevent same groups forming after a while
                entry[1] = entry[1] + score

            possible_matches = sorted(possible_matches, key=lambda x: x[1])  # sort after score

        last_player = possible_matches.pop(0)[0]   #take the player with the lowest score of remaining possible people
        groups[current_group].append(last_player)
        playerlist.remove(last_player)
        current_group += 1
    return


if __name__ == '__main__':

    for i in range(signups):
        playerlist.append(person(str(i)))   # create people with digits as names


initial_split()
playerlist = []
for i in range(rounds):
    update_groupings()
    split_players()

print("")
update_groupings()

# some info on how well matches are made
statistic = []
for player in playerlist:
    for played_with in playerlist:
        statistic.append(player.amount_played(played_with))  # printing a 2d array with the amount of times 2 players played with each other
        print(player.amount_played(played_with), end="")
    print("")

for i in range(signups):  # a player never plays with it self, therefore remove num signups of zeros from the statistic
    statistic.remove(0)
print(Counter(statistic))   # counting the overall "times played with" results