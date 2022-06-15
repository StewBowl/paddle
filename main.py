#add title screen
#add four player mode
#add win screen

import pygame
import random
from sys import exit


class Sounds: #Stores all sounds in game
    def __init__(self):
        self.ball_hit = pygame.mixer.Sound('audio/woosh.wav') #when ball hits a surface
        self.round_win = pygame.mixer.Sound ('audio/roundWin.wav') #when ball goes off screen
        self.game_win = pygame.mixer.Sound ('audio/gameWin.wav') #when ball goes off screen 8 times


class Boundry: #Boundry is the line in the middle of the screen that seperates the players fields
    def __init__(self, WINDOW_WIDTH, WINDOW_HEIGHT, screen):
        self.width = WINDOW_WIDTH/300 
        self.height = WINDOW_HEIGHT
        self.position_x = WINDOW_WIDTH/2
        self.position_y = 0
        self.color = 'Grey'
        
        
    def draw(self, screen): #displays boundry
        self.rect = pygame.Rect(self.position_x, self.position_y, self.width, self.height)
        pygame.draw.rect(screen, self.color, self.rect)


class Scoreboard: #displays scores variable
    def __init__(self, WINDOW_WIDTH, WINDOW_HEIGHT, score):
        self.width_player = WINDOW_WIDTH * (8/10)
        self.width_opponent = WINDOW_WIDTH * (1/5)
        self.height = WINDOW_HEIGHT* (4/5)
        self.font = pygame.font.Font(None, int(WINDOW_WIDTH/25)) #Sets font for title
        self.player = self.font.render(str(score[0]), False, 'Black') #Creates Pong TItle
        self.opponent = self.font.render(str(score[1]), False, 'Black') #Creates Pong TItle
        self.color = 'Grey'
       
        
    def draw (self, screen, score): #displays scoreboard
        self.player = self.font.render(str(score[0]), False, self.color) #Creates Pong TItle
        self.opponent = self.font.render(str(score[1]), False, self.color) #Creates Pong TItle
        screen.blit(self.player,(self.width_player, self.height)) #player score
        screen.blit(self.opponent,(self.width_opponent, self.height)) #Opponent score        


class Paddle: #Class of players opponent is rightside of the screen and player is leftside of screen
    def __init__(self, WINDOW_WIDTH, WINDOW_HEIGHT, screen, position_x, position_y, up_key, down_key):
        self.width = WINDOW_WIDTH/200
        self.height = WINDOW_HEIGHT/10
        self.position_x = position_x
        self.position_y = position_y
        self.velocity = WINDOW_HEIGHT/50
        self.color = 'Black'
        self.up_key = up_key
        self.down_key = down_key
        
    def draw(self, screen): #draws paddle
        Boundry.draw(self, screen)

    def move(self, screen, WINDOW_HEIGHT, pressed): #detects when input keys are pressed and shifts paddle
        
        if(pressed[self.up_key] and self.rect.top >= 0): #paddle shift up
            self.position_y -= self.velocity
            
        if(pressed[self.down_key] and self.rect.bottom <= WINDOW_HEIGHT): # paddle shift down
            self.position_y += self.velocity


class Ball: # ball entity starts at middle of field and randomly decides a direction to fling itself
    def __init__(self, WINDOW_WIDTH, WINDOW_HEIGHT, screen):
        self.width = WINDOW_WIDTH/150
        self.height = WINDOW_HEIGHT/75
        self.position_x = WINDOW_WIDTH/2
        self.position_y = WINDOW_HEIGHT/2
        self.velocity_x = WINDOW_WIDTH/230
        self.velocity_y = WINDOW_HEIGHT/180
        self.color = 'Black'
        
    def draw(self, screen): #displays ball
        Boundry.draw(self, screen)
        
    
    def center(self, screen, WINDOW_WIDTH, WINDOW_HEIGHT): #centers ball after score
        self.position_x = WINDOW_WIDTH/2
        self.position_y =  WINDOW_HEIGHT/2
        if random.randint(0,1): self.velocity_x = WINDOW_WIDTH/180 #generates random number to decide if player or opponent recieves ball
        else: self.velocity_x = -WINDOW_WIDTH/180
        self.velocity_y = random.randint(int(-WINDOW_HEIGHT/180), int(WINDOW_HEIGHT/180)) #randomly decided vertical direction of velocity
        Sounds().round_win.play()
    
    def collision(self, WINDOW_WIDTH, WINDOW_HEIGHT): #determines when and what to do upon a collision with player/opponent
        self.velocity_x = -self.velocity_x
        self.velocity_x *= 1.08 #ball accelerates by 8% each time the paddle hits it (this resets when the ball goes off screen)
        self.velocity_y = random.randint(int(-WINDOW_HEIGHT/160), int(WINDOW_HEIGHT/160))
        Sounds().ball_hit.play()
    
    def move(self, screen, WINDOW_WIDTH, WINDOW_HEIGHT, score, player, opponent):
        if self.rect.colliderect(player) or self.rect.colliderect(opponent): #when ball collides with player/opponent
            self.collision(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        if self.rect.bottom >= WINDOW_HEIGHT or self.rect.top <= 0: #when ball collides with ceiling or floor
            self.velocity_y = -self.velocity_y #reverse y velocity of ball
            Sounds().ball_hit.play()
            
        if self.position_x >= WINDOW_WIDTH or self.position_x <= 0: #when ball goes offscreen on the left (opponent scores)
            if self.position_x >= WINDOW_WIDTH:
                score[1] += 1
                self.center(screen, WINDOW_WIDTH, WINDOW_HEIGHT) #returns ball to initial position
                
            if self.position_x <= 0: #when ball goes offscreen on right (player scores)
                score[0] += 1
                self.center(screen, WINDOW_WIDTH, WINDOW_HEIGHT) #returns ball to initial position
            
        self.position_x += self.velocity_x #adds velocity to ball to shift it right/left
        self.position_y += self.velocity_y #add velocity to ball to shift it up/down


def initialize(WINDOW_WIDTH, WINDOW_HEIGHT, screen, clock, score): #sets default position for all entities and returns them to main
    boundry = Boundry(WINDOW_WIDTH, WINDOW_HEIGHT, screen)
    scoreboard = Scoreboard(WINDOW_WIDTH, WINDOW_HEIGHT, score)
    player = Paddle(WINDOW_WIDTH, WINDOW_HEIGHT, screen, WINDOW_WIDTH/20, WINDOW_HEIGHT/2, pygame.K_w , pygame.K_s)
    opponent = Paddle(WINDOW_WIDTH, WINDOW_HEIGHT, screen, WINDOW_WIDTH*(19/20), WINDOW_HEIGHT/3, pygame.K_UP, pygame.K_DOWN)
    ball = Ball(WINDOW_WIDTH, WINDOW_HEIGHT, screen)
    display(screen, clock, score, boundry, scoreboard, player, opponent, ball)
    return boundry, scoreboard, player, opponent, ball
    

def display(screen, clock, score, boundry, scoreboard, player, opponent, ball): #updates display
    screen.fill('White')
    boundry.draw(screen)
    player.draw(screen)
    opponent.draw(screen)
    ball.draw(screen)
    scoreboard.draw(screen, score)
    pygame.display.update() #updates and initializes game display
    clock.tick(60) #sets maximum framerate to 60


def main():
    pygame.init() #initializes all pygame modules
    WINDOW_DIMENSIONS = (1600, 800) #default values are 1600, 800
    SCALED_WIDTH = (WINDOW_DIMENSIONS[0]/1600)*1600#used to scale resolution when changed from default values
    SCALED_HEIGHT = (WINDOW_DIMENSIONS[1]/800)*800
    
    screen = pygame.display.set_mode(WINDOW_DIMENSIONS) #creates screen
    clock = pygame.time.Clock() #creates frane clock
    active = True #activates game loop
    win = False #used to continue/stop the games progression
    score = [0,0]
    
    boundry, scoreboard, player, opponent, ball = initialize(SCALED_WIDTH, SCALED_HEIGHT, screen, clock, score) #creates objects
    
    while active: #loop for running game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()#stops display
                exit() #stops code executions
                
            if win == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: #Waits for space to be pressed to continue
                        score = [0,0]
                        win = False
                
        if win == False:
            pressed = pygame.key.get_pressed() #stores pressed inputs
            
            player.move(screen, SCALED_HEIGHT, pressed) #inputs are sent for player movement
            opponent.move(screen, SCALED_HEIGHT, pressed) #inputs are sent for opponent movement
            ball.move(screen, SCALED_WIDTH, SCALED_HEIGHT, score, player, opponent) #updates ball's position
            
            display(screen, clock, score, boundry, scoreboard, player, opponent, ball) # updates display
            
            if score[0] > 7 or score[1] > 7: #checks if a players' score has exceeded 7 to end round
                win = True
                pygame.mixer.stop() #stops sounds to clear audio for game_win
                Sounds().game_win.play()
                
                
main()