import game
import pygame
import Levels
import pytest
import os

# def test_key_is_down():
#     event = pygame.event.Event(pygame.KEYDOWN)
#     event.key = pygame.K_LEFT
#     print(event.key == event.K_LEFT)
#     # sprite = player_sprite
#     # n = key_is_down(event,sprite)
#     # res = None
#     # assert (res == True)
#
# def test_change_speed():
#     speed=[1,0]
#     PlayerPath = os.path.join(os.getcwd(), 'images/pacman.png')
#     Ghost1Path = os.path.join(os.getcwd(), 'images/Blinky.png')
#     Ghost2Path = os.path.join(os.getcwd(), 'images/Clyde.png'
#     Ghost3Path = os.path.join(os.getcwd(), 'images/Inky.png')
#     Ghost4Path = os.path.join(os.getcwd(), 'images/Pinky.png')
#
#     level=Levels.Level1()
#     sprite,sprite1 = level.setupPlayers(PlayerPath, [Ghost1Path, Ghost2Path, Ghost3Path, Ghost4Path])
#     pygame.display.set_mode(sprite)
#     pygame.display.set_mode(sprite1)
#     changeSpeed(speed, sprite)
#     for hero in sprite:
#         assert(hero.changeSpeed==[1,0])

# test_change_speed()



game.main(game.initialize())

def testValidGhos1tpath():
    if not os.path.exists(game.Ghost1Path):
        print("test failed")

def testValidPlayerpath():
    if not os.path.exists(game.PlayerPath):
        print("test failed")


def testValidGhos2tpath():
    if not os.path.exists(game.Ghost2Path):
        print("test failed")

def testValidGhos3tpath():
    if not os.path.exists(game.Ghost3Path):
        print("test failed")

def testValidGhos4tpath():
    if not os.path.exists(game.Ghost4Path):
        print("test failed")
