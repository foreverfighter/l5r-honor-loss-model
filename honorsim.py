import csv
import random

# inputs
# the amount of honor lost during the game
# each player's starting honor

# output
# cards drawn by each player by the end of the game

STARTING_HONOR = 11


class Player:

    def __init__(self):
        self.honor = 11
        self.cards_drawn = 0
        self.honor_lost_from_conf = 0


class Game:

    def __init__(self):
        self.players = []
        self.log = [
            'p1honor,p1drawn,p1honor_lost_from_conf,p2honor,p2drawn,p2honor_lost_from_conf'
        ]

    def draw_phase(self):
        bids = []
        for p in self.players:
            bid = max(min(5, p.honor - 2), 1)
            p.cards_drawn += bid
            bids.append(bid)
        bid_diff = bids[0] - bids[1]
        self.players[0].honor -= bid_diff
        self.players[1].honor += bid_diff

    def conflict_phase(self):
        for p in self.players:
            roll = random.randint(1, 100)
            if roll <= 30:
                honor_to_lose = 0
            elif roll <= 50:
                honor_to_lose = 1
            elif roll <= 70 and p.honor > 4:
                honor_to_lose = 2
            elif roll <= 90 and p.honor > 5:
                honor_to_lose = 3
            elif p.honor > 5:
                honor_to_lose = 4
            else:
                honor_to_lose = 1
            p.honor -= honor_to_lose
            p.honor_lost_from_conf += honor_to_lose

    def log_stats(self):
        self.log.append(
            f'{self.players[0].honor},{self.players[0].cards_drawn},{self.players[0].honor_lost_from_conf},{self.players[1].honor},{self.players[1].cards_drawn},{self.players[1].honor_lost_from_conf}'
        )

    def reset_stats(self):
        for p in self.players:
            p.honor = 11
            p.cards_drawn = 0
            p.honor_lost_from_conf = 0


game = Game()
game.players.append(Player())
game.players.append(Player())
for i in range(1000):
    for i in range(5):
        game.draw_phase()
        game.conflict_phase()
    game.log_stats()
    game.reset_stats()

with open('data.csv', "w") as f:
    for line in game.log:
        f.write(line + '\n')
