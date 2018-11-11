import itertools
from Piece import Piece, Pawn, Bishop, Knight, Rook, King, Queen
from utils import WHITE, BLACK, letters, numbers, convert_l_n_to_indexes, choose_field

"""
QUESTIONS:
1.self.so_sth ma samo to robic operujac na self.board czy prowadzic do self.board.do_sth? czy moze self.get_board().metoda? 
np. self.get_board().execute_move(piece_chosen, destination) - czy to nie wyglada dziwnie?
2. jak uniknac local variable might be referenced before assignment?
"""


class Game:

    def __init__(self) -> None:
        self.players = self.initialize_players()
        self.board = Board()
        self.current_player = self.players[1]
        self.turn_number = 1

    def get_board(self):
        return self.board

    def run(self):
        self.initialize_starting_board()
        finished = False
        while not finished:
            field_chosen, destination = None, None
            self.show_board()
            current_player = self.get_current_player()

            valid_piece_chosen = False
            while not valid_piece_chosen:
                print(f"{current_player.get_name()}'s move. Choose a piece to move")
                field_chosen = current_player.choose_a_piece_to_move()
                valid_piece_chosen = self.get_board().validate_piece_choice(field_chosen, current_player)
                if valid_piece_chosen:
                    piece_chosen = self.get_board().get_square_content(field_chosen[0], field_chosen[1])
                    print("You chose to move: " + str(piece_chosen) + " from " + str(field_chosen))
                    possible_moves = self.get_possible_moves(piece_chosen, field_chosen)
                    if not possible_moves:
                        print("You cannot move this piece!")
                        valid_piece_chosen = False
                    else:
                        print("Possible moves: " + str(possible_moves))

            valid_destination_chosen = False
            while not valid_destination_chosen:
                destination = current_player.choose_a_destination()
                if destination in possible_moves:
                    valid_destination_chosen = True
            self.get_board().execute_move(field_chosen, destination, piece_chosen)

    def get_possible_moves(self, piece_chosen, field_chosen):
        assert isinstance(piece_chosen, Piece)
        board = self.get_board()
        return piece_chosen.get_possible_moves(field_chosen, board)

    def initialize_starting_board(self):
        self.board.initialize_starting_board()

    def initialize_players(self):
        # name = input(("Welcome to the chess game.\nWhat's the name of 1st player?\n"))
        name = "walter"
        player1 = Player(name, WHITE)
        # name = input("What's the name of 2nd player?\n")
        name = "betty"
        player2 = Player(name, BLACK)
        print(
            f"{player1.get_name()} is {player1.get_color()} and {player2.get_name()} is {player2.get_color()}. Let's begin!\n")
        return player1, player2

    def get_current_player(self):
        id = 1 if self.current_player.get_id() == 0 else 0
        self.current_player = self.players[id]
        return self.current_player

    def show_board(self):
        print(self.board)

    def ask_if_again(self):
        correct_input = False
        while not correct_input:
            answer = input("\nDo you want to play again?\nPlease answer 'yes' or 'no'.")
            if answer == "yes":
                return False
            elif answer == "no":
                return True


class Board:

    def __init__(self) -> None:
        self.board = self.generate_board()

    def __repr__(self):
        repr = ""
        for number in reversed(numbers):
            line = str(number) + "  " + chr(9122)
            for letter in letters:
                line += "  " + str(self.get_square(letter, number))
            line += "\n"
            repr += line
        repr += "    " + chr(9148) * 33 + "\n       " + chr(9398) + "  " + chr(9399) + "  " + chr(
            9400) + "  " + chr(9401) + "  " + chr(
            9402) + "  " + chr(9403) + "  " + chr(9404) + "  " + chr(9405)
        return repr

    def generate_board(self):
        board = [[] for _ in range(8)]
        for idx, letter in enumerate(letters):
            for x in range(8):
                board[idx].append(Square(letter, x + 1))
        return board

    def initialize_starting_board(self):
        for letter in letters:
            self.set_square_content(letter, 7, Pawn(BLACK))
            self.set_square_content(letter, 2, Pawn(WHITE))
        for letter in ['a', 'h']:
            self.set_square_content(letter, 1, Bishop(WHITE))
            self.set_square_content(letter, 8, Bishop(BLACK))
        for letter in ['b', 'g']:
            self.set_square_content(letter, 1, Knight(WHITE))
            self.set_square_content(letter, 8, Knight(BLACK))
        for letter in ['c', 'f']:
            self.set_square_content(letter, 1, Rook(WHITE))
            self.set_square_content(letter, 8, Rook(BLACK))
        self.set_square_content('d', 1, Queen(WHITE))
        self.set_square_content('e', 8, Queen(BLACK))
        self.set_square_content('e', 1, King(WHITE))
        self.set_square_content('d', 8, King(BLACK))

    def get_square(self, l, n):
        x_axis, y_axis = convert_l_n_to_indexes(l, n)
        return self.board[x_axis][y_axis]

    def check_if_occupied(self, l, n):
        x_axis, y_axis = convert_l_n_to_indexes(l, n)
        return self.board[x_axis][y_axis].get_occupied()

    def execute_move(self, field_chosen, destination, piece_chosen):
        self.set_square_content(destination[0], destination[1], piece_chosen)
        self.get_square(field_chosen[0], field_chosen[1]).set_square_free()

    def get_square_content(self, l, n):
        x_axis, y_axis = convert_l_n_to_indexes(l, n)
        return self.board[x_axis][y_axis].get_piece()

    def set_square_content(self, l, n, piece):
        x_axis, y_axis = convert_l_n_to_indexes(l, n)
        o = self.board[x_axis][y_axis]
        o.set_square_with_piece(piece)

    def validate_piece_choice(self, field_chosen, current_player):
        letter_from = field_chosen[0]
        number_from = field_chosen[1]
        piece_chosen = self.get_square_content(letter_from, number_from)
        if not piece_chosen:
            print("There is no piece on this field!")
            return False
        if piece_chosen.get_color() != current_player.get_color():
            print("The chosen piece belongs to your opponent!")
            return False
        return True

    def move_piece(self, move_from, move_to):
        letter_from = move_from[0]
        number_from = move_from[1]
        source_content = self.get_square_content(letter_from, number_from)
        letter_to = move_to[0]
        number_to = move_to[1]
        destination_content = self.get_square_content(letter_to, number_to)
        if not destination_content or (
                destination_content and destination_content.get_color() != source_content.get_color()):
            source_content.validate_move()
        pass


class Square:

    def __init__(self, letter, number, occupied=False, piece=None):
        self.letter = letter
        self.number = str(number)
        self.occupied = occupied
        self.piece = piece

    def __repr__(self):
        if self.occupied:
            return self.piece.get_sign()
        else:
            # return self.letter + self.number
            return "  "

    def get_occupied(self):
        return self.occupied

    def get_piece(self):
        if self.occupied == False:
            return None
        elif self.occupied == True:
            return self.piece

    def set_square_with_piece(self, piece):
        self.piece = piece
        self.occupied = True

    def set_square_free(self):
        self.piece = None
        self.occupied = False


class Player:
    newid = itertools.count()

    def __init__(self, name, color) -> None:
        self.id = next(Player.newid)
        self.name = name
        self.color = color

    def __repr__(self) -> str:
        return str(self.id) + " " + self.name + " " + self.color

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_color(self):
        return self.color

    def choose_a_piece_to_move(self):
        return choose_field("Choose a piece to move:\n")

    def choose_a_destination(self):
        return choose_field("Where do you want to move?\n")


def main():
    again = False
    while not again:
        chess_game = Game()
        chess_game.run()
        # again = chess_game.ask_if_again()
    print("Thank you for playing!")


if __name__ == '__main__':
    main()
