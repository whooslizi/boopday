import pygame, sys, random, webbrowser

pygame.init()
W, H = 400, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("boop game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Courier New", 24)
small_font = pygame.font.SysFont("Courier New", 18)

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (135,206,250)
GREEN = (0,200,0)
RED = (200,0,0)

phase = "start"
quiz_data = [
    {"q": "Dai hoc Cong nghe thuoc DH nao?", "opts": ["DH Kinh te", "DH Bach Khoa", "DHQG Ha Noi", "DH GTVT"], "a": 2},
    {"q": "Viet tat cua truong la gi?", "opts": ["UET", "NEU", "FTU", "PTIT"], "a": 0},
    {"q": "Nam thanh lap UET?", "opts": ["1990", "1999", "2004", "2000"], "a": 2}
]
quiz_index = 0
quiz_selected = 0

bird_y = H//2
bird_v = 0
gravity = 0.5
jump = -7
pipes = []
pipe_gap = 150
pipe_timer = 0
pipe_speed = 3
score = 0
game_over = False

# Password input
password_input = ""
password_correct = "uet2025"
password_error = False

def draw_text(text, x, y, f=font, c=WHITE):
    t = f.render(text, True, c)
    screen.blit(t, (x, y))

def reset_game():
    global bird_y, bird_v, pipes, score, game_over
    bird_y = H//2
    bird_v = 0
    pipes.clear()
    score = 0
    game_over = False

def draw_flappy():
    pygame.draw.circle(screen, RED, (60, int(bird_y)), 12)
    for x, gap_y in pipes:
        pygame.draw.rect(screen, GREEN, (x, 0, 50, gap_y))
        pygame.draw.rect(screen, GREEN, (x, gap_y + pipe_gap, 50, H))

def flappy_logic():
    global bird_y, bird_v, pipe_timer, score, game_over, phase
    bird_v += gravity
    bird_y += bird_v
    pipe_timer += 1
    if pipe_timer > 90:
        pipe_timer = 0
        gap_y = random.randint(100, 400)
        pipes.append([W, gap_y])
    for p in pipes:
        p[0] -= pipe_speed
    pipes[:] = [p for p in pipes if p[0] > -60]
    for x, gap_y in pipes:
        if 60 + 12 > x and 60 - 12 < x + 50:
            if bird_y < gap_y or bird_y > gap_y + pipe_gap:
                game_over = True
    if bird_y < 0 or bird_y > H:
        game_over = True
    for p in pipes:
        if p[0] + 50 == 60:
            score += 1
    if score >= 5:
        phase = "show_password"

def draw_quiz():
    q = quiz_data[quiz_index]
    draw_text("Cau hoi:", 20, 40)
    draw_text(q["q"], 20, 80)
    for i, opt in enumerate(q["opts"]):
        color = GREEN if i == quiz_selected else WHITE
        draw_text(f"{chr(65+i)}. {opt}", 40, 140 + i*40, font, color)

def draw_start():
    draw_text("dumb game", 40, 200)
    draw_text("Press ENTER to start", 70, 300)

def draw_show_password():
    draw_text("Congrats! You won", 40, 160)
    draw_text("Password: uet2025", 70, 220, small_font)
    draw_text("Press ENTER to continue", 60, 300, small_font)

def draw_password_prompt():
    global password_error
    draw_text("Enter password to continue:", 20, 180)
    pygame.draw.rect(screen, WHITE, (60, 230, 280, 40), 2)
    draw_text(password_input, 70, 240, font, WHITE)
    if password_error:
        draw_text("❌ Wrong password", 90, 300, small_font, RED)

while True:
    screen.fill(BLUE)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if phase == "start" and e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                phase = "quiz"

        elif phase == "quiz" and e.type == pygame.KEYDOWN:
            if e.key == pygame.K_DOWN:
                quiz_selected = (quiz_selected + 1) % 4
            elif e.key == pygame.K_UP:
                quiz_selected = (quiz_selected - 1) % 4
            elif e.key == pygame.K_RETURN:
                correct = quiz_data[quiz_index]["a"]
                if quiz_selected == correct:
                    quiz_index += 1
                    quiz_selected = 0
                    if quiz_index >= len(quiz_data):
                        reset_game()
                        phase = "flappy"

        elif phase == "flappy":
            if e.type == pygame.KEYDOWN and not game_over:
                if e.key == pygame.K_SPACE:
                    bird_v = jump
            if e.type == pygame.KEYDOWN and game_over:
                if e.key == pygame.K_r:
                    reset_game()

        elif phase == "show_password" and e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                phase = "enter_password"

        elif phase == "enter_password":
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_BACKSPACE:
                    password_input = password_input[:-1]
                elif e.key == pygame.K_RETURN:
                    if password_input.strip() == password_correct:
                        webbrowser.open("https://nimble-speculoos-e55a66.netlify.app/")
                        pygame.quit()
                        sys.exit()
                    else:
                        password_error = True
                        password_input = ""
                elif e.unicode.isprintable():
                    if len(password_input) < 20:
                        password_input += e.unicode

    if phase == "start":
        draw_start()
    elif phase == "quiz":
        draw_quiz()
    elif phase == "flappy":
        if not game_over:
            flappy_logic()
        draw_flappy()
        draw_text(f"Score: {score}", 10, 10)
        if game_over:
            draw_text("Game Over! Press R to restart", 40, H//2)
    elif phase == "show_password":
        draw_show_password()
    elif phase == "enter_password":
        draw_password_prompt()

    pygame.display.flip()
    clock.tick(60)
