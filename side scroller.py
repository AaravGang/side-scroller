import random
import time

import pygame
from pygame.locals import *

pygame.init()
stime = time.time()
W, H = 800, 447
win = pygame.display.set_mode((W, H))
pygame.display.set_caption("Side Scroller")
run = True
speed = 30
bg = pygame.image.load("static/bg.jpeg")
bgX = 0
bgX2 = bg.get_width()
score = 0
clock = pygame.time.Clock()
obstacles = []
lives = 3


class saw(object):
    images = [
        pygame.image.load("static/SAW0.png"),
        pygame.image.load("static/SAW1.png"),
        pygame.image.load("static/SAW2.png"),
        pygame.image.load("static/SAW3.png"),
    ]
    
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w#
        self.h = h
        self.count = 0
    
    def draw(self):
        if self.count >= 8:
            self.count = 0
        win.blit(
            pygame.transform.scale(self.images[self.count // 2], (64, 64)),
            (self.x, self.y),
        )
        self.count += 1


class wood(saw):
    images = pygame.image.load("static/spike.png")
    
    def draw(self):
        win.blit(self.images, (self.x, self.y))


class player(object):
    run = [pygame.image.load(("static/"+str(x) + ".png")) for x in range(8, 16)]
    jump = [pygame.image.load(("static/"+str(x) + ".png")) for x in range(1, 8)]
    slide = [
        pygame.image.load(("static/S1.png")),
        pygame.image.load(("static/S2.png")),
        pygame.image.load(("static/S2.png")),
        pygame.image.load(("static/S2.png")),
        pygame.image.load(("static/S2.png")),
        pygame.image.load(("static/S2.png")),
        pygame.image.load(("static/S2.png")),
        pygame.image.load(("static/S2.png")),
        pygame.image.load(("static/S3.png")),
        pygame.image.load(("static/S4.png")),
        pygame.image.load(("static/S5.png")),
    ]
    jumpList = [
        1,
        1,
        1,
        1,
        1,
        1,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        4,
        4,
        4,
        4,
        4,
        4,
        4,
        4,
        4,
        4,
        4,
        4,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        -1,
        -1,
        -1,
        -1,
        -1,
        -1,
        -2,
        -2,
        -2,
        -2,
        -2,
        -2,
        -2,
        -2,
        -2,
        -2,
        -2,
        -2,
        -3,
        -3,
        -3,
        -3,
        -3,
        -3,
        -3,
        -3,
        -3,
        -3,
        -3,
        -3,
        -4,
        -4,
        -4,
        -4,
        -4,
        -4,
        -4,
        -4,
        -4,
        -4,
        -4,
        -4,
    ]
    gameOverImg = pygame.image.load("static/0.png")
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.slideUp = False
        self.gameOver = False
    
    def draw(self, win):
        if self.gameOver:
            self.sliding = False
            self.jumping = False
            self.slideCount = 0
            self.jumpCount = 0
            self.runCount = 0
            self.slideUp = False
            while self.y < 340:
                clock.tick(10)
                self.y += 10
                
                win.blit(bg, (bgX, 0))
                win.blit(bg, (bgX2, 0))
                font = pygame.font.Font("freesansbold.ttf", 32)
                
                text = font.render("Game Over", True, (0, 0, 0))
                
                textRect = text.get_rect()
                
                textRect.center = (W // 2, H // 2)
                
                for o in obstacles:
                    o.draw()
                win.blit(text, textRect)
                
                win.blit(self.gameOverImg, (self.x - 10, self.y))
                
                FontForScore = pygame.font.Font("freesansbold.ttf", 22)
                textForScore = FontForScore.render(
                    "Score: %s" % int(score), True, (0, 0, 0)
                )
                textRectForScore = textForScore.get_rect()
                textRectForScore.center = (60, 40)
                win.blit(textForScore, textRectForScore)
                
                pygame.display.update()
        elif self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.2
            win.blit(self.jump[self.jumpCount // 18], (self.x, self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
        elif self.sliding or self.slideUp:
            if self.slideCount < 20:
                self.y += 1
            elif self.slideCount == 80:
                self.y -= 19
                self.sliding = False
                self.slideUp = True
            if self.slideCount >= 110:
                self.slideCount = 0
                self.slideUp = False
                self.runCount = 0
            win.blit(self.slide[self.slideCount // 10], (self.x, self.y))
            self.slideCount += 1
        
        else:
            if self.runCount > 42:
                self.runCount = 0
            win.blit(self.run[self.runCount // 6], (self.x, self.y))
            
            self.runCount += 1


runner = player(400, 317, 64, 64)


def DrawWin():
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgX2, 0))
    
    FontForScore = pygame.font.Font("freesansbold.ttf", 22)
    textForScore = FontForScore.render("Score: %s" % int(score), True, (0, 0, 0))
    textRectForScore = textForScore.get_rect()
    textRectForScore.center = (60, 40)
    win.blit(textForScore, textRectForScore)
    for o in obstacles:
        o.draw()
    
    runner.draw(win)
    pygame.display.update()


def CheckCollision(p1, p2):
    if isinstance(p2, wood):
        ox1 = p2.x - 24
        ox2 = p2.x + 24
        oy1 = 0
        oy2 = 330
    else:
        ox1 = p2.x - 32
        ox2 = p2.x + 32
        oy1 = p2.y - 32
        oy2 = p2.y + 32
    if p1.x >= ox1 and p1.x <= ox2 and p1.y >= oy1 and p1.y <= oy2:
        return True
    else:
        return False


pygame.time.set_timer(USEREVENT + 1, 500)
randtime = pygame.time.set_timer(USEREVENT + 2, random.randint(3000, 5000))

while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == USEREVENT + 1:
            speed += 1
        
        if event.type == USEREVENT + 2:
            randobject = random.randrange(0, 2)
            if randobject == 0:
                obstacles.append(saw(900, 310, 64, 64))
            elif randobject == 1:
                obstacles.append(wood(900, 0, 48, 320))
    
    for o in obstacles:
        
        if CheckCollision(runner, o):
            runner.gameOver = True
            lives -= 1
            DrawWin()
            obstacles.remove(o)
            if lives <= 0:
                win.fill((255, 255, 255))
                fl = pygame.font.Font("freesansbold.ttf", 22)
                tl = fl.render(
                    "Game Over...You have Lost...Click Anywhere On Screen To Exit.",
                    True,
                    (0, 0, 0),
                )
                tlRect = tl.get_rect()
                tlRect.center = (W // 2, H // 2)
                win.blit(tl, tlRect)
                pygame.display.update()
                CompleteGameOver = True
                while CompleteGameOver:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            try:
                                quit()
                            except:
                                pygame.quit()
                                
                                quit()
                        
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            try:
                                quit()
                            except:
                                pygame.quit()
                                
                                quit()
                                # quit()
            
            run = "GameOverEndScreen"
            while run == "GameOverEndScreen":
                pos = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        
                        if (
                                W // 2 - 100 < pos[0] < W // 2 + 100
                                and H // 2 - 100 < pos[1] < H // 2 + 100
                        ):
                            runner.gameOver = False
                            runner.y = 317
                            run = True
                
                win.blit(bg, (bgX, 0))
                win.blit(bg, (bgX2, 0))
                font = pygame.font.Font("freesansbold.ttf", 32)
                
                text = font.render("Click Here To Continue", True, (0, 0, 0))
                fl = pygame.font.Font("freesansbold.ttf", 32)
                tl = fl.render("Lives Left: %s" % lives, True, (0, 255, 255))
                tlRect = tl.get_rect()
                tlRect.center = (W // 2, H // 2 + 50)
                
                textRect = text.get_rect()
                
                textRect.center = (W // 2, H // 2)
                
                for o in obstacles:
                    o.draw()
                win.blit(text, textRect)
                
                win.blit(runner.gameOverImg, (runner.x, runner.y))
                
                FontForScore = pygame.font.Font("freesansbold.ttf", 22)
                textForScore = FontForScore.render(
                    "Score: %s" % int(score), True, (0, 0, 0)
                )
                textRectForScore = textForScore.get_rect()
                textRectForScore.center = (60, 40)
                win.blit(tl, tlRect)
                win.blit(textForScore, textRectForScore)
                
                pygame.display.update()
    
    clock.tick(speed)
    bgX -= 2
    bgX2 -= 2
    score += 0.1
    for o in obstacles:
        if o.x < o.w * -1:
            obstacles.remove(o)
        else:
            o.x -= 2
    
    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()
    keys = pygame.key.get_pressed()
    if keys[K_UP] or keys[K_a]:
        runner.jumping = True
    
    if keys[K_DOWN] or keys[K_l]:
        runner.sliding = True
    
    DrawWin()

pygame.quit()
