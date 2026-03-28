import pygame
import random

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colors
YELLOW = (255, 223, 0)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
DARK_GREEN = (0, 100, 0)

# Load images
face = pygame.image.load("face.png")
face = pygame.transform.scale(face, (70, 60))  # Wider and bigger (70x60)

trophy = pygame.image.load("trophy.png")
trophy = pygame.transform.scale(trophy, (70, 70))

# Load game over image
game_over_img = pygame.image.load("image.png")
game_over_img = pygame.transform.scale(game_over_img, (300, 200))

# Load start screen image
start_img = pygame.image.load("start.png")
start_img = pygame.transform.scale(start_img, (200, 150))

# Player
player_x = 100
player_y = HEIGHT // 2
velocity = 0
gravity = 0.5
jump = -8

# Game state
game_started = False
game_over = False

# Pipes (trophies)
pipes = []
pipe_width = 70
gap = 250
pipe_speed = 2.3

# Score
score = 0
font = pygame.font.SysFont(None, 50)
passed_pipes = []  # Track which pipes we've scored for

# Load and play background music
try:
    pygame.mixer.music.load("Bole Jo Koyal Bago Mein Tik Tok - 64Kbps-(Mr-Jat.in).mp3")
    pygame.mixer.music.set_volume(0.3)  # Set background music to 70% volume
    # Set start time to 1:42 (102 seconds) and end time to 2:10 (130 seconds)
    pygame.mixer.music.play(loops=-1, start=102.0)
    # We'll stop it at 2:10 manually in the game loop
    music_start_time = pygame.time.get_ticks()
    music_duration = 28  # 28 seconds from 1:42 to 2:10
except:
    print("Could not load music file")

def create_pipe(first_pipe=False):
    gap_y = random.randint(100, HEIGHT - 300)
    if first_pipe:
        return [150, gap_y]  # First pipe starts in front of Dhoni (x=150)
    else:
        return [WIDTH, gap_y]  # Normal pipes start at right edge

def draw_pipes(pipes):
    for pipe in pipes:
        x, gap_y = pipe
        
        # Draw top pipe (green rectangle)
        top_pipe = pygame.Rect(x, 0, pipe_width, gap_y)
        pygame.draw.rect(screen, GREEN, top_pipe)
        pygame.draw.rect(screen, DARK_GREEN, top_pipe, 3)
        
        # Add trophy decoration on top pipe
        if gap_y > 40:
            screen.blit(trophy, (x, gap_y - 70))
        
        # Draw bottom pipe (green rectangle)
        bottom_pipe = pygame.Rect(x, gap_y + gap, pipe_width, HEIGHT - gap_y - gap)
        pygame.draw.rect(screen, GREEN, bottom_pipe)
        pygame.draw.rect(screen, DARK_GREEN, bottom_pipe, 3)
        
        # Add trophy decoration on bottom pipe
        if HEIGHT - gap_y - gap > 40:
            screen.blit(trophy, (x, gap_y + gap))

def move_pipes(pipes):
    for pipe in pipes:
        pipe[0] -= pipe_speed
    return [pipe for pipe in pipes if pipe[0] > -pipe_width]

def check_collision(pipes, px, py):
    player_rect = pygame.Rect(px, py, 70, 60)  # Updated to new face size (70x60)
    
    for pipe in pipes:
        x, gap_y = pipe
        
        # Top pipe collision
        top_rect = pygame.Rect(x, 0, pipe_width, gap_y)
        # Bottom pipe collision  
        bottom_rect = pygame.Rect(x, gap_y + gap, pipe_width, HEIGHT - gap_y - gap)
        
        if player_rect.colliderect(top_rect) or player_rect.colliderect(bottom_rect):
            return True
    
    # Check boundaries
    if py < 0 or py > HEIGHT - 60:  # Updated height to 60
        return True
    
    return False

running = True
frame_count = 0

while running:
    screen.fill(YELLOW)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_started and not game_over:
                    game_started = True
                elif game_started and not game_over:
                    velocity = jump
                    # Play jump sound (0.4 second)
                    try:
                        jump_sound = pygame.mixer.Sound("ek_chakke_ne_world_cup.mp3")
                        jump_sound.set_volume(1.0)  # Maximum volume for jump sound
                        jump_sound.play(maxtime=400)  # Play for 400ms (0.4 second)
                    except:
                        pass
                elif game_over:  # Restart with spacebar when game is over
                    # Restart game
                    game_started = False
                    game_over = False
                    player_y = HEIGHT // 2
                    velocity = 0
                    pipes = []
                    score = 0
                    passed_pipes = []
                    frame_count = 0
                    # Restart background music
                    try:
                        pygame.mixer.music.play(loops=-1, start=102.0)
                        music_start_time = pygame.time.get_ticks()
                    except:
                        pass
            elif event.key == pygame.K_r and game_over:
                # Restart game
                game_started = False
                game_over = False
                player_y = HEIGHT // 2
                velocity = 0
                pipes = []
                score = 0
                passed_pipes = []
                frame_count = 0
                # Restart background music
                try:
                    pygame.mixer.music.play(loops=-1, start=102.0)
                    music_start_time = pygame.time.get_ticks()
                except:
                    pass

    if game_over:
        # Display game over image
        game_over_rect = game_over_img.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        screen.blit(game_over_img, game_over_rect)
        
        game_over_text = font.render("GAME OVER!", True, BLACK)
        game_over_text_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))
        screen.blit(game_over_text, game_over_text_rect)
        
        score_text = font.render(f"Score: {score}", True, BLACK)
        score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 150))
        screen.blit(score_text, score_rect)
        
        restart_text = font.render("Press SPACE or R to restart", True, BLACK)
        restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 200))
        screen.blit(restart_text, restart_rect)
    elif not game_started:
        # Show start screen
        # Display start image
        start_rect = start_img.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        screen.blit(start_img, start_rect)
        
        start_text = font.render("Press SPACE to Start", True, BLACK)
        start_rect = start_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))
        screen.blit(start_text, start_rect)
    else:
        # Game logic
        velocity += gravity
        player_y += velocity

        # Spawn pipes (first one extremely early, then normal spacing)
        if frame_count == 2:  # First pipe after just 2 frames (0.03 seconds)
            pipes.append(create_pipe(first_pipe=True))
        elif frame_count % 90 == 0 and frame_count > 2:  # Normal spacing after first
            pipes.append(create_pipe(first_pipe=False))

        pipes = move_pipes(pipes)

        # Draw
        draw_pipes(pipes)
        screen.blit(face, (player_x, player_y))

        # Collision
        if check_collision(pipes, player_x, player_y) and not game_over:
            print("GAME OVER - Score:", score)
            game_over = True
            # Stop background music
            pygame.mixer.music.stop()
            # Play game over sound
            try:
                game_over_sound = pygame.mixer.Sound("ek_chakke_ne_world_cup.mp3")
                game_over_sound.play()
            except:
                print("Could not load game over sound")

        # Score for passing pipes (2 points for top and bottom set)
        for pipe in pipes:
            x, gap_y = pipe
            # Check if player passed the pipe and hasn't scored for it yet
            if x + pipe_width < player_x and pipe not in passed_pipes:
                score += 2  # 2 points for passing both top and bottom bars
                passed_pipes.append(pipe)

        # Display score
        text = font.render(str(score), True, BLACK)
        screen.blit(text, (WIDTH//2 - 20, 50))

        # Control music loop - restart at 1:42 after reaching 2:10
        current_time = pygame.time.get_ticks()
        if current_time - music_start_time > music_duration * 1000:  # Convert to milliseconds
            pygame.mixer.music.play(loops=-1, start=102.0)
            music_start_time = current_time

    pygame.display.update()
    clock.tick(60)
    frame_count += 1

pygame.quit()