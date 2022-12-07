from main import Game
import tkinter
import pytest

def test_is_valid_move():
    game = Game()
    game.used_fields = ["[2, 2]", "[0, 2]", "[0, 0]"]
    assert game.is_valid_move("[1,2]")


def test_is_not_valid_move():
    game = Game()
    game.used_fields = ["[2, 2]", "[0, 2]", "[0, 0]"]
    assert not game.is_valid_move("[2, 2]")


def test_draw_symbol_valid_field_input():
    game = Game()
    player_symbol = "X"
    field = tkinter.Button()
    game.draw_symbol(player_symbol, field)


def test_draw_symbol_invalid_field_input():
    with pytest.raises(TypeError):
        game = Game()
        player_symbol = "X"
        field = [1, 2]
        game.draw_symbol(player_symbol, field)


def test_update_score_correct():
    player = Game.Player("X")
    player.update_score(row_n=2, col_n=1)
    assert player.score["row2"] == 1 & player.score["col1"] == 1


def test_update_score_key_not_found():
    with pytest.raises(KeyError):
        player = Game.Player("X")
        player.update_score(row_n=2, col_n=3)


def test_is_winner():
    player = Game.Player("X")
    player.score["row1"] = 3
    assert Game.is_winner(player)


def test_is_no_winner():
    player = Game.Player("X")
    player.score["row1"] = 2
    assert not Game.is_winner(player)


def test_is_tie():
    game = Game()
    game.used_fields = [[0, 0],
                        [0, 1],
                        [0, 2],
                        [1, 0],
                        [1, 1],
                        [1, 2],
                        [2, 0],
                        [2, 1],
                        [2, 2]]
    assert game.is_tie()


def test_is_not_tie():
    game = Game()
    game.used_fields = [[0, 0],
                        [0, 1],
                        [0, 2],
                        [1, 0],
                        [1, 1],
                        [1, 2],
                        [2, 0],
                        [2, 1]]
    assert not game.is_tie()

def test_playerX_starts():
    game = Game()
    attempt = 1
    for _ in range(attempt):
        player = game.switch_player()
    assert str(player) == "Player X"

def test_switch_player():
    game = Game()
    attempt = 2
    for _ in range(attempt):
        player = game.switch_player()
    assert str(player) == "Player O"

def test_iteration_error_switch_player_when_no_moves_left():
    game = Game()
    with pytest.raises(StopIteration):
        attempt = 10
        for _ in range(attempt+1):
            player = game.switch_player()

