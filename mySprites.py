import pygame
class Spaceship(pygame.sprite.Sprite):
    '''This class defines the sprite for our player'''
    def __init__(self, screen,width, height):
        '''This initializer takes a screen surface'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        # Define the image attributes for a black square.
        self.image = pygame.image.load("mario1.png")
        self.image = self.image.convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width()/2,screen.get_height()/2)
 
        # position it 60 pixels from the bottom of the screen.
        self.rect.bottom = screen.get_height()-60
 
        # Center the player horizontally in the window.
        self.rect.left = screen.get_width()/2 + 50
        self.__screen = screen
        self.__dx = 0
    def change_direction(self, xy_change):
        '''This method takes a (x,y) tuple as a parameter, extracts the 
        x element from it, and uses this to set the players x direction.'''
        self.__dx = xy_change[1]
         
    def update(self):
        '''This method will be called automatically to reposition the
        player sprite on the screen.'''
        # Check if we have reached the left or right of the screen.
        if ((self.rect.left > 0) and (self.__dx > 0)) or\
           ((self.rect.right < self.__screen.get_width()) and (self.__dx < 0)):
            self.rect.left -= (self.__dx*3)
class Aliens(pygame.sprite.Sprite):
    '''Our Aliens class inherits from the Sprite class'''
    def __init__(self, screen, image, start_top, start_left):
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Set the image and rect attributes for the bricks
        self.image = pygame.image.load(image)
        self.image = self.image.convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.top = start_top
        self.rect.left = start_left
        self.__dx = 1
        self.start_left= start_left
        self.start_top= start_top
        self.__screen = screen

    def update(self):
        '''This method will be called automatically to reposition the
        alien sprite on the screen.'''
        if ((self.rect.left >self.start_left) and (self.__dx < 0)) or\
           ((self.rect.left < self.start_left+100) and (self.__dx > 0)):
            self.rect.left += self.__dx
        else:
            self.__dx = -self.__dx
            if self.rect.top < self.start_top+120:
                self.rect.top+=1

class Shot(pygame.sprite.Sprite):
    def __init__(self, screen,image,start_center):
            '''This initializer takes a screen surface as a parameter, initializes
            the image and rect attributes, and y direction of shot.'''
            # Call the parent __init__() method
            pygame.sprite.Sprite.__init__(self)    
            
            # Define the image attributes for a fireball.
            self.image = pygame.image.load(image)
            self.image = self.image.convert()
            self.image.set_colorkey((255,255,255))
            self.__screen = screen
            self.__dy = -10      
            self.rect = self.image.get_rect()       
            self.rect.centerx = start_center
            self.rect.bottom = self.__screen.get_height()-50
            
            # Instance variables to keep track of the screen surface
            # and set the initial y vector for the shot.
    def check_bullet(self):
        if self.rect.bottom<1:
            return True
        else:
            return False
    
    def update(self):
        if self.rect.bottom > 0:
            self.rect.bottom += self.__dy
class AlienShot(pygame.sprite.Sprite):
    def __init__(self, screen, image,start_center,start_bottom):
            '''This initializer takes a screen surface as a parameter, initializes
            the image and rect attributes, and y direction of shot.'''
            # Call the parent __init__() method
            pygame.sprite.Sprite.__init__(self)    
            
            # Define the image attributes for a bulletbill.
            self.image = pygame.image.load(image)
            self.image = self.image.convert()
            self.image.set_colorkey((255,255,255))
            self.__screen = screen
            self.__dy = 10   
            self.rect = self.image.get_rect()       
            self.rect.centerx = start_center
            self.rect.bottom = start_bottom
            
            # Instance variables to keep track of the screen surface
            # and set the initial y vector for the shot.
    def check_bullet(self):
        if self.rect.bottom>479:
            return True
        else:
            return False
    
    def update(self):
        if self.rect.bottom > 0:
            self.rect.bottom += self.__dy
class ScoreKeeper(pygame.sprite.Sprite):
    '''This class defines a label sprite to display the score.'''
    def __init__(self):
        '''This initializer loads the system font "mariof", and
        sets the starting scores'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Load our custom font, and initialize the starting score.
        self.__font = pygame.font.Font("mariof.ttf", 20)
        self.__player_lives = 3
        self.__aliens = 54
        self.__boss_lives = 7
        
    def player_scored(self):
        '''This method removes one from our minion count'''
        self.__aliens-= 1
    def get_aliens(self):
        '''this method returns our number of minions left on the screen'''
        return self.__aliens     
    
    def lose_life(self):
        '''This method removes one life from player'''
        self.__player_lives-=1   
    def get_lives(self):
        '''returns players number of lives'''
        return self.__player_lives
        
    def boss_lose_life(self):
        self.__boss_lives -= 1
    def get_boss_lives(self):
        return self.__boss_lives
        
 
    def update(self):
        '''This method will be called automatically to display 
        the current score at the top of the game window.'''
        score = "Enemies Remaining: %d Player Lives: %d Boss Lives: %d" %(self.__aliens,self.__player_lives,self.__boss_lives)
        
        
        self.image = self.__font.render(score, 2, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (320, 30)
class Walls(pygame.sprite.Sprite):
    def __init__(self,screen, image, start_x):
        '''This initializer takes a screen surface'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        # Define the image attributes for a black square.
        self.image = pygame.image.load(image)
        self.image = self.image.convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        
        
        self.rect.top = 300
        self.rect.right= start_x
        self.__screen = screen
        self.damage = 7
    def damage_wall(self):
        self.damage -= 1
    def wall_health(self):
        return self.damage


class Boss(pygame.sprite.Sprite):
    '''This class defines the sprite for our Boss.'''
    def __init__(self, screen):
        '''This initializer takes a screen surface as a parameter, initializes
        the image and rect attributes, and x,y direction of the boss.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Set the image and rect attributes for the boss
        self.image = pygame.image.load("bowser.png")
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width()/2,screen.get_height()/2)
 
        # Instance variables to keep track of the screen surface
        # and set the initial x and y vector for the ball.
        self.__screen = screen
        self.__dx = 3
        self.__dy = -3
 
    def change_direction(self):
        '''This method causes the y direction of the ball to reverse.'''
        self.__dy = -self.__dy
             
    def update(self):
        '''This method will be called automatically to reposition the
        ball sprite on the screen.'''
        # Check if we have reached the left or right end of the screen.
        # If not, then keep moving the ball in the same x direction.
        if ((self.rect.left > 0) and (self.__dx < 0)) or\
           ((self.rect.right < self.__screen.get_width()) and (self.__dx > 0)):
            self.rect.left += self.__dx
        # If yes, then reverse the x direction. 
        else:
            self.__dx = -self.__dx
             
        # Check if we have reached the top or bottom of the court.
        # If not, then keep moving the ball in the same y direction.
        if ((self.rect.top > 50) and (self.__dy > 0)) or\
           ((self.rect.bottom < 300) and (self.__dy < 0)):
            self.rect.top -= self.__dy
        # If yes, then reverse the y direction. 
        else:
            self.__dy = -self.__dy  
class EndZone(pygame.sprite.Sprite):
    '''This class defines the sprite for our end zone'''
    def __init__(self, screen):
        '''This initializer takes a screen surface, and y position  as
        parameters.  '''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        # Our endzone sprite will be a 1 pixel wide black line.
        self.image = pygame.Surface((screen.get_width(), 1))
        self.image = self.image.convert()
        self.image.fill((0, 0, 0))
         
        # Set the rect attributes for the endzone
        self.rect = self.image.get_rect()
        self.rect.bottom = 480