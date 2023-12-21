import random
from collections import Counter

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

    def amount_partners(self):
        return len(self.played)


playerlist = []
groups = []
teamSize = 5
signups = 23
rounds = 13


def update_groupings():
    global groups, playerlist
    playerlist = []

    for group in groups:
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


def split_list_generic():
    global groups, playerlist
    groups = []
    current_group = 0
    amount_groups = (len(playerlist) // teamSize) + 1
    for i in range(amount_groups):
        groups.append([])

    # freilose generieren
    freilose = len(playerlist) % teamSize
    for i in range(freilose):
        groups[-1].append(playerlist.pop(-1))

    while playerlist:

        if len(playerlist) == teamSize:
            groups[current_group] = playerlist
            return
        random.shuffle(playerlist)
        possible_matches = playerlist.copy()
        for enum, entry in enumerate(possible_matches):  # score for partner matching
            possible_matches[enum] = [entry, 0]

        for i in range(teamSize - 1):
            cur_player = possible_matches.pop(0)[0]
            playerlist.remove(cur_player)
            groups[current_group].append(cur_player)
            for entry in possible_matches:
                score = cur_player.played.count(entry[0])
                score = score * random.uniform(0.99, 1.01)
                entry[1] = entry[1] + score

            possible_matches = sorted(possible_matches, key=lambda x: x[1])

        last_player = possible_matches.pop(0)[0]
        groups[current_group].append(last_player)
        playerlist.remove(last_player)
        current_group += 1
    return


if __name__ == '__main__':

    for i in range(signups):
        playerlist.append(person(str(i)))

# random.shuffle(playerlist)
initial_split()
playerlist = []
for i in range(rounds):
    update_groupings()
    playerlist.sort()
    split_list_generic()
    pass
print("")
update_groupings()
statistic = []
for player in playerlist:
    for played_with in playerlist:
        statistic.append(player.amount_played(played_with))
        print(player.amount_played(played_with), end="")
    print("")

for i in range(signups):
    statistic.remove(0)
print(Counter(statistic))