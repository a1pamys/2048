import pygame
import random
import time

pygame.init()

# initial set up
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 24)
file = open('high_score', 'r')
init_high = int(file.readline())
file.close()
high_score = init_high

# 2048 game color library
colors = {
    0: '#CCC0B3',
    2: '#EEE4DA',
    4: '#EDE0C8',
    8: '#F2B179',
    16: '#F59563',
    32: '#F67C5F',
    64: '#F65E3B',
    128: '#EDCF72',
    256: '#EDCC61',
    512: '#EDC850',
    1024: '#EDC53F',
    2048: '#EDC22E',
    'light text': '#F9F6F2',
    'dark text': '#776E65',
    'other': '#000000',
    'bg': '#BBAE9F'
}

# game variables initialize
board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over, spawn_new = False, True
bot, calculating = False, False
init_count, score, moves = 0, 0, 62
direction = ''
d_up, d_down, d_left, d_right = 'UP', 'DOWN', 'LEFT', 'RIGHT'

possible_bot_directions = [d_up, d_left, d_right, d_down]

file = open('high_score', 'r')
high_score = int(file.readline())
file.close()

# draw game over and restart text
def draw_over():
    pygame.draw.rect(screen, 'black', [50, 50, 300, 100], 0, 10)
    game_over_text1 = font.render('Game Over!', True, 'white')
    game_over_text2 = font.render('Press Enter to Restart', True, 'white')
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))


# take your turn based on direction
def take_turn(dir, board):
    global score
    merged = [[False for _ in range(4)] for _ in range(4)]
    if direction == d_up:
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0

                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] \
                            and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] *= 2
                        if not calculating:
                            score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True

    elif direction == d_down:
        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j] \
                            and not merged[2 - i + shift][j]:
                        board[3 - i + shift][j] *= 2
                        if not calculating:
                            score += board[3 - i + shift][j]
                        board[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True

    elif direction == d_left:
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] \
                        and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    if not calculating:
                        score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

    elif direction == d_right:
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][3 - j + shift] = board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + shift <= 3:
                    if board[i][4 - j + shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift] \
                            and not merged[i][3 - j + shift]:
                        board[i][4 - j + shift] *= 2
                        if not calculating:
                            score += board[i][4 - j + shift]
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True
    return board

# best move
def get_best_direction(board_values):
    for dir in possible_bot_directions:
        test_board_values = list(map(list, board_values))
        test_board_values = take_turn(dir, test_board_values)
        if test_board_values != possible_bot_directions:
            return dir

    return [d_up, d_left, d_right, d_down][random.randint(0, 3)]

# spawn in new pieces randomly when turns start
def new_pieces(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 1) == 10: # 10% -> 4
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full


# draw background for the board
def draw_board():
    pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)
    moves_text = font.render(f'Moves: {moves}', True, 'black')
    score_text = font.render(f'Score: {score}', True, 'black')
    high_score_text = font.render(f'High Score: {high_score}', True, 'black')
    switch_bot_text = font.render(f'For BOT mode press Space', True, 'blue')
    screen.blit(moves_text, (10, 410))
    screen.blit(score_text, (10, 450))
    screen.blit(high_score_text, (10, 490))
    screen.blit(switch_bot_text, (10, 530))
    pass


# draw tiles for game
def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]

            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']

            pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)

            if value > 0:
                value_len = len(str(value)) # 2048 -> 4 8 -> 1
                font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, 'black', [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)


# main game loop
run = True
while run:
    timer.tick(fps)
    screen.fill('gray')
    draw_board()
    draw_pieces(board_values)

    if spawn_new or init_count < 2:
        board_values, game_over = new_pieces(board_values)
        spawn_new = False
        init_count += 1
        moves -= 1

    if bot and not game_over:
        calculating = True
        old_board_values = list(map(list, board_values))
        direction = get_best_direction(board_values)
        calculating = False
        board_values = take_turn(direction, board_values)
        spawn_new = old_board_values != board_values
        if old_board_values == board_values:
            possible_bot_directions.remove(direction)
        else:
            possible_bot_directions = [d_up, d_left, d_right, d_down]
        direction = ''
        time.sleep(0.2)

    if direction:
        old_board_values = list(map(list, board_values))
        board_values = take_turn(direction, board_values)
        direction = ''
        spawn_new = old_board_values != board_values

    if game_over or moves == 0:
        game_over = True
        draw_over()
        if high_score > init_high:
            file = open('high_score', 'w')
            file.write(f'{high_score}')
            file.close()
            init_high = high_score

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYUP and not game_over:
            if event.key == pygame.K_UP:
                direction = d_up
            elif event.key == pygame.K_DOWN:
                direction = d_down
            elif event.key == pygame.K_LEFT:
                direction = d_left
            elif event.key == pygame.K_RIGHT:
                direction = d_right
            elif event.key == pygame.K_SPACE:
                bot = not bot

            if game_over:
                if event.key == pygame.K_RETURN:
                    board_values = [[0 for _ in range(4)] for _ in range(4)]
                    spawn_new = True
                    init_count = 0
                    score = 0
                    direction = ''
                    game_over = False

    if score > high_score:
        high_score = score

    pygame.display.flip()
pygame.quit()
