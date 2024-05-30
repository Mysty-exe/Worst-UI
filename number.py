import pygame
import random
from vector import Vector

pygame.font.init()

class Number:
    fontObj = pygame.font.SysFont("arial", 15)
    speed = 1

    def __init__(self, number):
        self.number = number
        self.text = self.fontObj.render(str(random.randint(0, 9)), True, (255, 255, 255))
        self.rect = self.text.get_rect()
        self.location = Vector(random.randint(25, 950), random.randint(75, 550))
        self.moveVector = Vector(random.randint(-9, 9), random.randint(-9, 9))
        self.rect.x, self.rect.y = self.location.x, self.location.y

    def draw(self, display):
        display.blit(self.text, self.location.coord())

    def move(self):
        self.rect.x, self.rect.y = self.location.x, self.location.y
        self.location += self.moveVector.normalize() * self.speed

    def change_vector(self):
        self.moveVector = Vector(random.randint(-9, 9), random.randint(-9, 9))

