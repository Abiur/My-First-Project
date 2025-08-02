import pygame
import time
import random

# Initialize pygame
pygame.init()

# Set display dimensions
WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 12  # snake body block size

# Bigger sizes for apple and snake head
APPLE_SIZE = 20
SNAKE_HEAD_SIZE = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (213, 50, 80)

# Game settings
SNAKE_SPEED = 15

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock for controlling speed
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont("bahnschrift", 25)

# Load images and scale to bigger size
apple_img = pygame.image.load("apple.png")
apple_img = pygame.transform.scale(apple_img, (APPLE_SIZE, APPLE_SIZE))

snake_head_img = pygame.image.load("snake_head.png")
snake_head_img = pygame.transform.scale(snake_head_img, (SNAKE_HEAD_SIZE, SNAKE_HEAD_SIZE))

# Draw gradient background
def draw_gradient_background(start_color, end_color):
    for y in range(HEIGHT):
        r = start_color[0] + (end_color[0] - start_color[0]) * y // HEIGHT
        g = start_color[1] + (end_color[1] - start_color[1]) * y // HEIGHT
        b = start_color[2] + (end_color[2] - start_color[2]) * y // HEIGHT
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

# Display message
def message(msg, color, x, y):
    text = font.render(msg, True, color)
    screen.blit(text, [x, y])

# Draw snake with image head + round body
def draw_snake(block_size, snake_list):
    for i, block in enumerate(snake_list):
        if i == len(snake_list) - 1:
            # For head, adjust position because head size is bigger than body block size
            # Center the bigger head on snake position
            head_x = block[0] + (block_size // 2) - (SNAKE_HEAD_SIZE // 2)
            head_y = block[1] + (block_size // 2) - (SNAKE_HEAD_SIZE // 2)
            screen.blit(snake_head_img, (head_x, head_y))
        else:
            # Draw round body using circle
            center_x = block[0] + block_size // 2
            center_y = block[1] + block_size // 2
            radius = block_size // 2
            pygame.draw.circle(screen, GREEN, (center_x, center_y), radius)

# Main game loop
def game_loop():
    game_over = False
    game_close = False

    # Position snake at grid (multiple of BLOCK_SIZE)
    x = WIDTH // 2 // BLOCK_SIZE * BLOCK_SIZE
    y = HEIGHT // 2 // BLOCK_SIZE * BLOCK_SIZE
    x_change = 0
    y_change = 0

    snake_list = []
    length_of_snake = 1

    # Food position also multiples of BLOCK_SIZE for easy collision
    food_x = random.randrange(0, WIDTH - APPLE_SIZE, BLOCK_SIZE)
    food_y = random.randrange(0, HEIGHT - APPLE_SIZE, BLOCK_SIZE)

    while not game_over:
        while game_close:
            draw_gradient_background((10, 10, 40), (30, 30, 100))
            message("You Lost! Press C to Play Again or Q to Quit", RED, WIDTH // 6, HEIGHT // 3)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = BLOCK_SIZE
                    x_change = 0

        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        x += x_change
        y += y_change

        draw_gradient_background((10, 10, 40), (30, 30, 100))

        # Draw apple with updated bigger size
        screen.blit(apple_img, (food_x, food_y))

        snake_head = [x, y]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(BLOCK_SIZE, snake_list)
        pygame.display.update()

        # Use Rect collision detection for apple eating with bigger sizes
        snake_head_rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        apple_rect = pygame.Rect(food_x, food_y, APPLE_SIZE, APPLE_SIZE)
        if snake_head_rect.colliderect(apple_rect):
            food_x = random.randrange(0, WIDTH - APPLE_SIZE, BLOCK_SIZE)
            food_y = random.randrange(0, HEIGHT - APPLE_SIZE, BLOCK_SIZE)
            length_of_snake += 1

        clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()

# Run the game
game_loop()
