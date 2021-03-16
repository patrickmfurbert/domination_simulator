# Author: Patrick Furbert
# Date: November 25, 2020

# Required Moduels

# Class Definitions
class Pawn:
    """
    Represents player pawn for game
    Focus/Domination
    """

    def __init__(self, color):
        """
        Creates instance of Pawn with
        color, top, and bottom assignments
        """
        self._color = color
        self._top = True
        self._bottom = True

    def set_top(self, pawn):
        """
        Set new pawn as the top in a stack
        """
        self._top = pawn

    def set_bottom(self, pawn):
        """
        Set new pawn as the bottom in a stack
        """
        self._bottom = pawn

    def get_top(self):
        """
        Returns the top of the stack
        """
        return self._top

    def get_bottom(self):
        """
        Returns the bottom of the stack
        """
        return self._bottom

    def get_color(self):
        """
        Return the color of the pawn
        """
        return self._color

    def make_bottom(self):
        """
        Make pawn the bottom of the stack
        """
        self._bottom = True

    def make_top(self):
        """
        Make pawn the top of the stack
        """
        self._top = True

    def make_singleton(self):
        """
        Make pawn a singleton by
        unlinking the top and bottom
        from other pawns
        """
        self.make_bottom()
        self.make_top()


class Player:
    """
    Represents Player object that has
    name, color, attribute objects
    """
    def __init__(self, name, color):
        """
        Returns a player object
        """
        self._name = name
        self._color = color
        self._reserve = []
        self._num_captured = 0

    def get_name(self):
        """
        returns the name of the player
        """
        return self._name

    def get_color(self):
        """
        returns sthe color of the player
        """
        return self._color

    def captured_piece(self):
        """
        Increase the number of captured
        pieces by one
        """
        self._num_captured += 1

    def how_many_captured(self):
        """
        Returns the number of captured pieces
        """
        return self._num_captured

    def add_to_reserve(self, pawn):
        """
        adds a pawn to the players
        reserve pieces list
        """
        self._reserve.append(pawn)

    def remove_from_reserve(self):
        """
        takes a pawn from the reserve
        """
        if len(self._reserve) > 0:
            return self._reserve.pop(0)
        else:
            return False

    def get_reserve(self):
        """
        returns the reserve list
        for the specified player
        """
        return self._reserve


class FocusGame:
    """
    Represents Two player version of the
    game Focus/Domination
    """

    def __init__(self, p1, p2):
        # player info assignment as tuple
        # ex: ("PlayerA", "R") or ("PlayerB", "G")
        self._p1 = Player(p1[0], p1[1])
        self._p2 = Player(p2[0], p2[1])
        self._players = [self._p1, self._p2]
        self._whos_turn = None  # any player may start the game
        self._turns_generator = None # initialize turns_generator
        self._game_over = False
        # board initialization
        self._board = [[None for y in range(6)] for x in range(6)]
        for x in range(6):
            for y in range(6):
                if x % 2 == 0:
                    if y < 2:
                        self._board[x][y] = Pawn(p1[1])
                        continue
                    if y < 4:
                        self._board[x][y] = Pawn(p2[1])
                        continue
                    if y < 6:
                        self._board[x][y] = Pawn(p1[1])
                        continue
                else:
                    if y < 2:
                        self._board[x][y] = Pawn(p2[1])
                        continue
                    if y < 4:
                        self._board[x][y] = Pawn(p1[1])
                        continue
                    if y < 6:
                        self._board[x][y] = Pawn(p2[1])
                        continue

    def move_piece(self, player, start_pos, end_pos, num_pawns):
        """
        Function for making moves
        """

        # if starting pos has None return False
        if self.getBoard()[start_pos[0]][start_pos[1]] is None:
            return False

        # validate move coordinates legal(not out of range of board)
        for a in start_pos + end_pos:
            if a < 0 or a > 5:
                return False

        # validate player move request is horizontal or vertical
        if start_pos[0] != end_pos[0] and start_pos[1] != end_pos[1]:
            return False

        # validate move color is legal (top pawn color equal to player color)
        # this should also work in the case that there is no pawn at the square
        pawn = self.getBoard()[start_pos[0]][start_pos[1]]
        while pawn.get_top() is not True:
            pawn = pawn.get_top()
        for p in self.getPlayers():
            if p.get_name() == player:
                if pawn.get_color() != p.get_color():
                    return False

        # validate the appropriate number of pieces are moving
        if self.getPawnsAtCoordinate(start_pos) < num_pawns:
            return False
        if num_pawns > 5:
            return False

        # validate that distance being moved is equal to the number of pawns
        row_difference = abs(start_pos[0] - end_pos[0])
        column_difference = abs(start_pos[1] - end_pos[1])
        if row_difference != num_pawns and column_difference != num_pawns:
            return False

        # handle first move
        if self._whos_turn is None:
            self._turns_generator = self.start_turns(player)
            self.handle_move(player, start_pos, end_pos, num_pawns)
            return "successfully moved"
        # handle subsequent moves
        else:
            self.handle_move(player, start_pos, end_pos, num_pawns)
            if self._game_over is True:
                return "{} Wins".format(player)
            return "successfully moved"

    def handle_move(self, player, start_pos, end_pos, num_pawns):
        """
        Move logic for move_piece function
        """
        # verify it is the correct players turn
        if self.whos_turn_is_it() == player or self.whos_turn_is_it() is None:
            # move
            # get references to stacks/pawns at start and end location
            bottom_pawn_at_start = self.getBoard()[start_pos[0]][start_pos[1]]
            bottom_pawn_at_end = self.getBoard()[end_pos[0]][end_pos[1]]

            # determine if you are moving entire stack or partial stack
            # in the case that it is 1 pawn, this is also an entire stack
            entire_stack = num_pawns == self.getPawnsAtCoordinate(start_pos) # this value is a boolean

            # move stack pawn
            if entire_stack:
                # set starting board position to None
                self.getBoard()[start_pos[0]][start_pos[1]] = None
                # is there pawn at the end position or nothing
                if bottom_pawn_at_end is None:
                    self.getBoard()[end_pos[0]][end_pos[1]] = bottom_pawn_at_start
                else:
                    # get the pawn being captured
                    captured = self.getPawnAtTop(end_pos)

                    # change the top of the captured pawn
                    captured.set_top(bottom_pawn_at_start)

                    # reassign the bottom of the stac
                    bottom_pawn_at_start.set_bottom(captured)

            else:  # we are not moving the entire stack
                # we must get reference to the pawn that will
                # become the bottom of the stack we are moving
                bottom_of_partial_stack = self.getPartialStackPawn(self.getPawnAtTop(start_pos), num_pawns)

                # if space to be moving is empty just placce it
                if self.getBoard()[end_pos[0]][end_pos[1]] is None:
                    self.getBoard()[end_pos[0]][end_pos[1]] = bottom_of_partial_stack
                    # reassign the top pawn remaining at the start position to top
                    bottom_of_partial_stack.get_bottom().make_top()
                    bottom_of_partial_stack.make_bottom()

                else:
                    # move partial stack onto captured
                    captured = self.getPawnAtTop(end_pos)
                    captured.set_top(bottom_of_partial_stack)

                    # reassign the top pawn remaining at the start position to top
                    bottom_of_partial_stack.get_bottom().make_top()

                    # reassign the bottom of the partial stack pawn
                    bottom_of_partial_stack.set_bottom(captured)

            # deal with any extra pieces and assign them accordingly
            if self.getPawnsAtCoordinate(end_pos) > 5:

                # get the bottom of the leftovers
                left_overs_bottom = self.getBoard()[end_pos[0]][end_pos[1]]

                # get bottom of the 5 stack we will leave
                bottom_of_five_stack = self.getPartialStackPawn(self.getPawnAtTop(end_pos), 5)

                # make the pawn beneath the bottom a top
                bottom_of_five_stack.get_bottom().make_top()

                # make the bottom of the five stack a bottom
                bottom_of_five_stack.make_bottom()

                # set new 5 stack on the board
                self.getBoard()[end_pos[0]][end_pos[1]] = bottom_of_five_stack

                # get player color and current player
                color = "unknown"
                current_player = None
                for p in self.getPlayers():
                    if p.get_name() == player:
                        color = p.get_color()
                        current_player = p

                # cycle through left overs and assign reserve and capture accordingly
                next_pawn = None

                while True:

                    # capture the next reference
                    next_pawn = left_overs_bottom.get_top()

                    # make current pawn a singleton(both top and bottom)
                    left_overs_bottom.make_singleton()

                    # check color and assign to reserve or capture
                    if left_overs_bottom.get_color() == color:
                        current_player.add_to_reserve(left_overs_bottom)
                    else:
                        current_player.captured_piece()

                    # reassign the reference of left_overs_bottom
                    left_overs_bottom = next_pawn

                    if left_overs_bottom is True:
                        
                        break

            # check if there was a win
            if self.checkForWin(player) is True:
                self._game_over = True

            # change turn at the end of the move
            self.changeTurn()


    def printScore(self):
        """
        Prints the current score
        """
        for p in self.getPlayers():
            reserve = []
            for piece in p.get_reserve():
                reserve.append(piece.get_color())
            print("{} | Captures: {} | Reserve: {}".format(p.get_name(), p.how_many_captured(), reserve))

    def checkForWin(self, player):
        """
        Function that checks for win
        (ie did a player capture 6 pieces)
        """
        for p in self.getPlayers():
            if p.get_name() == player:
                if p.how_many_captured() >= 6:
                    return True

    def show_pieces(self, position):
        """
        Function returning the list showing
        the pieces that are present in that location
        starting with the bottom piece in the 0th index
        """
        pieces = []
        pawn = self._board[position[0]][position[1]]
        if pawn is not None:
            pieces.append(pawn.get_color())
            while pawn.get_top() is not True:
                pawn = pawn.get_top()
                pieces.append(pawn.get_color())
            return pieces
        else:
            return False

    def show_reserve(self, player):
        """
         function to show the reserve for any
        """
        for p in self.getPlayers():
            if p.get_name() == player:
                return len(p.get_reserve())

    def show_captured(self, player):
        """
        returns the number of pieces capture by the player
        """
        for p in self.getPlayers():
            if p.get_name() == player:
                return p.how_many_captured()

    def reserved_move(self, player, location):
        """
        places the piece from the reserve to the location
        and reduced the reserved pieces, if none
        return 'no pieces in reserve'
        """

        # Check that is is the appropriate turn
        if self.whos_turn_is_it() == player:
            for p in self.getPlayers():

                if p.get_name() == player:

                    # check that location is None
                    if self.getBoard()[location[0]][location[1]] is not None:
                        return False

                    # check that reserve has a piece
                    if len(p.get_reserve()) == 0:
                        return False

                    # else place a piece
                    self.getBoard()[location[0]][location[1]] = p.get_reserve().pop()
                    self.getBoard()[location[0]][location[1]].make_singleton()
                    self.changeTurn()

    def changeTurn(self):
        """
        Changes the player turn
        """
        self._whos_turn = next(self._turns_generator)
        return self._whos_turn

    def whos_turn_is_it(self):
        """
        Returns the turn of the current player
        """
        return self._whos_turn

    def start_turns(self, player):
        """
        initializes generator for turns
        """
        turn = player
        while True:
            for p in [p for p in self.getPlayers() if p.get_name() != turn]:
                turn = p.get_name()
            yield turn

    def getPlayers(self):
        """
        Gets a list of the two current players
        """
        return self._players

    def getBoard(self):
        """
        Get the board
        """
        return self._board

    def getPawnsAtCoordinate(self, coordinate):
        """
        Takes coordinates as a tuple
        and returns the number of pawns
        in the stack
        """
        count = 0
        if self.getBoard()[coordinate[0]][coordinate[1]] is None:
            return count
        else:
            count += 1
            pawn = self.getBoard()[coordinate[0]][coordinate[1]]
            while pawn.get_top() is not True:
                pawn = pawn.get_top()
                count += 1
            return count

    def getPawnAtTop(self, coordinate):
        """
        Returns the pawn at the stop of a stack
        """

        pawn = self.getBoard()[coordinate[0]][coordinate[1]]
        while pawn.get_top() is not True:
            pawn = pawn.get_top()
        return pawn

    def getPartialStackPawn(self, top_pawn, num_pawns):
        """
        Get reference to the pawn that
        defines the partial stack
        """
        pawn = top_pawn
        for x in range(1, num_pawns):
            pawn = pawn.get_bottom()
        return pawn

    def print_board(self):
        """
        Prints the board
        """
        for x in range(6):
            for y in range(6):
                # check if we are looking at the top
                pawn = self._board[x][y]
                if pawn is None:
                    print("X", end=" ")
                else:
                    while pawn.get_top() is not True:
                        pawn = pawn.get_top()
                    print(pawn.get_color(), end=" ")
            print("")


def main():

    #Example game run
    game = FocusGame(("p1", "R"), ("p2", "G"))
    game.print_board()
    game.move_piece("p2", (1, 1), (1, 2), 1)
    print(game.show_pieces((1, 2)))
    print(game.show_pieces((1, 3)))
    print(game.whos_turn_is_it())
    game.print_board()
    game.printScore()
    game.move_piece("p1", (0, 0), (0, 1), 1)
    print(game.show_pieces((0, 0)))
    print(game.show_pieces((0, 1)))
    print(game.whos_turn_is_it())
    game.print_board()
    game.printScore()
    game.move_piece("p2", (0, 2), (0, 1), 1)
    print(game.show_pieces((0, 2)))
    print(game.show_pieces((0, 1)))
    print(game.whos_turn_is_it())
    game.print_board()
    game.printScore()
    game.move_piece("p1", (2, 0), (1, 0), 1)
    print(game.show_pieces((2, 0)))
    print(game.show_pieces((1, 0)))
    print(game.whos_turn_is_it())
    game.print_board()
    game.printScore()
    game.move_piece("p2", (0, 1), (0, 4), 3)
    print(game.show_pieces((0, 1)))
    print(game.show_pieces((0, 4)))
    print(game.whos_turn_is_it())
    game.print_board()
    game.printScore()
    game.move_piece("p1", (1, 0), (1, 2), 2)
    print(game.show_pieces((1, 0)))
    print(game.show_pieces((1, 2)))
    print(game.whos_turn_is_it())
    game.print_board()
    game.printScore()
    game.move_piece("p2", (0, 4), (4, 4), 4)
    print(game.show_pieces((0, 4)))
    print(game.show_pieces((4, 4)))
    print(game.whos_turn_is_it())
    game.print_board()
    game.printScore()
    game.move_piece("p1", (4, 5), (4, 4), 1)
    print(game.show_pieces((4, 5)))
    print(game.show_pieces((4, 4)))
    print(game.whos_turn_is_it())
    game.print_board()
    game.printScore()
    game.move_piece("p2", (1, 5), (1, 4), 1)
    print(game.show_pieces((2, 5)))
    print(game.show_pieces((2, 4)))
    print(game.whos_turn_is_it())
    game.print_board()
    game.printScore()
    game.reserved_move("p1", (1,1))
    print(game.whos_turn_is_it())
    game.print_board()
    game.move_piece("p2", (3, 4), (4, 4), 1)
    print(game.show_pieces((3, 4)))
    print(game.show_pieces((4, 4)))
    print(game.whos_turn_is_it())
    game.print_board()
    game.printScore()
    game.move_piece("p1", (1, 3), (1, 2), 1)
    print(game.show_pieces((1, 3)))
    print(game.show_pieces((1, 2)))
    print(game.whos_turn_is_it())
    game.print_board()
    game.printScore()
    game.move_piece("p2", (2, 2), (1, 2), 1)
    print(game.show_pieces((2, 2)))
    print(game.show_pieces((1, 2)))
    print(game.whos_turn_is_it())
    game.print_board()
    game.printScore()
    game.move_piece("p1", (1, 1), (1, 2), 1)
    print(game.show_pieces((1, 1)))
    print(game.show_pieces((1, 2)))
    print(game.whos_turn_is_it())
    game.print_board()
    game.printScore()
    game.move_piece("p2", (3, 1), (3, 2), 1)
    print(game.show_pieces((3, 1)))
    print(game.show_pieces((3, 2)))
    print(game.whos_turn_is_it())
    game.print_board()
    game.printScore()
    game.move_piece("p1", (2, 1), (1, 1), 1)
    print(game.show_pieces((2, 1)))
    print(game.show_pieces((1, 1)))
    print(game.whos_turn_is_it())
    game.print_board()
    game.printScore()
    game.move_piece("p2", (3, 2), (1, 2), 2)
    print(game.show_pieces((3, 2)))
    print(game.show_pieces((1, 2)))
    print(game.whos_turn_is_it())
    game.print_board()
    game.printScore()
    game.move_piece("p1", (4, 0), (3, 0), 1)
    print(game.show_pieces((4, 0)))
    print(game.show_pieces((3, 0)))
    print(game.whos_turn_is_it())
    game.print_board()
    game.printScore()
    print(game.show_pieces((1, 4)))
    game.move_piece("p2", (1, 4), (1, 3), 1)
    print(game.show_pieces((1, 4)))
    print(game.show_pieces((1, 3)))
    print(game.whos_turn_is_it())
    game.print_board()
    game.printScore()
    game.move_piece("p1", (2, 4), (2, 3), 1)
    print(game.show_pieces((2, 4)))
    print(game.show_pieces((2, 3)))
    print(game.whos_turn_is_it())
    game.print_board()
    game.printScore()
    game.move_piece("p2", (1, 3), (1, 2), 1)
    print(game.show_pieces((1, 3)))
    print(game.show_pieces((1, 2)))
    print(game.whos_turn_is_it())
    game.print_board()
    game.printScore()
    game.move_piece("p1", (1, 1), (1, 2), 1)
    print(game.show_pieces((1, 1)))
    print(game.show_pieces((1, 2)))
    print(game.whos_turn_is_it())
    game.print_board()
    game.printScore()
    game.reserved_move("p2", (1, 5))
    game.print_board()
    game.printScore()
    game.move_piece("p1", (5, 2), (5, 1), 1)
    print(game.show_pieces((5, 2)))
    print(game.show_pieces((5, 1)))
    print(game.whos_turn_is_it())
    game.print_board()
    game.printScore()
    game.move_piece("p2", (1, 5), (1, 4), 1)
    print(game.show_pieces((1, 4)))
    print(game.show_pieces((1, 5)))
    print(game.whos_turn_is_it())
    game.print_board()
    game.printScore()
    game.move_piece("p1", (5, 3), (5, 4), 1)
    print(game.show_pieces((5, 3)))
    print(game.show_pieces((5, 4)))
    print(game.whos_turn_is_it())
    game.print_board()
    game.printScore()
    print(game.move_piece("p2", (1, 4), (1, 2), 2))
    print(game.show_pieces((1, 4)))
    print(game.show_pieces((1, 2)))
    print(game.whos_turn_is_it())
    game.print_board()
    game.printScore()

if __name__ == "__main__":
    main()
