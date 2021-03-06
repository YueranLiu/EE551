import os
import sys
import pygame
import Levels


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)

BGMPath = os.path.join(os.getcwd(), 'sounds/latale.mp3')
ICON = pygame.image.load('images/icon.png')

packmanPic = 'images/pacman.png'
ghost1Pic = 'images/Blinky.png'
ghost2Pic = 'images/Clyde.png'
ghost3Pic = 'images/Inky.png'
ghost4Pic = 'images/Pinky.png'
PlayerPath = os.path.join(os.getcwd(), packmanPic)
Ghost1Path = os.path.join(os.getcwd(), ghost1Pic)
Ghost2Path = os.path.join(os.getcwd(), ghost2Pic)
Ghost3Path = os.path.join(os.getcwd(), ghost3Pic)
Ghost4Path = os.path.join(os.getcwd(), ghost4Pic)

def key_is_down(event, player_sprites):
    if event.key == pygame.K_LEFT:
        changeSpeed([-1,0], player_sprites)
    elif event.key == pygame.K_RIGHT:
        changeSpeed([1,0],player_sprites)
    elif event.key == pygame.K_UP:
        changeSpeed([0, -1],player_sprites)
    elif event.key == pygame.K_DOWN:
        changeSpeed([0, 1],player_sprites)


def changeSpeed(speed, player_sprites):
    for hero in player_sprites:
        hero.changeSpeed(speed)

def key_is_up(event, player_sprites):
    if (event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT) or (event.key == pygame.K_UP) or (
           event.key == pygame.K_DOWN):
        for hero in player_sprites:
            hero.is_move = False


def startLevelGame(level, screen, font):
    clock = pygame.time.Clock()
    SCORE = 0
    wall_sprites = level.setupWalls(PURPLE)
    gate_sprites = level.setupGate(WHITE)
    player_sprites, ghost_sprites = level.setupPlayers(PlayerPath, [Ghost1Path, Ghost2Path, Ghost3Path, Ghost4Path])
    food_sprites = level.setupFood(YELLOW, WHITE)
    is_clearance = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(-1)
                pygame.QUIT()
            if event.type == pygame.KEYDOWN:
                key_is_down(event, player_sprites)

            if event.type == pygame.KEYUP:
                key_is_up(event, player_sprites)
                #if (event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT) or (event.key == pygame.K_UP) or (
                #       event.key == pygame.K_DOWN):
                #    hero.is_move = False
        screen.fill(BLACK)
        for hero in player_sprites:
            hero.update(wall_sprites, gate_sprites)
        player_sprites.draw(screen)
        for hero in player_sprites:
            food_eaten = pygame.sprite.spritecollide(hero, food_sprites, True)
        SCORE += len(food_eaten)
        wall_sprites.draw(screen)
        gate_sprites.draw(screen)
        food_sprites.draw(screen)
        for ghost in ghost_sprites:
           

            if ghost.tracks_loc[1] < ghost.tracks[ghost.tracks_loc[0]][2]:
                ghost.changeSpeed(ghost.tracks[ghost.tracks_loc[0]][0: 2])
                ghost.tracks_loc[1] += 1
            else:
                if ghost.tracks_loc[0] < len(ghost.tracks) - 1:
                    ghost.tracks_loc[0] += 1
                elif ghost.role_name == 'Clyde':
                    ghost.tracks_loc[0] = 2
                else:
                    ghost.tracks_loc[0] = 0
                ghost.changeSpeed(ghost.tracks[ghost.tracks_loc[0]][0: 2])
                ghost.tracks_loc[1] = 0
            if ghost.tracks_loc[1] < ghost.tracks[ghost.tracks_loc[0]][2]:
                ghost.changeSpeed(ghost.tracks[ghost.tracks_loc[0]][0: 2])
            else:
                if ghost.tracks_loc[0] < len(ghost.tracks) - 1:
                    loc0 = ghost.tracks_loc[0] + 1
                elif ghost.role_name == 'Clyde':
                    loc0 = 2
                else:
                    loc0 = 0
                ghost.changeSpeed(ghost.tracks[loc0][0: 2])
            ghost.update(wall_sprites, None)
        ghost_sprites.draw(screen)
        score_text = font.render("Score: %s" % SCORE, True, RED)
        screen.blit(score_text, [20, 20])
        if len(food_sprites) == 0:
            is_clearance = True
            break
        if pygame.sprite.groupcollide(player_sprites, ghost_sprites, False, False):
            is_clearance = False
            break
        pygame.display.flip()
        clock.tick(10)
    return is_clearance


def showText(screen, font, is_clearance, flag=False):
    clock = pygame.time.Clock()
    msg = 'Game Over!' if not is_clearance else 'Congratulations, you won!'
    positions = [[235, 233], [65, 303], [170, 333]] if not is_clearance else [[145, 233], [65, 303], [170, 333]]
    surface = pygame.Surface((400, 200))
    surface.set_alpha(10)
    surface.fill((128, 128, 128))
    screen.blit(surface, (100, 200))
    texts = [font.render(msg, True, WHITE),
             font.render('Press ENTER to continue or play again.', True, WHITE),
             font.render('Press ESCAPE to quit.', True, WHITE)]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if is_clearance:
                        if not flag:
                            return
                        else:
                            main(initialize())
                    else:
                        main(initialize())
                elif event.key == pygame.K_ESCAPE:
                    sys.exit()
                    pygame.quit()
        for idx, (text, position) in enumerate(zip(texts, positions)):
            screen.blit(text, position)
        pygame.display.flip()
        clock.tick(10)


def initialize():
    pygame.init()
    pygame.display.set_icon(ICON)
    screen = pygame.display.set_mode([606, 606])
    pygame.display.set_caption('Pacman')
    return screen



def main(screen):
    pygame.mixer.init()
    pygame.mixer.music.load(BGMPath)
    pygame.mixer.music.play(-1, 0.0)
    pygame.font.init()
    fond_small = pygame.font.Font('font/myfont.ttf', 18)
    font_big = pygame.font.Font('font/myfont.ttf',30)

    level = Levels.Level1()
    is_clearance = startLevelGame(level, screen, fond_small)

    showText(screen, font_big, is_clearance, True)


if __name__ == '__main__':
    main(initialize())
