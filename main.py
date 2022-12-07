import tkinter as tk
from tkinter import font

MAX_ATTEMPTS = 9
BACKGROUND_COLOR = "#FFFFFF"
FIELD_COLOR = "#198F7F"
HEIGHT = "580"
WIDTH = "350"
START_TEXT = "Speler X begint het spel"


class Game(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Boter, kaas & eieren")
        self.configure(background=BACKGROUND_COLOR)
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.resizable(False, False)

        self.board_header()
        self.board_grid()
        self.board_footer()

        self.active_players = [self.Player("X"), self.Player("O")]
        self.players = (self.active_players[(attempts + 1) % len(self.active_players)]
                        for attempts in range(1, MAX_ATTEMPTS + 2))
        self.used_fields = []
        self.game_over = False

    class Player:
        def __init__(self, symbol: str):
            self.score = {
                "row0": 0,
                "row1": 0,
                "row2": 0,

                "col0": 0,
                "col1": 0,
                "col2": 0,

                "d0": 0,
                "d1": 0
            }

            self.player_symbol = symbol

        def __repr__(self):
            return f"Player {self.player_symbol}"

        def update_score(self, row_n: int, col_n: int) -> None:
            """Update score voor elke mogelijke combinatie"""
            self.score[f"row{row_n}"] += 1
            self.score[f"col{col_n}"] += 1

            # Check of diagonale combinatie mogelijk is
            if row_n == col_n:
                self.score["d0"] += 1
            if row_n + col_n == 2:
                self.score["d1"] += 1


    def board_header(self):
        """Plaatst header text bovenaan in de window"""
        grid_frame = tk.Frame(master=self, background=BACKGROUND_COLOR)
        grid_frame.pack()
        self.header_button = tk.Button(master=grid_frame,
                                       text="Opnieuw beginnen",
                                       font=font.Font(size=12),
                                       background=BACKGROUND_COLOR,
                                       command=self.reset_game)
        self.header_button.grid(column=1,row=0, padx=5, pady=5)

    def board_grid(self):
        """Plaatst een 3x3 grid in een apart frame"""
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(3):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(3):
                field = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    bg=FIELD_COLOR,
                    width=3,
                    height=2,
                    name=str([row, col]),

                )
                field.row = row
                field.col = col
                field.bind("<Button-1>", self.process_movement)
                field.grid(
                    row=row,
                    column=col,
                    padx=2,
                    pady=2,
                )

    def board_footer(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        self.footer_text = tk.Label(text=START_TEXT,
                                    font=font.Font(size=20),
                                    background=BACKGROUND_COLOR)
        self.footer_text.pack()

    def process_movement(self, event: tk.Event) -> None:
        """Verwerk zet van speler X en check of speler X heeft gewonnen of gelijkspel"""
        if not self.game_over:
            field = event.widget
            move = str(field).split(".")[-1]

            # In de eerste beurt moet direct een speler toegewezen worden - Anders gebruik active speler
            if not self.used_fields:
                player = self.switch_player()
            else:
                player = self.active

            # Valideer de zet op het selecteren van een leeg veld
            if self.is_valid_move(move):
                self.move_player(player, move, field)

            if self.is_winner(player):
                self.end_game(message=f"Speler {player.player_symbol} wint het spel!")
            elif self.is_tie():
                self.end_game(message="Gelijkspel!")

    def is_valid_move(self, move: str) -> bool:
        """Controleer of gekozen veld al eerder is gekozen"""
        return move not in self.used_fields

    def draw_symbol(self, player_sym: str, field: tk.Button) -> None:
        """Plaats symbool van speler op gekozen veld"""
        field['text'] = player_sym

    def move_player(self, player: Player, movement: str, field: tk.Button) -> None:
        """Plaats speler symbool op gekozen veld"""
        used_field = movement
        self.draw_symbol(player.player_symbol, field)
        self.used_fields.append(used_field)

        player.update_score(row_n=field.row, col_n=field.col)

        # Update actieve speler
        self.active = self.switch_player()
        self.footer_text['text'] = f"Speler {self.active.player_symbol} is aan zet"

    def switch_player(self) -> Player:
        """Return volgende item in generator"""
        return next(self.players)

    @staticmethod
    def is_winner(player: Player) -> bool:
        """Return true als een van de drie score categorien gelijk aan drie is"""
        for item in player.score.values():
            if item == 3:
                return True

    def is_tie(self) -> bool:
        """Return true als alle velden gebruikt zijn"""
        return len(self.used_fields) == MAX_ATTEMPTS

    def end_game(self, message: str) -> None:
        """Disable buttons, toon message en stop het spel"""
        self.footer_text['text'] = message

        # Disable alle velden
        for w in self.winfo_children():
            for item in w.winfo_children():
                if str(w) == ".!frame2":
                    item['state'] = 'disabled'
        self.game_over = True

    def reset_game(self) -> None:
        """Reset alle attributen voor opnieuw beginnen van spel"""
        self.active_players = [self.Player("X"), self.Player("O")]
        self.players = (self.active_players[(attempts + 1) % len(self.active_players)]
                        for attempts in range(1, MAX_ATTEMPTS + 2))
        self.used_fields = []
        self.game_over = False
        self.footer_text['text'] = START_TEXT

        # Enable alle velden
        for w in self.winfo_children():
            for item in w.winfo_children():
                if str(w) == ".!frame2":
                    item.config(text="")
                    item['state'] = 'normal'


def main():
    game = Game()
    game.mainloop()


if __name__ == '__main__':
    main()
