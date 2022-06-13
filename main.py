import pygame
import entities
from sys import exit


def main():
    pygame.init() #runs images and plays sounds
    windowSize = (1600, 800)
    screen = pygame.display.set_mode(windowSize) #sets display size
    pygame.display.set_caption('Paddle')
    clock = pygame.time.Clock() #used to set framerate
    points = [0,0]
    player, opponent, ball, scoreboard, field= entities.initialize(screen, windowSize, clock, points)
    ongoing = True
    active = True
    gameWinSound = pygame.mixer.Sound ('audio/gameWin.wav')
    
    while(active): #loop for running game
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()#stops display
                exit() #stops code executions
            if(ongoing == False):
                if(event.type == pygame.KEYDOWN):
                    if(event.key == pygame.K_SPACE):
                        ongoing = True
                
        if(ongoing == False):   
            if(points[0] > 7):
                points = [0,0]
                player, opponewent, ball, scoreboard, field = entities.initialize(screen, windowSize, clock, points)

                
            if(points[1] > 7):
                points = [0,0]
                player, opponent, ball, scoreboard, field = entities.initialize(screen, windowSize, clock, points)
                
        
        if(ongoing == True):
            pressed = pygame.key.get_pressed()
                    
            player.move(screen, pressed, windowSize)
                   
            opponent.move(screen, pressed, windowSize)
                
            ball.move(screen, player, opponent, windowSize, points)
            
            screen.fill("White")
            
            player.draw(screen)
            
            opponent.draw(screen)
            
            field.draw(screen)
            
            ball.draw(screen)
            
            scoreboard.draw(screen, windowSize, points)
            
            if(points[0] > 7 or points[1] > 7):
                pygame.mixer.stop()
                gameWinSound.play()
                ongoing = False

            pygame.display.update() #updates and initializes game display
            clock.tick(60) #sets maximum framerate to 60
        
main()