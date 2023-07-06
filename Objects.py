import pygame
import random
from enum import Enum

class GameState(Enum):
    PRE_GAME = 1
    RUNNING = 2
    END = 3


class Bird(pygame.sprite.Sprite):

    def __init__(self, bird_width, bird_height, game_width, game_height, bird_gravity, bird_jumpheight):
        super().__init__()
        self.images = [
            pygame.transform.scale(pygame.image.load("assets/bird1.png").convert_alpha(), (bird_width, bird_height)),
            pygame.transform.scale(pygame.image.load("assets/bird2.png").convert_alpha(), (bird_width, bird_height)),
            pygame.transform.scale(pygame.image.load("assets/bird3.png").convert_alpha(), (bird_width, bird_height))
        ]
        self.image_index = 0
        self.image_speed = 3
        self.game_width = game_width
        self.game_height = game_height

        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.center = (game_width // 2, game_height // 2)
        self.velocity = 0
        self.bird_gravity = bird_gravity
        self.bird_jumpheight = bird_jumpheight

        self.flap_up = True
        self.flap_countdown = 0

    def reset(self):
        self.velocity = 0
        self.rect = self.image.get_rect()
        self.rect.center = (self.game_width // 2, self.game_height // 2)

    def __check_images(self):
        self.image_speed -= 1
        if self.image_speed <= 0:
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]
            self.image_speed = 3

    def pre_update(self):
        self.__check_images()

        if self.flap_up:
            self.rect.y -= 1
            self.flap_countdown += 1
            if self.flap_countdown >= 13:
                self.flap_countdown = 0
                self.flap_up = False
        else:
            self.rect.y += 1
            self.flap_countdown += 1
            if self.flap_countdown >= 13:
                self.flap_countdown = 0
                self.flap_up = True

    def update(self):
        self.__check_images()

        self.velocity += self.bird_gravity
        self.rect.y += self.velocity

    def fine_update(self, velocityfactor):
        self.__check_images()

        self.velocity += velocityfactor
        self.rect.y += velocityfactor

    def jump(self):
        self.velocity = -self.bird_jumpheight


class UpperTube(pygame.sprite.Sprite):

    def __init__(self, x, tube_height, tube_image, tube_speed):
        super().__init__()
        self.image = pygame.transform.flip(pygame.transform.rotate(tube_image, 180), True, False)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0 - self.image.get_height() + tube_height
        self.tube_speed = tube_speed

    def update(self):
        self.rect.x -= self.tube_speed

class Tube(pygame.sprite.Sprite):

    def __init__(self, x, game_height, tube_speed, tube_gap):
        super().__init__()
        bottom_tube_part_height = random.randint(200, game_height - tube_gap)
        loaded_image = pygame.image.load("assets/pipe.png").convert_alpha()

        self.image = loaded_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = (game_height - bottom_tube_part_height)
        self.tube_speed = tube_speed

        self.upper_part = UpperTube(x, game_height - (bottom_tube_part_height + tube_gap), loaded_image, tube_speed)

    def get_upper_part(self):
        return self.upper_part

    def update(self):
        self.rect.x -= self.tube_speed

class Score(pygame.sprite.Sprite):

    def __init__(self, game_width, gap_between_numbers):
        super().__init__()
        self.zero = pygame.image.load("assets/0.png").convert_alpha()
        self.one = pygame.image.load("assets/1.png").convert_alpha()
        self.two = pygame.image.load("assets/2.png").convert_alpha()
        self.three = pygame.image.load("assets/3.png").convert_alpha()
        self.four = pygame.image.load("assets/4.png").convert_alpha()
        self.five = pygame.image.load("assets/5.png").convert_alpha()
        self.six = pygame.image.load("assets/6.png").convert_alpha()
        self.seven = pygame.image.load("assets/7.png").convert_alpha()
        self.eight = pygame.image.load("assets/8.png").convert_alpha()
        self.nine = pygame.image.load("assets/9.png").convert_alpha()
        self.mapping = {
            0: self.zero,
            1: self.one,
            2: self.two,
            3: self.three,
            4: self.four,
            5: self.five,
            6: self.six,
            7: self.seven,
            8: self.eight,
            9: self.nine
        }
        self.gap_between = gap_between_numbers

        self.count = 0
        self.game_width = game_width
        self.image = self.zero
        self.rect = self.image.get_rect()
        self.rect.x = (self.game_width / 2) - (self.rect.width / 2)
        self.rect.y = 100

    def update(self):
        countString = str(self.count)
        items = len(countString)

        surface_x = 0 - self.gap_between
        surface_y = 0
        allElements = []

        for i in range(items):
            element = self.mapping[int(countString[i])]
            surface_x += element.get_width() + self.gap_between
            surface_y = element.get_height()
            allElements.append(element)

        surface = pygame.Surface((surface_x, surface_y))
        surface.set_colorkey((0, 0, 0))

        for i in range(len(allElements)):
            element = allElements[i]

            if i == 0:
                surface.blit(element, (0, 0))
            elif i == 1 and len(allElements) == 3:
                surface.blit(element, ((surface_x - (element.get_width() * 2) - self.gap_between), 0))
            elif i == 1 and len(allElements) == 4:
                surface.blit(element, ((surface_x - (element.get_width() * 3) - self.gap_between * 2), 0))
            elif i == 2 and len(allElements) == 3:
                surface.blit(element, ((surface_x - (element.get_width() * 1)), 0))
            elif i == 2 and len(allElements) == 4:
                surface.blit(element, ((surface_x - (element.get_width() * 2) - self.gap_between), 0))
            elif i == 3 and len(allElements) == 4:
                surface.blit(element, ((surface_x - element.get_width()), 0))
            else:
                surface.blit(element, ((surface_x - (element.get_width() * i)), 0))

        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.x = (self.game_width / 2) - (self.rect.width / 2)
        self.rect.y = 100

    def reset(self):
        self.count = 0

    def increase(self):
        if self.count < 9999:
            self.count += 1
