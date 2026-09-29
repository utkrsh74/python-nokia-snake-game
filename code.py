import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Define Color palette (classic nokia monochrome greens)
COLOR_SHEEL = (190,195, 180)  # Outer gray-green plastic
COLOR_SCREEN_BG = (143, 166, 126) # characteristic LCD backlight screen
COLOR_PIXEL_DARK = (45, 52, 40) # Active dark screen pixels
COLOR_KEYPAD = (210, 215, 205) # Button color
COLOR_TEXT = (30,35,25)

# frame and matrix setup
CELL_SIZE = 10
GRID_WIDTH = 20
GRID_HEIGHT = 18

# UI/Dimensions (Drawing a retro phone body around the game)
SCREEN_WIDTH =200
SCREEN_HEIGHT = 180
PADDING_TOP = 40
PADDING_LEFT =30

WINDOW_WIDTH = 260
WINDOW_HEIGHT = 440

# Setup window display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Nokia 3310 Snake Classic")
clock = pygame.time.Clock()

# Fonts 
font_game = pygame.font.SysFont("Courier",14, bold=True)
font_retro = pygame.font.SysFont("Arial", 11, bold=True)

def draw_phone_body(score, game_over):
    #fill background/desk
    screen.fill((40, 44, 52))

    # 1.Outer phone body shell
    phone_rect = pygame.Rect(15, 15, WINDOW_WIDTH - 30, WINDOW_HEIGHT - 30)
    pygame.draw.rect(screen, COLOR_SHEEL, phone_rect, border_radius=40)
    pygame.draw.rect(screen, COLOR_PIXEL_DARK, phone_rect, width=3, border_radius=40)

    # 2. LCD Screen Glass Border
    screen_border = pygame.Rect(PADDING_LEFT - 5, PADDING_TOP - 25, SCREEN_WIDTH + 10, SCREEN_HEIGHT + 30)
    pygame.draw.rect(screen, COLOR_PIXEL_DARK, screen_border, width=2, border_radius=5)

    # 3. Active LCD Backlight Screen
    game_screen = pygame.Rect(PADDING_LEFT, PADDING_TOP, SCREEN_WIDTH, SCREEN_HEIGHT)
    pygame.draw.rect(screen, COLOR_SCREEN_BG, game_screen)
    pygame.draw.rect(screen, COLOR_PIXEL_DARK, game_screen, width=1)


    # Header bar inside the screen (score display)
    pygame.draw.line(screen, COLOR_PIXEL_DARK, (PADDING_LEFT, PADDING_TOP - 1), (PADDING_LEFT + SCREEN_WIDTH, PADDING_TOP - 1), 1)
    score_txt = font_game.render(f"Score:{score:04d}", True, COLOR_PIXEL_DARK)
    screen.blit(score_txt, (PADDING_LEFT + 5, PADDING_TOP - 20))

    # 4. Mock keypad Design (visual representation of 2,4,6,8)
    key_y_start = 240
    key_w, key_h = 45, 30
    cols = [35, 105, 175]

    # Draw keypad buttons grid (Rows for 1-3, 4-6, 7-9)
    labels = [["1", "2 ▲", "3"], ["4 ◄", "5", "6 ►"], ["7", "8 ▼", "9"]]
    for row_idx, row_y in enumerate([key_y_start, key_y_start + 40, key_y_start + 80]):
        for col_idx, col_x in enumerate(cols):
            btn_rect = pygame.Rect(col_x, row_y, key_w, key_h)
            # Highlight control keys slightly
            is_control = (row_idx == 0 and col_idx == 1) or (row_idx == 1 and col_idx in [0, 2]) or (row_idx == 2 and col_idx == 1)
            bg_color = (230, 235, 225) if is_control else COLOR_KEYPAD
            
            pygame.draw.rect(screen, bg_color, btn_rect, border_radius=8)
            pygame.draw.rect(screen, COLOR_PIXEL_DARK, btn_rect, width=1, border_radius=8)
            
            lbl = font_retro.render(labels[row_idx][col_idx], True, COLOR_TEXT)
            lbl_rect = lbl.get_rect(center=btn_rect.center)
            screen.blit(lbl, lbl_rect)

def main():
    # Game Variables
    snake = [(10, 9), (9, 9), (8, 9)]  # Grid coordinates
    direction = (1, 0)                  # Initial moving right
    next_direction = (1, 0)
    
    # Generate initial food
    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    while food in snake:
        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        
    score = 0
    game_over = False

    while True:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key in [pygame.K_5, pygame.K_KP5, pygame.K_RETURN, pygame.K_SPACE]:
                        main() # Restart the game
                else:
                    # Keypad configurations:
                    # 2 / Up Arrow -> UP
                    if (event.key == pygame.K_2 or event.key == pygame.K_KP2 or event.key == pygame.K_UP) and direction != (0, 1):
                        next_direction = (0, -1)
                    # 8 / Down Arrow -> DOWN
                    elif (event.key == pygame.K_8 or event.key == pygame.K_KP8 or event.key == pygame.K_DOWN) and direction != (0, -1):
                        next_direction = (0, 1)
                    # 4 / Left Arrow -> LEFT
                    elif (event.key == pygame.K_4 or event.key == pygame.K_KP4 or event.key == pygame.K_LEFT) and direction != (1, 0):
                        next_direction = (-1, 0)
                    # 6 / Right Arrow -> RIGHT
                    elif (event.key == pygame.K_6 or event.key == pygame.K_KP6 or event.key == pygame.K_RIGHT) and direction != (-1, 0):
                        next_direction = (1, 0)

        # 2. Game Logic Updates
        if not game_over:
            direction = next_direction
            # Calculate new head position
            head_x, head_y = snake[0]
            dir_x, dir_y = direction
            new_head = (head_x + dir_x, head_y + dir_y)

            # Collision Detection: Boundaries or Self-eating
            if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
                new_head in snake):
                game_over = True
            else:
                snake.insert(0, new_head)
                # Check if food is eaten
                if new_head == food:
                    score += 10
                    # Relocate food
                    while True:
                        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                        if food not in snake:
                            break
                else:
                    snake.pop() # Remove tail segment if food wasn't eaten

        # 3. Drawing
        draw_phone_body(score, game_over)
        
        # Draw Food (Classic square pixel)
        food_rect = pygame.Rect(PADDING_LEFT + food[0]*CELL_SIZE, PADDING_TOP + food[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, COLOR_PIXEL_DARK, food_rect)
        
        # Draw Snake
        for idx, segment in enumerate(snake):
            seg_rect = pygame.Rect(PADDING_LEFT + segment[0]*CELL_SIZE, PADDING_TOP + segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if idx == 0:
                # Differentiate head with a small border styling
                pygame.draw.rect(screen, COLOR_PIXEL_DARK, seg_rect)
                pygame.draw.rect(screen, COLOR_SCREEN_BG, seg_rect.inflate(-4, -4))
            else:
                # Solid body pixel
                pygame.draw.rect(screen, COLOR_PIXEL_DARK, seg_rect.inflate(-2, -2))

        # Game Over Overlay
        if game_over:
            # Semi-transparent screen wipe effect simulating old screen clearing
            go_text1 = font_game.render("GAME OVER", True, COLOR_PIXEL_DARK)
            go_text2 = font_retro.render("Press 5 to Retry", True, COLOR_PIXEL_DARK)
            
            screen.blit(go_text1, (PADDING_LEFT + 55, PADDING_TOP + 70))
            screen.blit(go_text2, (PADDING_LEFT + 50, PADDING_TOP + 95))

        pygame.display.flip()
        
        # Dynamic speed curve based on score (starts smooth, gains difficulty)
        current_speed = 7 + min(score // 30, 8)
        clock.tick(current_speed)

if __name__ == "__main__":
    main()

