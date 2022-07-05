# Alexander Wildey
# Created: April 2018
# 2D Dodgeball Game in PyGame

import sys, random, time, os
import pygame
from pygame.locals import *

FPS = 60
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
TEXTCOLOR = (0, 0, 0)

class Ball(pygame.sprite.Sprite): #class for the dodgeballs
    def __init__(self, xy = (0, 0), mx = 0, my = 0):
        pygame.sprite.Sprite.__init__(self)
        self.imageLoad('Ball.png')
        self.rect.centerx, self.rect.centery = xy

        self.movex = mx
        self.movey = my

    def update(self):
        self.move()
        self.hitWall()

    def move(self):
        self.rect.x += self.movex
        self.rect.y += self.movey

    def imageLoad(self, filename):
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.smoothscale(self.image, (30, 30))
        self.rect = self.image.get_rect()

    def hitWall(self):
        if self.rect.right >= WINDOWWIDTH:
            self.movex *= -1

        elif self.rect.left <= 0:
            self.movex *= -1

        elif self.rect.bottom >= WINDOWHEIGHT:
            self.movey *= -1

        elif self.rect.top <= 0:
            self.movey *= -1

class BallManager(): #class to manage the dodgeballs and hold them in a list
    def __init__(self, ballnum, balls = []):
        self.ballList = balls

        if ballnum > 0:
            self.manyBalls(ballnum)

    def newBall(self, xy = (0, 0), mx = 0, my = 0):
        self.ballList.append(Ball(xy, mx, my))

    def manyBalls(self, ballnum):
        for i in range(ballnum):
            self.newBall((40, 40), 4, 4)

class Player(pygame.sprite.Sprite): #class for the player's character
    def __init__(self, xy):
        pygame.sprite.Sprite.__init__(self)
        self.imgLoad()

        self.rect.centerx, self.rect.centery = xy

        self.movingRight = 0
        self.movingLeft = 0
        self.movingUp = 0
        self.movingDown = 0

    def moveRight(self):
        self.movingRight = 15
        self.rect.x += self.movingRight

    def moveLeft(self):
        self.movingLeft = 15
        self.rect.x -= self.movingLeft

    def moveUp(self):
        self.movingUp = 15
        self.rect.y -= self.movingUp

    def moveDown(self):
        self.movingDown = 15
        self.rect.y += self.movingDown

    def playerMove(self, movingDown, movingUp, movingLeft, movingRight):
        if self.rect.bottom >= WINDOWHEIGHT:
            self.rect.bottom = WINDOWHEIGHT - 1

        elif self.rect.top <= 0:
            self.rect.top = 1

        elif self.rect.left <= 0:
            self.rect.left = 1

        elif self.rect.right >= WINDOWWIDTH:
            self.rect.right = WINDOWWIDTH - 1

    def update(self):
        self.playerMove(self.movingDown, self.movingUp, self.movingLeft, self.movingRight)

    def imgLoad(self):
        self.image = pygame.image.load('player.png')
        self.image = pygame.transform.smoothscale(self.image, (30, 30))
        self.rect = self.image.get_rect()


class Score(pygame.sprite.Sprite): #class for the game score
    def __init__(self, w, h, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.lastScoreTime = time.time()
        self.addScoreFreq = 1
        self.scoreText = pygame.font.Font(None, 26)
        self.image = self.scoreText.render("Score: %d" %(self.score), 1, TEXTCOLOR)
        self.rect = pygame.Rect(w, h, x, y)

    def increaseScore(self):
        if time.time() - self.lastScoreTime > self.addScoreFreq:
            self.score += 1
            self.lastScoreTime = time.time()
            self.image = self.scoreText.render("Score: %d" %(self.score), 1, TEXTCOLOR)

    def update(self):
        self.increaseScore()

class Lives(pygame.sprite.Sprite): #class for the player's lives
    def __init__(self, w, h, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.lives = 3
        self.livesText = pygame.font.Font(None, 26)
        self.image = self.livesText.render("Lives: %s" %(self.lives), 1, TEXTCOLOR)
        self.rect = pygame.Rect(w, h, x, y)

    def update(self):
        self.image = self.livesText.render("Lives: %s" %(self.lives), 1, TEXTCOLOR)

class Game(object): #class for the game
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(1, 30)
        self.DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        self.FPSCLOCK = pygame.time.Clock()
        pygame.display.set_caption('Dodgeball')

        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
        self.background = pygame.image.load('background.png')
        self.DISPLAYSURF.blit(self.background, (0, 0))
        pygame.display.flip()

        self.playerSprite = pygame.sprite.RenderUpdates()
        self.ballSprites = pygame.sprite.RenderUpdates()
        self.scoreSprite = pygame.sprite.RenderUpdates()
        self.livesSprite = pygame.sprite.RenderUpdates()

        self.player = Player((320, 240))

        self.SCORE = Score(540, 25, 100, 25)

        self.LIVES = Lives(30, 25, 50, 25)

        self.playerSprite.add(self.player)

        self.scoreSprite.add(self.SCORE)

        self.livesSprite.add(self.LIVES)

        self.DODGEBALL = 1

        self.dodgeballs = BallManager(self.DODGEBALL)

    def runGame(self):
        running = True

        while running == True: #main game loop
            self.FPSCLOCK.tick(FPS)
            running = self.eventHandler()

            if self.SCORE.score > 0:
                if self.SCORE.score % 10 == 0:
                    self.DODGEBALL += 1
                    self.dodgeballs = BallManager(self.DODGEBALL)
                    self.SCORE.score += 1

            for ball in self.dodgeballs.ballList:
                self.ballSprites.add(ball)

            collisionList = pygame.sprite.groupcollide(self.playerSprite, self.ballSprites, True, False)

            for collision in collisionList:
                self.LIVES.lives -= 1
                if self.LIVES.lives > 0:
                    self.player = Player((WINDOWWIDTH, 240))
                    self.playerSprite.add(self.player)
                    pygame.time.wait(500)

                elif self.LIVES.lives <= 0:
                    running = False

            self.ballSprites.clear(self.DISPLAYSURF, self.background)
            self.playerSprite.clear(self.DISPLAYSURF, self.background)
            self.scoreSprite.clear(self.DISPLAYSURF, self.background)
            self.livesSprite.clear(self.DISPLAYSURF, self.background)

            for sprite in self.ballSprites:
                sprite.update()

            for sprite in self.playerSprite:
                sprite.update()

            for sprite in self.scoreSprite:
                sprite.update()

            for sprite in self.livesSprite:
                sprite.update()

            showBalls = self.ballSprites.draw(self.DISPLAYSURF)
            showPlayer = self.playerSprite.draw(self.DISPLAYSURF)
            showScore = self.scoreSprite.draw(self.DISPLAYSURF)
            showLives = self.livesSprite.draw(self.DISPLAYSURF)

            pygame.display.update(showBalls)
            pygame.display.update(showPlayer)
            pygame.display.update(showScore)
            pygame.display.update(showLives)

    def eventHandler(self): #handles keyboard input for moving player's character
         for event in pygame.event.get():
             if event.type == QUIT:
                 pygame.quit()
                 sys.exit()

             if event.type == KEYDOWN:
                 if event.key == K_ESCAPE:
                     pygame.quit()
                     sys.exit()

                 elif (event.key == K_LEFT or event.key == K_a):
                     self.player.moveLeft()

                 elif (event.key == K_RIGHT or event.key == K_d):
                     self.player.moveRight()

                 elif (event.key == K_UP or event.key == K_w):
                     self.player.moveUp()

                 elif (event.key == K_DOWN or event.key == K_s):
                     self.player.moveDown()

         return True

    def endScreen(self): #the game's end screen
        self.DISPLAYSURF.blit(self.background, (0, 0))

        self.endText1 = pygame.font.Font(None, 40)
        self.showText1 = self.endText1.render("GAME OVER", 1, TEXTCOLOR)
        self.rect1 = pygame.Rect(225, 180, 25, 25)

        self.endText2 = pygame.font.Font(None, 32)
        self.showText2 = self.endText2.render("Your Score is: %d" %(self.SCORE.score), 1, TEXTCOLOR)
        self.rect2 = pygame.Rect(225, 220, 25, 25)

        self.restartText = pygame.font.Font(None, 24)
        self.showRestart = self.restartText.render("Press Space to play again or Escape to quit", 1, TEXTCOLOR)
        self.restartRect = pygame.Rect(150, 450, 25, 25)

        self.DISPLAYSURF.blit(self.showText1, self.rect1)
        self.DISPLAYSURF.blit(self.showText2, self.rect2)
        self.DISPLAYSURF.blit(self.showRestart, self.restartRect)

        pygame.display.update()

        show = True

        while show == True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == KEYDOWN:
                    if event.key ==K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    elif event.key == K_SPACE:
                        self.dodgeballs.ballList[:] = []
                        main()

    def startScreen(self): #the game's start screen
        self.DISPLAYSURF.blit(self.background, (0, 0))

        self.startText1 = pygame.font.Font(None, 40)
        self.showStart1 = self.startText1.render("DODGEBALL", 1, TEXTCOLOR)
        self.rect1 = pygame.Rect(240, 220, 25, 25)

        self.startText2 = pygame.font.Font(None, 24)
        self.showStart2 = self.startText2.render("Press Space to start", 1, TEXTCOLOR)
        self.rect2 = pygame.Rect(250, 450, 25, 25)

        self.instruct = pygame.font.Font(None, 28)
        self.showInstruct = self.instruct.render("Use the arrow keys to move. Press Escape to quit.", 1, TEXTCOLOR)
        self.instructRect = pygame.Rect(90, 325, 25, 25)

        self.DISPLAYSURF.blit(self.showStart1, self.rect1)
        self.DISPLAYSURF.blit(self.showStart2, self.rect2)
        self.DISPLAYSURF.blit(self.showInstruct, self.instructRect)

        pygame.display.update()

        show = True

        while show == True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    elif event.key == K_SPACE:
                        show = False
                        self.DISPLAYSURF.blit(self.background, (0, 0))
                        pygame.display.update()
                        self.SCORE.lastScoreTime = time.time()
                        return show

def main():
    game = Game()
    game.startScreen()
    game.runGame()
    game.endScreen()

if __name__ == '__main__':
    main()
