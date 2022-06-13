import pygame
import random

class Ball:
    def __init__(self, screen, windowSize, position):
        self.size = {"width":windowSize[0]/100, "height": windowSize[1]/50}
        self.posX = windowSize[0]/2
        self.posY =  windowSize[1]/2
        if(random.randint(0,1)): self.velX = 5
        else: self.velX = -12
        self.velY = random.randint(-12, 12)
        self.color = 'black'
        self.rect = pygame.Rect(self.posX, self.posY, self.size.get('height'), self.size.get('width'))
        self.hitSound = pygame.mixer.Sound('audio/woosh.wav')
        self.roundWinSound = pygame.mixer.Sound ('audio/roundWin.wav')

    def center(self, screen, windowSize):
        self.posX = windowSize[0]/2
        self.posY =  windowSize[1]/2
        if(random.randint(0,1)): self.velX = 5
        else: self.velX = -5
        self.velY = random.randint(-2, 2)

    def draw(self, screen):
        self.rect = pygame.Rect(self.posX, self.posY, self.size.get('width'), self.size.get('height'))
        pygame.draw.rect(screen, self.color, self.rect)
        
    def move(self, screen, player, opponent, windowSize, points):
        
        if(self.rect.colliderect(player)):
            self.velX = -19
            self.velY = random.randint(-12, 12)
            self.hitSound.play()
            
        if(self.rect.colliderect(opponent)):
            self.velX = 19
            self.velY = random.randint(-12, 12)
            self.hitSound.play()
        
        if(self.rect.bottom >= windowSize[1]  or self.rect.top <= 0):
            self.velY = -self.velY
            self.hitSound.play()
            
        if(self.posX >= windowSize[0]):
            points[1] += 1
            Ball.center(self, screen, windowSize)
            self.roundWinSound.play()
            
        if(self.posX <= 0):
            points [0] += 1
            Ball.center(self, screen, windowSize)
            self.roundWinSound.play()
        
        self.posX += self.velX
        self.posY += self.velY
        
        return(True)
        

class Paddle:
    def __init__(self, screen, windowSize, coordinates, upKey, downKey):
        Ball.__init__(self, screen, windowSize, coordinates)
        self.size.update({"height": windowSize[1]/8})
        self.posX = windowSize[0]/coordinates[0]
        self.posY =  windowSize[1]/coordinates[1]
        self.velY = 18
        self.rect = pygame.Rect(self.posX, self.posY, self.size.get('width'), self.size.get('height'))
        self.upKey = upKey
        self.downKey = downKey
        
    def draw(self, screen):
        Ball.draw(self, screen)
        
    def move(self, screen, pressed, windowSize):
        
        if(pressed[self.upKey] and self.rect.top >= 0):
            self.posY -= self.velY
            
        if(pressed[self.downKey] and self.rect.bottom <= windowSize[1]):
            self.posY += self.velY
            
class Field:
    def __init__ (self, screen, windowSize):
        self.size = {"width":windowSize[0]/200, "height": windowSize[1]}
        self.posX = windowSize[0]/2
        self.posY =  0
        self.color = 'Grey'
        self.rect = pygame.Rect(self.posX, self.posY, self.size.get('width'), self.size.get('height'))
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
            
class Scoreboard:
    def __init__(self, windowSize, points):
        self.font = pygame.font.Font(None, 50) #Sets font for title
        self.player = self.font.render(str(points[0]), False, 'Black') #Creates Pong TItle
        self.opponent = self.font.render(str(points[1]), False, 'Black') #Creates Pong TItle
       
    def draw (self, screen, windowSize, points):
        self.player = self.font.render(str(points[0]), False, 'Black') #Creates Pong TItle
        self.opponent = self.font.render(str(points[1]), False, 'Black') #Creates Pong TItle
        screen.blit(self.player,(windowSize[0]*(8/10), windowSize[1]/5)) #player score
        screen.blit(self.opponent,(windowSize[0]*(1/5), windowSize[1]/5)) #Opponent score
        

def initialize(screen, windowSize, clock, points): #Creates entities upon launch and starts title screen
    
    def entities(screen, windowSize): #Creates Paddles ball and Title Screen texts
    
        ball = Ball(screen, windowSize, (2,2))
        
        opponent = Paddle(screen, windowSize, (10, 2), pygame.K_w , pygame.K_s) #Creates player paddle (Rightside of screen)
        
        player = Paddle(screen, windowSize, (10/9, 2), pygame.K_UP, pygame.K_DOWN) #Creates Opponents Paddle (Leftside of screen)
        
        scoreboard = Scoreboard(windowSize, points)
        
        field = Field(screen, windowSize)
    
        def default():
            
            screen.fill('White')
            
            opponent.draw(screen)
            
            player.draw(screen)
            
            field.draw(screen)
            
            ball.draw(screen)
            
            scoreboard.draw(screen, windowSize, points)
            
        default()
        
        return(player, opponent, ball, scoreboard, field)

    pygame.display.update() #updates and initializes game display
    
    clock.tick(60) #sets maximum framerate to 60
    
    player, opponent, ball, scoreboard, field = entities(screen, windowSize)
    
    return(player, opponent, ball, scoreboard, field)


    