import pygame
from sys import exit

class Paddle:
    def __init__(self, windowWidth, windowHeight):
        self.model = pygame.Surface((windowWidth/100,windowHeight/5))
        self.model.fill('Yellow')


def main():
    windowHeight = 400
    windowWidth = 800
    pygame.init() #runs images and plays sounds
    screen = pygame.display.set_mode((windowWidth, windowHeight)) #sets display size
    pygame.display.set_caption('Paddle')
    clock = pygame.time.Clock() #used to set framerate
    
    background_surface = pygame.Surface((windowWidth,windowHeight)) #Creates Background
    background_surface.fill('Blue')

    player = Paddle(windowWidth, windowHeight) #Creates player paddle (Rightside of screen)
    opponent = Paddle(windowWidth, windowHeight) #Creates Opponents Paddle (Leftside of screen)
    
    ball_surface = pygame.Surface((windowWidth*(1/100),windowHeight*(1/50))) #creates ball
    ball_surface.fill('Yellow')    

    title_font = pygame.font.Font(None, 50) #Sets font for title

    title_surface = title_font.render('Paddle', False, 'Yellow') #Creates Pong TItle
    
    player.model.fill('Red')
    
    while True: #loop for running game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()#stops display
                exit() #stops code execution
        
        screen.blit(background_surface,(0,0)) #Displays background
        
        screen.blit(opponent.model,(windowWidth/6, windowHeight/2)) #Displays Player
        
        screen.blit(player.model,(windowWidth*(5/6), windowHeight/4)) #Displays Opponent
        
        screen.blit(ball_surface,(windowWidth*(1/2), windowHeight*(1/2))) #Displays Ball
        
        screen.blit(title_surface,(windowWidth*(1/2)-50, windowHeight*(1/4))) #Displays Title
        
        pygame.display.update() #updates and initializes game display
        clock.tick(60) #sets maximum framerate to 60
        
main()