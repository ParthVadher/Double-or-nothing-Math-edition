import pygame
import random
import sys

pygame.init()

#Default design(height width windown name)
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Double or Nothing: Math Edition")

#Colour Pallete in which u can add and edit
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 139)
LIGHT_BLUE = (173, 216, 230)
TEAL = (0, 128, 128)
CYAN = (0, 255, 255)
GRAY = (200, 200, 200)

#Font size and type (replace none with font name)
font_large = pygame.font.Font(None, 100)
font_medium = pygame.font.Font(None, 74)
font_small = pygame.font.Font(None, 50)

#Music
pygame.mixer.music.load('assets\cbgm.mp3')
pygame.mixer.music.play(-1)
correct_sound = pygame.mixer.Sound('assets\cr.mp3')
wrong_sound = pygame.mixer.Sound('assets\wr.mp3')

username = ""
score = 1
running = True
question = ""
answer = 0
user_answer = ""
show_username_screen = True
double_or_nothing_prompt = False
game_over = False
final_score_display = False
timer = 30
clock = pygame.time.Clock()

question_templates = [
    ("What is {0} + {1}?", lambda x, y: max(0, x + y)),
    ("What is {0} - {1}?", lambda x, y: max(0, abs(x - y))),
    ("What is {0} * {1}?", lambda x, y: max(0, x * y)),
    ("What is {0} / {1}?", lambda x, y: max(0, x // y if y > 0 else 0)),
    ("Find the nature of roots of {0}x² + {1}x + {2} = 0", 
        lambda a, b, c: "Real and Distinct" if b**2 - 4*a*c > 0 else 
                        "Real and Equal" if b**2 - 4*a*c == 0 else 
                        "Complex"),
    ("Can a triangle be formed with sides {0}, {1}, {2}?", 
        lambda a, b, c: "Yes" if a+b>c and a+c>b and b+c>a else "No"),
    ("If {0} coins are tossed, number of possible outcomes?", lambda n: 2**n),
    ("How many 2-digit even numbers can be formed using digits {0}, {1}, {2}, {3}, {4} if repetition is allowed?",
        lambda d1, d2, d3, d4, d5: 10),
    ("How many 2-flag signals can be formed using {0} flags?", lambda f: 12),
]

def generate_question():
    global question, answer, timer
    template = random.choice(question_templates)
    numbers = [random.randint(1, 10) for _ in range(template[0].count("{"))]
    question = template[0].format(*numbers)
    answer = template[1](*numbers)
    timer = 30
#Gradient and shadowing design elements

def draw_gradient(color1, color2):
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

def display_text_with_shadow(text, font, color, x, y, shadow_color=BLACK):
    shadow = font.render(text, True, shadow_color)
    text_surface = font.render(text, True, color)
    screen.blit(shadow, (x + 2, y + 2))
    screen.blit(text_surface, (x, y))

generate_question()

while running:
    if show_username_screen:
        #Username screen design elements
        draw_gradient(DARK_BLUE, LIGHT_BLUE)
        display_text_with_shadow("Enter your username:", font_medium, WHITE, WIDTH // 2 - 200, HEIGHT // 2 - 100)
        display_text_with_shadow(username, font_medium, WHITE, WIDTH // 2 - 100, HEIGHT // 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username:
                    show_username_screen = False
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode
        pygame.display.flip()
        continue

    if final_score_display:
        #Final score design element
        draw_gradient(CYAN, LIGHT_BLUE)
        display_text_with_shadow(f"Final Score: {score}", font_large, GREEN, WIDTH // 2 - 200, HEIGHT // 2 - 100)
        display_text_with_shadow(f"Thanks for playing, {username}!", font_medium, DARK_BLUE, WIDTH // 2 - 250, HEIGHT // 2 + 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        continue

    if game_over:
        #Game over screen design elements
        draw_gradient(GRAY, DARK_BLUE)
        display_text_with_shadow("Game Over!", font_large, RED, WIDTH // 2 - 150, HEIGHT // 2 - 100)
        display_text_with_shadow(f"Your Final Score: {score}", font_medium, BLACK, WIDTH // 2 - 200, HEIGHT // 2 + 50)
        pygame.draw.rect(screen, GREEN, (WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, 50))
        display_text_with_shadow("Replay", font_medium, BLACK, WIDTH // 2 - 50, HEIGHT // 2 + 160)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if WIDTH // 2 - 100 <= mouse_x <= WIDTH // 2 + 100 and HEIGHT // 2 + 150 <= mouse_y <= HEIGHT // 2 + 200:
                    username = ""
                    score = 1
                    user_answer = ""
                    show_username_screen = True
                    double_or_nothing_prompt = False
                    game_over = False
                    final_score_display = False
                    timer = 10
                    generate_question()
        pygame.display.flip()
        continue

    if double_or_nothing_prompt:
        #Double or nothing design element
        draw_gradient(TEAL, LIGHT_BLUE)
        display_text_with_shadow("Double or Nothing? (y/n)", font_medium, WHITE, WIDTH // 2 - 200, HEIGHT // 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    double_or_nothing_prompt = False
                    generate_question()
                elif event.key == pygame.K_n:
                    final_score_display = True
                    double_or_nothing_prompt = False
        pygame.display.flip()
        continue

    draw_gradient(LIGHT_BLUE, GREEN)

    delta_time = clock.tick(30) / 1000.0
    timer -= delta_time
    if timer <= 0:
        game_over = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if user_answer.isdigit() and int(user_answer) == answer:
                    score *= 2
                    correct_sound.play()
                    user_answer = ""
                    double_or_nothing_prompt = True
                else:
                    wrong_sound.play()
                    game_over = True
            elif event.key == pygame.K_BACKSPACE:
                user_answer = user_answer[:-1]
            else:
                user_answer += event.unicode

# Main Screen Design elements
    display_text_with_shadow(f"{question}", font_large, BLACK, WIDTH // 2 - 200, 100)
    display_text_with_shadow(f"Score: {score}", font_medium, GREEN, 50, 20)
    display_text_with_shadow(f"Your Answer: {user_answer}", font_medium, BLACK, 50, 200)
    display_text_with_shadow(f"Time Left: {max(0, int(timer))}", font_medium, RED, WIDTH - 300, 20)
    display_text_with_shadow(f"Player: {username}", font_small, DARK_BLUE, WIDTH - 250, 80)

    pygame.display.flip()

pygame.quit()
sys.exit()
