'''

def mouse_clicks(sq_selected, player_clicks, game_state, valid_moves, move_made):
    location = p.mouse.get_pos() # returns (x,y) position of the mouse into a list
    # for side panel make sure to keep track of the mouse location being relative to the new boundaries

    # column and row number
    col = location[0]//SQUARE_SIZE
    row = location[1]//SQUARE_SIZE
    if sq_selected == (row,col): # if the user clicked same square twice
        sq_selected = () # deselect
        player_clicks = [] # clear player clicks
    else:
        sq_selected = (row, col)
        player_clicks.append(sq_selected) # add both first and second clicks

    if len(player_clicks) == 2: # if its the player's 2nd click, we need to move the piece
        move = ChessEngine.Move(player_clicks[0], player_clicks[1], game_state.board)
        print(move.get_chess_notation())
        for i in range(len(valid_moves)): # iterating through the valid moves to see if player's move is in it
            if move == valid_moves[i]:
                game_state.make_move(valid_moves[i])
                move_made = True
                sq_selected = ()  # reset user clicks
                player_clicks = []
        if not move_made:
            player_clicks = [sq_selected]
'''