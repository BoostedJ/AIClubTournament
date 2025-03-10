import random
import tkinter as tk

# Board settings
BOARD_SIZE = 10
SHIP_SIZES = [5, 4, 3, 3, 2]  # Standard Battleship ship sizes


class BattleshipGame:

    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.boards = [self.init_board(), self.init_board()]
        self.shots_taken = [set(), set()]
        self.turn = 0

        # Ask players to place ships
        for i, player in enumerate(self.players):
            self.boards[i] = player.place_ships(self.boards[i], SHIP_SIZES)

    def init_board(self):
        return [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def is_valid_shot(self, shot, player_idx):
        return 0 <= shot[0] < BOARD_SIZE and 0 <= shot[
            1] < BOARD_SIZE and shot not in self.shots_taken[player_idx]

    def take_turn(self):
        player_idx = self.turn % 2
        opponent_idx = 1 - player_idx
        shot = self.players[player_idx].choose_target()

        while not self.is_valid_shot(shot, player_idx):
            shot = self.players[player_idx].choose_target()

        self.shots_taken[player_idx].add(shot)
        hit = self.boards[opponent_idx][shot[0]][shot[1]] == 'S'
        self.boards[opponent_idx][shot[0]][shot[1]] = 'X' if hit else 'O'
        self.players[player_idx].record_shot(shot, hit)

        # Check if the game is over immediately after a successful hit
        if self.is_game_over():
            return

        self.turn += 1
        return hit

    def is_game_over(self):
        return not any('S' in row for row in self.boards[0]) or not any(
            'S' in row for row in self.boards[1])

    def play_full_game(self):
        while not self.is_game_over():
            self.take_turn()


class BattleshipGUI:

    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.main_frame = tk.Frame(root)
        self.main_frame.grid(row=0, column=0)

        self.board_frames = [
            self.create_board_frame(game.players[0].name, 0),
            self.create_board_frame(game.players[1].name, 1)
        ]

        self.status_label = tk.Label(root,
                                     text="Game in Progress",
                                     font=("Arial", 14))
        self.status_label.grid(row=1, column=0, columnspan=2)
        self.next_move_button = tk.Button(root,
                                          text="Next Move",
                                          command=self.next_move)
        self.next_move_button.grid(row=2, column=0, columnspan=2)
        self.next_two_moves_button = tk.Button(root,
                                               text="Next 2 Moves",
                                               command=self.next_two_moves)
        self.next_two_moves_button.grid(row=3, column=0, columnspan=2)
        self.skip_to_end_button = tk.Button(root,
                                            text="Skip to End",
                                            command=self.skip_to_end)
        self.skip_to_end_button.grid(row=4, column=0, columnspan=2)

        self.update_boards()

    def create_board_frame(self, player_name, col):
        frame = tk.Frame(self.main_frame)
        frame.grid(row=0, column=col, padx=10)
        label = tk.Label(frame, text=player_name, font=("Arial", 12, "bold"))
        label.grid(row=0, column=0, columnspan=BOARD_SIZE)
        return frame

    def update_boards(self):
        for player_idx in range(2):
            for widget in self.board_frames[player_idx].winfo_children():
                if isinstance(widget, tk.Label) and widget.cget(
                        "text") != self.game.players[player_idx].name:
                    widget.destroy()
            for r in range(BOARD_SIZE):
                for c in range(BOARD_SIZE):
                    cell = self.game.boards[player_idx][r][c]
                    color = "white" if cell == '.' else "red" if cell == 'X' else "blue" if cell == 'S' else "gray"
                    label = tk.Label(self.board_frames[player_idx],
                                     text=cell,
                                     width=2,
                                     height=1,
                                     bg=color,
                                     font=("Arial", 12))
                    label.grid(
                        row=r + 1,
                        column=c)  # Offset row by 1 to leave space for name

    def next_move(self):
        if not self.game.is_game_over():
            self.game.take_turn()
            self.update_boards()
        if self.game.is_game_over():
            self.status_label.config(
                text=
                f"Game Over! {self.game.players[self.game.turn % 2].name} Wins"
            )
            self.disable_buttons()

    def next_two_moves(self):
        for _ in range(2):
            if self.game.is_game_over():
                break
            self.game.take_turn()
            self.update_boards()
        if self.game.is_game_over():
            self.status_label.config(
                text=
                f"Game Over! {self.game.players[self.game.turn % 2].name} Wins"
            )
            self.disable_buttons()

    def skip_to_end(self):
        self.game.play_full_game()
        self.update_boards()
        self.status_label.config(
            text=f"Game Over! {self.game.players[self.game.turn % 2].name} Wins"
        )
        self.disable_buttons()

    def disable_buttons(self):
        self.next_move_button.config(state=tk.DISABLED)
        self.next_two_moves_button.config(state=tk.DISABLED)
        self.skip_to_end_button.config(state=tk.DISABLED)


class DefaultBattleshipAI:

    def __init__(self, name):
        self.name = name
        self.shots_history = []  # Stores (x, y, hit) for each shot taken

    def place_ships(self, board, ship_sizes):
        return self.default_place_ships(board, ship_sizes)

    def choose_target(self):
        return self.default_choose_target()

    def default_choose_target(self):
        """Always selects the top-left most open space."""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if not any(shot[0] == row and shot[1] == col for shot in
                           self.shots_history):  # Find the first unshot cell
                    return (row, col)

    def default_place_ships(self, board, ship_sizes):
        """Random ship placement"""
        for size in ship_sizes:
            placed = False
            while not placed:
                row, col = random.randint(0, BOARD_SIZE - 1), random.randint(
                    0, BOARD_SIZE - 1)
                direction = random.choice([(1, 0),
                                           (0, 1)])  # Vertical or Horizontal

                # Check if ship fits
                if all(0 <= row + direction[0] * i < BOARD_SIZE and 0 <= col +
                       direction[1] * i < BOARD_SIZE and board[
                           row + direction[0] * i][col +
                                                   direction[1] * i] == '.'
                       for i in range(size)):
                    for i in range(size):
                        board[row + direction[0] * i][col +
                                                      direction[1] * i] = 'S'
                    placed = True
        return board

    def record_shot(self, shot, hit):
        """Records the shot and whether it was a hit or miss."""
        self.shots_history.append((shot[0], shot[1], hit))


class MyBattleship:
    """ Rename this class to your name. This will make it easier to run two submissions against each other.
        Ex: Renaming MyBattleshipAI to LoganWolff
    """

    def __init__(self, name):
        self.name = name
        self.shots_history = []  # Stores (x, y, hit) for each shot taken
        self.hit_locations = []
        self.hunt_mode = True    
        self.current_direction = None  
        self.last_hit = None     

    def place_ships(self, board, ship_sizes):
        """Include your code here and remove the default return call"""
        for size in ship_sizes:
            placed = False
            while not placed:
                try: 
                    row, col = random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)
                    direction = random.choice([(1, 0), (0, 1)])
                    if all(0 <= row + direction[0] * i < BOARD_SIZE and
                           0 <= col + direction[1] * i < BOARD_SIZE and
                           board[row + direction[0] * i][col + direction[1] * i] == '.' and
                           board[row + direction[0] * i + 1][col + direction[1] * i] != 'S' and
                           board[row + direction[0] * i][col + direction[1] * i + 1] != 'S' and 
                           board[row + direction[0] * i - 1][col + direction[1] * i] != 'S' and
                           board[row + direction[0] * i][col + direction[1] * i -1] != 'S' for i in range(size)):
                        for i in range(size):
                            board[row+direction[0]*i][col+direction[1]*i] = 'S'
                        placed = True
                except:
                    pass
        return board

    def choose_target(self):
        if self.hunt_mode:
            return self.hunt_target()
        else:
            return self.target_ship()

    def hunt_target(self):
        while True:
            row = random.randint(0, BOARD_SIZE - 1)
            col = random.randint(0, BOARD_SIZE - 1)
            
            if not any(shot[0] == row and shot[1] == col for shot in self.shots_history):
                return (row, col)

    def target_ship(self):
        if self.last_hit and self.current_direction:
            row, col = self.last_hit
            dr, dc = self.current_direction
            new_row = row + dr
            new_col = col + dc
            
            if (0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE and 
                not any(shot[0] == new_row and shot[1] == new_col for shot in self.shots_history)):
                return (new_row, new_col)
            
            self.current_direction = (-dr, -dc)
            
            first_hit = self.hit_locations[0]
            new_row = first_hit[0] + self.current_direction[0]
            new_col = first_hit[1] + self.current_direction[1]
            
            if (0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE and 
                not any(shot[0] == new_row and shot[1] == new_col for shot in self.shots_history)):
                return (new_row, new_col)
        
        if self.hit_locations:
            last_hit = self.hit_locations[-1]
            
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
            random.shuffle(directions)  
            
            for dr, dc in directions:
                new_row = last_hit[0] + dr
                new_col = last_hit[1] + dc
                
                if (0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE and 
                    not any(shot[0] == new_row and shot[1] == new_col for shot in self.shots_history)):
                    self.current_direction = (dr, dc)
                    return (new_row, new_col)
        
        self.hunt_mode = True
        return self.hunt_target()

    def is_ship_sunk(self):
        if not self.hit_locations:
            return True
            
        for hit_row, hit_col in self.hit_locations:
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_row, new_col = hit_row + dr, hit_col + dc
                
                if (0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE and 
                    not any(shot[0] == new_row and shot[1] == new_col for shot in self.shots_history)):
                    return False
        
        return True

    def default_choose_target(self):
        """Always selects the top-left most open space."""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if not any(shot[0] == row and shot[1] == col for shot in
                           self.shots_history):  # Find the first unshot cell
                    return (row, col)

    def default_place_ships(self, board, ship_sizes):
        """Random ship placement"""
        for size in ship_sizes:
            placed = False
            while not placed:
                row, col = random.randint(0, BOARD_SIZE - 1), random.randint(
                    0, BOARD_SIZE - 1)
                direction = random.choice([(1, 0),
                                           (0, 1)])  # Vertical or Horizontal

                # Check if ship fits
                if all(0 <= row + direction[0] * i < BOARD_SIZE and 0 <= col +
                       direction[1] * i < BOARD_SIZE and board[
                           row + direction[0] * i][col +
                                                   direction[1] * i] == '.'
                       for i in range(size)):
                    for i in range(size):
                        board[row + direction[0] * i][col +
                                                      direction[1] * i] = 'S'
                    placed = True
        return board

    def record_shot(self, shot, hit):
        """Records the shot and whether it was a hit or miss."""
        self.shots_history.append((shot[0], shot[1], hit))
        
        if hit:
            self.hunt_mode = False
            self.hit_locations.append(shot)
            self.last_hit = shot
            
        else:
            if not self.hunt_mode:
                if self.is_ship_sunk():
                    self.hunt_mode = True
                    self.hit_locations = []
                    self.last_hit = None
                    self.current_direction = None


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Battleship Game")
    player1 = MyBattleship("Player")
    player2 = DefaultBattleshipAI("Default AI")
    game = BattleshipGame(player1, player2)
    gui = BattleshipGUI(root, game)
    root.mainloop()
