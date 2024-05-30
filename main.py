# Imports modules needed
import pygame
import random
from number import Number

# Initializes Pygame
pygame.init()

width, height = 1000, 600

icon = pygame.image.load(f"Assets\\icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Worst UI")
screen = pygame.display.set_mode((width, height), 0, 32)
display = pygame.Surface((width, height))
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
fps = 60

bigFontObj = pygame.font.SysFont("arial", 20)
fontObj = pygame.font.SysFont("arial", 15)
title = bigFontObj.render("Please Enter your Date of Birth", True, (255, 255, 255))
dob = fontObj.render("Date of Birth: 00-00-0000", True, (255, 255, 255))

mouse_pos = pygame.mouse.get_pos()
last_mouse_pos = None
clicking = False

lineSegments = []
rect_lines = [[(25, 75), (975, 75)], [(25, 75), (25, 575)], [(975, 75), (975, 575)], [(25, 575), (975, 575)]]
numbers = []

for n in range(30):
    numbers.append(Number(random.randint(0, 9)))

running = True
while running:
    display.fill((0, 0, 0))

    events = pygame.event.get()

    # Event loop
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    clicking = pygame.mouse.get_pressed()[0]

    display.blit(title, (500 - title.get_width() / 2, 10))
    display.blit(dob, (500 - dob.get_width() / 2, 40))

    mouse_pos = pygame.mouse.get_pos()

    for rectline in rect_lines:
        pygame.draw.line(display, (255, 255, 255), rectline[0], rectline[1], 5)
        for number in numbers:
            if number.rect.clipline(rectline[0], rectline[1]):
                number.change_vector()

    for number in numbers:
        number.move()
        number.draw(display)

    if clicking:
        if mouse_pos[0] > 25 and mouse_pos[0] < 975 and mouse_pos[1] > 75 and mouse_pos[1] < 575:
            lineSegments.append([mouse_pos, last_mouse_pos])

    for segment in lineSegments:    
        pygame.draw.line(display, (255, 255, 255), segment[0], segment[1], 5)

    screen.blit(display, (0, 0))
    if mouse_pos[0] > 25 and mouse_pos[0] < 975 and mouse_pos[1] > 75 and mouse_pos[1] < 575:
        last_mouse_pos = mouse_pos

    # Sets fps and updates screen
    clock.tick(fps)
    pygame.display.update()

pygame.quit()