import random

class Card:
    def __init__(self, attack, defense, pitch, effect, cost, name):
        self.attack = attack
        self.defense = defense
        self.pitch = pitch
        self.effect = effect
        self.cost = cost
        self.value = (attack - cost) / (defense - pitch)


class Player:
    def __init__(self, deck):
        self.life = 20
        self.hand = []
        self.deck = deck
        random.shuffle(self.deck)
        self.draw(4)

    def draw(self, num_cards):
        for i in range(num_cards):
            if len(self.deck) > 0:
                card = self.deck.pop(0)
                self.hand.append(card)

    def play_card(self, card_index):
        if card_index >= 0 and card_index < len(self.hand):
            card = self.hand[card_index]
            if card.cost <= sum(c.pitch >= card.cost for c in self.hand):
                self.hand.pop(card_index)
                return card
        return None

    def block(self, card_indices):
        defense = 0
        for index in card_indices:
            if index >= 0 and index < len(self.hand):
                card = self.hand[index]
                defense += self.hand[index].defense
                print(f"Player blocked with {card.name}, Defense: {card.defense}")
        return defense


class Game:
    def __init__(self, deck_size):
        self.deck = [
            Card(4, 3, 1, "go again", 1, "blackout kick"),
            Card(3, 4, 1, "", 1, "sideways kick"),
            Card(4, 3, 1, "go again", 1, "blackout kick"),
            Card(4, 3, 1, "go again", 1, "blackout kick"),
        ]
        for i in range(deck_size - 4):
            card = self.deck[i % 4]
            self.deck.append(card)
        random.shuffle(self.deck)
        self.player1 = Player(self.deck[:4])
        self.player2 = Player(self.deck[4:8])
        self.turn = 1

    def start(self):
        while self.player1.life > 0 and self.player2.life > 0:
            print("Turn", self.turn)
            print("Player 1 life:", self.player1.life)
            print("Player 2 life:", self.player2.life)
            print("Player 1 hand:")
            for i, card in enumerate(self.player1.hand):
                print(
                    i + 1,
                    "-",
                    "Attack:",
                    card.attack,
                    "Defense:",
                    card.defense,
                    "Pitch:",
                    card.pitch,
                    "Effect:",
                    card.effect,
                    "Cost: ",
                    card.cost
                )
            card_index = int(input("Player 1, choose a card to play (1-4): ")) - 1
            while card_index < 0 or card_index >= len(self.player1.hand):
                card_index = (
                    int(input("Invalid input. Player 1, choose a card to play (1-4): "))
                    - 1
                )
            card = self.player1.play_card(card_index)
            if card is None:
                print(
                    "Invalid move. The card you want to play cannot be played without destroying a card with higher pitch."
                )
            else:
                print(
                    "Player 1 played a card with Attack:",
                    card.attack,
                    "Defense:",
                    card.defense,
                    "Pitch:",
                    card.pitch,
                    "Effect:",
                    card.effect,
                )
                if card.effect == "go again":
                    block_indeces = input("Player 2, choose a card to block (comma-seperated list): ")
                    block_indices = [int(i) - 1 for i in block_indices.split(",")]
                    while not all(i >= 0 and i < len(self.player2.hand) for i in block_indices):
                        block_indices = input("Invalid input. Player 2, choose cards to block (comma-separated list): ")
                        block_indices = [int(i) - 1 for i in block_indices.split(",")]
                    defense = self.player2.block(block_indeces)
                    print("Player 2 blocks with a total defense of ", defense)
                    if defense >= card.attack:
                        print("The full attack was blocked")
                    else:
                        self.player2.life -= max(card.attack - self.player2.block([]), 0)

            
                    
                    print("Player 2 life:", self.player2.life)
                    print("Player 1 gets to play again.")
                    
                else:
                    self.player2.life -= max(card.attack - self.player2.block([]), 0)
                    print("Player 2 life:", self.player2.life)
                    if self.player2.life <= 0:
                        break
                    self.player1.draw(4 - len(self.player1.hand))
                    self.turn += 1
                    print("Player 1's turn ends")
                    
                    
                    print("Player 1 drew", 4 - len(self.player1.hand), "cards.")
        if self.player1.life <= 0:
            print("Player 2 wins!")
        else:
            print("Player 1 wins!")

Game(4).start()