import pygame
import heapq


def for_validmove(board, x, y):
    return all([
    0 <= x < len(board), 
    0 <= y < len(board[0]), 
    board[x][y] != '#'
    ])



def movetheplayer(board, player_x, player_y, dx, dy):
    
    new_board = [row[:] for row in board]
    new_x, new_y = player_x + dx, player_y + dy

    
    if for_validmove(new_board, new_x, new_y):
        cell = new_board[new_x][new_y]

        # If box push it
        if cell == 'B':  # 
            box_new_x, box_new_y = new_x + dx, new_y + dy  # Calculate box position

            # Check box can be pushed or not
            if for_validmove(new_board, box_new_x, box_new_y) and new_board[box_new_x][box_new_y] in ['.', 'G']:
                # Push to new position
                new_board[box_new_x][box_new_y] = 'B'
                # Update player position and goal state
                new_board[new_x][new_y] = 'P' if new_board[new_x][new_y] == '.' else 'G'
                new_board[player_x][player_y] = '.'
                return new_board, new_x, new_y
            else:
                return None, player_x, player_y 
        else:
            # Move the player without box
            new_board[new_x][new_y] = 'P'
            # Update the previous position
            new_board[player_x][player_y] = '.' if new_board[player_x][player_y] == 'P' else 'G'
            return new_board, new_x, new_y
        
    return None, player_x, player_y 



def get_box_positions(board):
    boxes = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'B':
                boxes.append((i, j))
    return boxes




def heuristic(board, goal_positions):
    box_positions = get_box_positions(board)
    distance = 0
    for box in box_positions:
        min_distance = min(abs(box[0] - goal[0]) + abs(box[1] - goal[1]) for goal in goal_positions)
        distance += min_distance
    return distance





def a_star_search(start_board, goal_positions, player_x, player_y):
    open_set = []
    heapq.heappush(open_set, (0, start_board, player_x, player_y, 0, [])) 
    closed_set = set()

    while open_set:
        _, current_board, player_x, player_y, g_score, path = heapq.heappop(open_set)
        board_tuple = tuple(map(tuple, current_board))

        if board_tuple in closed_set:
            continue

        closed_set.add(board_tuple)

        # Checking boxes in goal or not
        if all(current_board[goal[0]][goal[1]] == 'B' for goal in goal_positions):
            return path  # Return path

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_board, new_player_x, new_player_y = movetheplayer(current_board, player_x, player_y, dx, dy)
            if new_board:
                h_score = heuristic(new_board, goal_positions)
                f_score = g_score + 1 + h_score
                new_path = path + [(new_player_x, new_player_y)]
                heapq.heappush(open_set, (f_score, new_board, new_player_x, new_player_y, g_score + 1, new_path))

    return None  # Nosolution









def draw_cell(screen, cell, x, y, cell_size):
    color_mapping = {
        '#': (128, 128, 128),  # Wall
        'B': (255, 0, 0),      # Box
        'P': (0, 0, 255),      # Player
        '.': (200, 200, 200),  # Emptyspace
        'G': (0, 255, 0)       # Goal
    }

    # Get the color based on the cell value
    color = color_mapping.get(cell)

    # If cell draw it
    if color:
        pygame.draw.rect(screen, color, (x + 1, y + 1, cell_size - 2, cell_size - 2))




def draw_board(screen, board, top_left, cell_size=50):
    margin = 10
    x_offset, y_offset = top_left

    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            x = j * cell_size + margin + x_offset
            y = i * cell_size + margin + y_offset

            # Draw cell
            pygame.draw.rect(screen, (255, 255, 255), (x, y, cell_size, cell_size), 1)
            draw_cell(screen, cell, x, y, cell_size)













def animate_solution(screen, board, path, original_board, top_left, cell_size=50, delay=500, auto_solve=False):
    player_x, player_y = next((i, j) for i in range(len(board)) for j in range(len(board[0])) if board[i][j] == 'P')

    step_positions = []
    step_index = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:  # Move to nextstep
                    if step_index < len(path):
                        new_x, new_y = path[step_index]
                        dx, dy = new_x - player_x, new_y - player_y
                        board, player_x, player_y = movetheplayer(board, player_x, player_y, dx, dy)
                        step_positions.append(f"Step {step_index + 1}: ({new_x}, {new_y})")
                        step_index += 1
                elif event.key == pygame.K_LEFT:  # Move to previous
                    if step_index > 0:
                        step_index -= 1
                        new_x, new_y = path[step_index]
                        dx, dy = new_x - player_x, new_y - player_y
                        board, player_x, player_y = movetheplayer(board, player_x, player_y, dx, dy)
                        step_positions = step_positions[:step_index] 




            # mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # if next clicked
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    if step_index < len(path):
                        new_x, new_y = path[step_index]
                        dx, dy = new_x - player_x, new_y - player_y
                        board, player_x, player_y = movetheplayer(board, player_x, player_y, dx, dy)
                        step_positions.append(f"Step {step_index + 1}: ({new_x}, {new_y})")
                        step_index += 1

                # if previous clicked
                elif button_x + button_width + button_spacing <= mouse_x <= button_x + 2 * button_width + button_spacing and button_y <= mouse_y <= button_y + button_height:
                    if step_index > 0:
                        step_index -= 1
                        new_x, new_y = path[step_index]
                        dx, dy = new_x - player_x, new_y - player_y
                        board, player_x, player_y = movetheplayer(board, player_x, player_y, dx, dy)
                        step_positions = step_positions[:step_index]  # Remove steps after the previous one

                # if solve clicked
                elif button_x + 2 * (button_width + button_spacing) <= mouse_x <= button_x + 3 * button_width + 2 * button_spacing and button_y <= mouse_y <= button_y + button_height:
                    auto_solve = True

                #if close clicked
                elif button_x + 3 * (button_width + button_spacing) <= mouse_x <= button_x + 4 * button_width + 3 * button_spacing and button_y <= mouse_y <= button_y + button_height:
                    pygame.quit() 
                    exit() 

            # if solve clicked solve it
            if auto_solve and step_index < len(path):
                new_x, new_y = path[step_index]
                dx, dy = new_x - player_x, new_y - player_y
                board, player_x, player_y = movetheplayer(board, player_x, player_y, dx, dy)
                step_positions.append(f"Step {step_index + 1}: ({new_x}, {new_y})")
                step_index += 1
                if step_index == len(path):  # end running if completed
                    running = False

        screen.fill((0, 0, 0))  # Clear screen

        # diaplay original board
        draw_board(screen, original_board, top_left=(75, 50), cell_size=cell_size)

        # Display animated one right
        draw_board(screen, board, top_left=(750, 50), cell_size=cell_size)
        
        
        font = pygame.font.Font(None, 26)
        for i, step_text in enumerate(step_positions):
            rendered_text = font.render(step_text, True, (255, 255, 255))
            screen.blit(rendered_text, (550, 50 + i * 40))  # Position the step text with consistent spacing


        # Button positions and sizes
        button_width = 100
        button_height = 40
        button_spacing = 100
        button_x = 250
        button_y = 575

        button_colors = {
            "next": (0, 128, 0),  # Green
            "previous": (128, 0, 0),  # Red
            "solve": (0, 0, 255),  # Blue
            "close": (255, 0, 0)  # Red
            }
        text_color = (255, 255, 255)  # White for text
        button_labels = ["Next", "Previous", "Solve", "Close"]
        button_positions = [
            (button_x, button_y),  # Next button
            (button_x + button_width + button_spacing, button_y),  # Previous button
            (button_x + 2 * (button_width + button_spacing), button_y),  # Solve button
            (button_x + 3 * (button_width + button_spacing), button_y)  # Close button
            ]

         # Draw buttons and labels
        for i, label in enumerate(button_labels):
            button_x_pos, button_y_pos = button_positions[i]
            button_color = button_colors[label.lower()]
            # Draw the button
            pygame.draw.rect(screen, button_color, (button_x_pos, button_y_pos, button_width, button_height))
    
         # Render and center the text
            button_text = font.render(label, True, text_color)
            text_rect = button_text.get_rect(center=(button_x_pos + button_width // 2, button_y_pos + button_height // 2))
    
         # Display the text on the button
            screen.blit(button_text, text_rect)


        pygame.display.flip()
        pygame.time.delay(delay)







def main():
    pygame.init()

    screen_width = 1200
    screen_height = 650
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("AI POWERED SOKOBAN GAME SOLVER")

    # Initial board state
    board = [
        ['#', '#', '#', '#', '#', '#', '#'],
        ['#', '.', '.', 'G', '#', '.', '#'],
        ['#', '.', 'B', '.', '#', '.', '#'],
        ['#', '.', '.', 'P', '.', '.', '#'],
        ['#', '.', '.', 'B', '#', '#', '#'],
        ['#', '.', '.', '.', '#', 'G', '#'],
        ['#', '#', '#', '#', '#', '#', '#']
    ]

    goal_positions = [(1, 3), (5, 5)] 

    # Finding starting points of pplayer
    player_x, player_y = next((i, j) for i in range(len(board)) for j in range(len(board[0])) if board[i][j] == 'P')

    # Run A* to find the solution
    solution_path = a_star_search(board, goal_positions, player_x, player_y)
    if not solution_path:
        print("No solution found.")
        return

    running = True
    auto_solve = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))  # Clear screen

        # Animate solution on the right
        animate_solution(screen, [row[:] for row in board], solution_path, board, top_left=(650, 50), cell_size=50, auto_solve=auto_solve)

    pygame.quit()



if __name__ == "__main__":
    main()
