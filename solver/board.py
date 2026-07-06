def print_board(board):
    for i in range(len(board)):
        # Horizontal grid lines
        if i % 3 == 0 and i != 0:
            print("------+------+------")

        for j in range(len(board[i])):
                # Vertical grid lines
                if j % 3 == 0 and j != 0:
                    print("|", end=" ")

                print(board[i][j], end=" ")
            
        print()