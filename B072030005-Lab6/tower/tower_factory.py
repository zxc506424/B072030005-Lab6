from abc import ABC, abstractmethod
from settings import WIN_WIDTH, WIN_HEIGHT
from tower.attack_strategy import AOE, SingleAttack, Snipe
import os
import pygame

RAPID_TEST_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images", "rapid_test.png")), (70, 70))
PCR_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images", "pcr.png")), (70, 70))
ALCOHOL_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images", "alcohol.png")), (25, 70))
PLOT_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images", "vacant_lot.png")), (20, 20))


class Vacancy:
    def __init__(self, x, y):
        self.image = PLOT_IMAGE
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def clicked(self, x, y):
        return True if self.rect.collidepoint(x, y) else False

    def draw(self, win):
        win.blit(self.image, self.rect)


# tower (product)
class Tower:
    """ parent class of towers """
    def __init__(self, x: int, y: int, attack_strategy, image):
        self.image = image  # image of the tower
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # center of the tower
        self.level = 0  # level of the tower
        self._range = [100, 110, 120, 130, 140, 150]  # tower attack range
        self._damage = [2.0, 2.1, 2.2, 2.3, 2.4, 2.5]   # tower damage
        self.cd_count = 0  # used in self.is_cool_down()
        self.cd_max_count = 60  # used in self.is_cool_down()
        self.attack_strategy = attack_strategy  # chose an attack strategy (AOE, single attack ....)

    @classmethod
    def RapidTest(cls, x, y):
        rapid_test = cls(x, y, SingleAttack(), RAPID_TEST_IMAGE)
        rapid_test._range = [130, 140, 150, 160, 170, 180]
        rapid_test._damage = [2.0, 2.1, 2.2, 2.3, 2.4, 2.5]
        return cls(x, y, SingleAttack(), RAPID_TEST_IMAGE)

    @classmethod
    def Alcohol(cls, x, y):
        alcohol = cls(x, y, AOE(), ALCOHOL_IMAGE)
        alcohol._range = [120, 125, 130, 135, 140, 145]
        alcohol._damage = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
        return alcohol

    @classmethod
    def PCR(cls, x: int, y: int):
        """
        (Q2) create a pcr object (1) cd_max: 120 (2) attack range 100, 105, 110, 115, 120, 125 (3) Single attack
        (Bonus) Single attack to Snipe
        :param x: center x
        :param y: center y
        :return: object
        """
        cd_max_count = 120
        pcr = cls(x, y, Snipe(), PCR_IMAGE)
        pcr._range = [100, 105, 110, 115, 120, 125]    
        pcr._damage = [3.0, 3.2, 3.4, 3.6, 3.8, 4.0]   
        return pcr

    def attack(self, enemy_group):
        # cd
        if self.cd_count < self.cd_max_count:
            self.cd_count += 1
            return
        # syntax: attack_strategy().attack(tower, enemy_group, cd_count)
        # It's something like you hire a "Strategist" to decide how to attack the enemy
        # according to the the input parameters.
        # You can add other ways of attack just by expanding the "attack_strategy.py"
        self.cd_count = self.attack_strategy.attack(enemy_group, self, self.cd_count)

    def get_range(self):
        return self._range[self.level]

    def get_damage(self):
        return self._damage[self.level]

    def clicked(self, x, y):
        return True if self.rect.collidepoint(x, y) else False

    def draw_effect_range(self, win):
        """
        draw the tower effect range, which is a transparent circle.
        """
        surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
        transparency = 120
        pygame.draw.circle(surface, (128, 128, 128, transparency), self.rect.center, self._range[self.level])
        win.blit(surface, (0, 0))




