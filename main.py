# Imports modules needed
import pygame
import random
from vector import Vector
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
fps = 60

bigFontObj = pygame.font.SysFont("arial", 20)
fontObj = pygame.font.SysFont("arial", 15)
title = bigFontObj.render("Please Enter your Date of Birth", True, (255, 255, 255))

mouse_pos = pygame.mouse.get_pos()
last_mouse_pos = pygame.mouse.get_pos()
clicking = False
state = "Game"
failed = 0

lineSegments = []
rect_lines = [[(25, 75), (975, 75)], [(25, 75), (25, 575)], [(975, 75), (975, 575)], [(25, 575), (975, 575)]]
numbers = [Number(random.randint(0, 9)) for n in range(30)]
numbersHit = []

def reset():
    numbers = [Number(random.randint(0, 9)) for n in range(30)]
    numbersHit = []
    lineSegments = []
    
    return numbers, numbersHit, lineSegments

def valid_check():
    ns = [str(n.number) for n in numbersHit]
    if int(f"{ns[0]}{ns[1]}") > 12:
        return False
    elif int(f"{ns[2]}{ns[3]}") > 31:
        return False
    elif int(f"{ns[4]}{ns[5]}{ns[6]}{ns[7]}") > 2023:
        return False
    return True

def get_date():
    ns = [str(n.number) for n in numbersHit]
    if len(ns) < 8 and len != 8:
        for _ in range(8 - len(ns)):
            ns.append("0")

    ns.insert(2, "-")
    ns.insert(5, "-")
    date = "".join(ns)
    return date

running = True
while running:
    display.fill((0, 0, 0))

    events = pygame.event.get()

    # Event loop
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if state == "Fail":
                    state = "Game"
                    numbers, numbersHit, lineSegments = reset()
                elif state == "Sus" or state == "Succeed":
                    running = False

    if state == "Game":
        pygame.mouse.set_visible(False)
        dob = fontObj.render(f"Date of Birth: {get_date()}", True, (255, 255, 255))

        display.blit(title, (500 - title.get_width() / 2, 10))
        display.blit(dob, (500 - dob.get_width() / 2, 40))

        mouse_pos = pygame.mouse.get_pos()

        for rectline in rect_lines:
            pygame.draw.line(display, (255, 255, 255), rectline[0], rectline[1], 5)
            for number in numbers:
                if number.rect.clipline(rectline[0], rectline[1]):
                    if rectline == rect_lines[0]:
                        number.moveVector = Vector(random.randint(-9, 9), random.randint(1, 9))
                    elif rectline == rect_lines[1]:
                        number.moveVector = Vector(random.randint(1, 9), random.randint(-9, 9))
                    elif rectline == rect_lines[2]:
                        number.moveVector = Vector(random.randint(-9, -1), random.randint(-9, 9))
                    elif rectline == rect_lines[3]:
                        number.moveVector = Vector(random.randint(-9, 9), random.randint(-9, -1))

        for number in numbers:
            number.move()
            number.draw(display)
            for segment in lineSegments:
                if number.rect.clipline(segment[0], segment[1]) and number not in numbersHit and len(numbersHit) < 8:
                    numbers.remove(number)
                    numbersHit.append(number)
                    if len(numbersHit) >= 8:
                        if not valid_check():
                            failed += 1
                            if failed < 3:
                                state = "Fail"
                            else:
                                state = "Sus"
                        else:
                            state = "Success"

        if mouse_pos[0] > 25 and mouse_pos[0] < 975 and mouse_pos[1] > 75 and mouse_pos[1] < 575:
            lineSegments.append([mouse_pos, last_mouse_pos])

        for segment in lineSegments:    
            pygame.draw.line(display, (255, 255, 255), segment[0], segment[1], 5)

        if mouse_pos[0] > 25 and mouse_pos[0] < 975 and mouse_pos[1] > 75 and mouse_pos[1] < 575:
            last_mouse_pos = mouse_pos

    elif state == "Succeed":
        pygame.mouse.set_visible(True)
        datetxt = bigFontObj.render(f"Date: {get_date()}", True, (255, 255, 255))
        valid = bigFontObj.render("Valid Date Entered", True, (255, 255, 255))
        enter = fontObj.render("Press Enter to continue", True, (255, 255, 255))
        display.blit(datetxt, (500 - datetxt.get_width() / 2, 250))
        display.blit(valid, (500 - valid.get_width() / 2, 300 - valid.get_height() / 2))
        display.blit(enter, (500 - enter.get_width() / 2, 350))

    elif state == "Fail":
        pygame.mouse.set_visible(True)
        datetxt = bigFontObj.render(f"Date: {get_date()}", True, (255, 255, 255))
        notvalid = bigFontObj.render("Date Inserted Is Not Valid", True, (255, 255, 255))
        enter = fontObj.render("Press Enter to try again", True, (255, 255, 255))
        display.blit(datetxt, (500 - datetxt.get_width() / 2, 250))
        display.blit(notvalid, (500 - notvalid.get_width() / 2, 300 - notvalid.get_height() / 2))
        display.blit(enter, (500 - enter.get_width() / 2, 350))

    elif state == "Sus":
        pygame.mouse.set_visible(True)
        notvalid = bigFontObj.render("Suspicious Activity Detected. Try Again in 72 Hours.", True, (255, 255, 255))
        enter = fontObj.render("Press Enter to exit", True, (255, 255, 255))
        display.blit(notvalid, (500 - notvalid.get_width() / 2, 300 - notvalid.get_height() / 2))
        display.blit(enter, (500 - enter.get_width() / 2, 350))

    screen.blit(display, (0, 0))

    # Sets fps and updates screen
    clock.tick(fps)
    pygame.display.update()

pygame.quit()