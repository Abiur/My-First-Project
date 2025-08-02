import pygame
import time
import random

# Initialize pygame
pygame.init()

# Set display dimensions
WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 10

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

def message(msg, color, x, y):
    text = font.render(msg, True, color)
    screen.blit(text, [x, y])

def draw_snake(block_size, snake_list):
    for block in snake_list:
        pygame.draw.rect(screen, GREEN, [block[0], block[1], block_size, block_size])

def game_loop():
    game_over = False
    game_close = False
    
    x = WIDTH // 2
    y = HEIGHT // 2
    x_change = 0
    y_change = 0
    
    snake_list = []
    length_of_snake = 1
    
    food_x = random.randrange(0, WIDTH - BLOCK_SIZE, BLOCK_SIZE)
    food_y = random.randrange(0, HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
    
    while not game_over:
        while game_close:
            screen.fill(BLACK)
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
                if event.key == pygame.K_LEFT:
                    x_change = -BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = BLOCK_SIZE
                    x_change = 0
        
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True
        
        x += x_change
        y += y_change
        
        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])
        
        snake_head = []
        snake_head.append(x)
        snake_head.append(y)
        snake_list.append(snake_head)
        
        if len(snake_list) > length_of_snake:
            del snake_list[0]
        
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True
        
        draw_snake(BLOCK_SIZE, snake_list)
        pygame.display.update()
        
        if x == food_x and y == food_y:
            food_x = random.randrange(0, WIDTH - BLOCK_SIZE, BLOCK_SIZE)
            food_y = random.randrange(0, HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
            length_of_snake += 1
        
        clock.tick(SNAKE_SPEED)
    
    pygame.quit()
    quit()

#Run the game
game_loop()
