import os
import time
import random

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


class Player:
    def __init__(self, is_ai=False):
        self.name = ""
        self.symbol = ""
        self.is_ai = is_ai

    def choose_name(self):
        if self.is_ai:
            self.name = "Computer 🤖"
            return

        while True:
            name = input("Enter your name: ")
            if name.isalpha():
                self.name = name
                break
            print("Invalid name.")

    def choose_symbol(self):
        while True:
            symbol = input(f"{self.name}, choose symbol: ")
            if symbol.isalpha() and len(symbol) == 1:
                self.symbol = symbol.upper()
                break
            print("Invalid symbol.")


class Board:
    def __init__(self):
        self.reset_board()

    def display_board(self):
        print("\n╔═══╦═══╦═══╗")
        for i in range(0, 9, 3):
            print(f"║ {self.board[i]} ║ {self.board[i+1]} ║ {self.board[i+2]} ║")
            if i < 6:
                print("╠═══╬═══╬═══╣")
        print("╚═══╩═══╩═══╝\n")

    def update_board(self, choice, symbol):
        if self.board[choice - 1].isdigit():
            self.board[choice - 1] = symbol
            return True
        return False

    def available_moves(self):
        return [i+1 for i in range(9) if self.board[i].isdigit()]

    def check_winner(self, symbol):
        b = self.board
        combos = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]
        return any(b[c[0]] == b[c[1]] == b[c[2]] == symbol for c in combos)

    def is_full(self):
        return all(not cell.isdigit() for cell in self.board)

    def reset_board(self):
        self.board = [str(i) for i in range(1, 10)]


class Game:
    def __init__(self):
        self.players = []
        self.board = Board()
        self.current_index = 0

    def start(self):
        while True:  # 🔁 إعادة اللعب
            clear_screen()
            print("🎮 XO GAME")
            print("1. Player vs Player")
            print("2. Player vs Computer")
            choice = input("Choose mode: ")

            if choice == "1":
                self.setup_pvp()
            else:
                self.setup_ai()

            self.play()

            # 🔁 سؤال إعادة اللعب
            again = input("\n🔁 Play again? (y/n): ").lower()
            if again != "y":
                print("👋 Goodbye!")
                break

            self.board.reset_board()
            self.current_index = 0

    def setup_pvp(self):
        p1 = Player()
        p2 = Player()

        print("\nPlayer 1:")
        p1.choose_name()
        p1.choose_symbol()

        print("\nPlayer 2:")
        p2.choose_name()
        p2.choose_symbol()

        self.players = [p1, p2]

    def setup_ai(self):
        human = Player()
        ai = Player(is_ai=True)

        print("\nPlayer:")
        human.choose_name()
        human.choose_symbol()

        ai.symbol = "O" if human.symbol != "O" else "X"

        self.players = [human, ai]

    def play(self):
        while True:
            clear_screen()
            self.board.display_board()

            player = self.players[self.current_index]

            if player.is_ai:
                print("🤖 Computer thinking...")
                time.sleep(1)
                move = self.best_move(player)
            else:
                print(f"{player.name}'s turn ({player.symbol})")
                move = self.get_move()

            self.board.update_board(move, player.symbol)

            if self.board.check_winner(player.symbol):
                clear_screen()
                self.board.display_board()

                if player.is_ai:
                    print("💀 You lost! Computer wins 🤖")
                else:
                    print(f"🏆 {player.name} wins! 🎉")
                break

            if self.board.is_full():
                clear_screen()
                self.board.display_board()
                print("🤝 Draw!")
                break

            self.current_index = 1 - self.current_index

    def get_move(self):
        while True:
            try:
                move = int(input("Choose (1-9): "))
                if move in self.board.available_moves():
                    return move
                print("❌ Invalid move.")
            except:
                print("⚠ Enter number.")

    # 🤖 AI
    def best_move(self, player):
        opponent = self.players[0] if player == self.players[1] else self.players[1]

        best_score = -float('inf')
        move = random.choice(self.board.available_moves())

        for m in self.board.available_moves():
            self.board.board[m-1] = player.symbol
            score = self.minimax(False, player, opponent)
            self.board.board[m-1] = str(m)

            if score > best_score:
                best_score = score
                move = m

        return move

    def minimax(self, is_max, ai, human):
        if self.board.check_winner(ai.symbol):
            return 1
        if self.board.check_winner(human.symbol):
            return -1
        if self.board.is_full():
            return 0

        if is_max:
            best = -float('inf')
            for m in self.board.available_moves():
                self.board.board[m-1] = ai.symbol
                score = self.minimax(False, ai, human)
                self.board.board[m-1] = str(m)
                best = max(best, score)
            return best
        else:
            best = float('inf')
            for m in self.board.available_moves():
                self.board.board[m-1] = human.symbol
                score = self.minimax(True, ai, human)
                self.board.board[m-1] = str(m)
                best = min(best, score)
            return best


# تشغيل اللعبة
game = Game()
game.start()