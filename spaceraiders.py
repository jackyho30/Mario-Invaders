"""
Author: Jacky Ho

Date: May 31, 2017

Description: Alien invader type game when player is a mario sprite shooting 
fireballs at minions (goombas spinys and shyguys). Game is started when player
presses a key. Once all minions have died a boss bowser is spawned with 7 
lives. The game is won when bowser is killed. Player will have 3 lives and the
game is lost if all 3 are lost. Enemies do notshoot unless if the player makes 
a move so that the player has option to stopplaying in the middle of the game 
and resume when they want to. One fireball fromplayer allowed on the screen at 
the time. One minion bulletbill on the screen at a time. Unlimited number of 
bullet bills from boss Bowser.
"""
# I - IMPORT AND INITIALIZE
import pygame, mySprites, random
pygame.init()
screen = pygame.display.set_mode((640, 480))


def intro():
    '''This function loads up our start screen.'''  
    intro = pygame.image.load("startscreen.png")
    intro = intro.convert()
    screen.blit(intro, (0,0))
    pygame.display.flip()
    
    keepGoing=True
    while keepGoing == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing=False
            elif event.type == pygame.KEYDOWN:
                keepGoing=False
    
                
def main():
    '''This function defines the 'mainline logic' for our invaders game.'''
      
    # DISPLAY
    pygame.display.set_caption("marioinvaders")
     
    # ENTITIES
    background = pygame.image.load("background.png")
    background = background.convert()

 
    # Sprites
    player = mySprites.Spaceship(screen,40,40)
    score_keeper = mySprites.ScoreKeeper()
    alien = mySprites.Aliens(screen,"white.png", 120,0)
    boss = mySprites.Boss(screen)
    boss_wall = mySprites.Walls(screen,"wall2.png",360)
    endzone = mySprites.EndZone(screen)
    aliens= []
    walls =[]
    #create our minions
    for i in range(1):
        aliens.append(mySprites.Aliens(screen,"shyguy.png",75,0+30*i))
        aliens.append(mySprites.Aliens(screen,"spiny.png",100,0+30*i))
        aliens.append(mySprites.Aliens(screen,"goomba.png",125,0+30*i))  
    alien_group= pygame.sprite.Group(aliens)    
    #create 5 defense walls
    for i in range(5):
        walls.append(mySprites.Walls(screen,"wall1.png",98+128*i))
    wall_group = pygame.sprite.Group(walls)
    #boss bullet group
    bg = pygame.sprite.Group() 
    
    allSprites = pygame.sprite.OrderedUpdates(player,score_keeper,aliens,walls,alien)
    
    #music and sounds
    pygame.mixer.music.load("mario_music.mp3")
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1)    
    fireball_sound = pygame.mixer.Sound("fireball.wav")
    kick_sound= pygame.mixer.Sound("kick.wav")
    lose_life_sound=pygame.mixer.Sound("loselife.wav")
    bill_sound=pygame.mixer.Sound("billsound.wav")
    fireball_sound.set_volume(1)    
    kick_sound.set_volume(1)
    lose_life_sound.set_volume(1)
    bill_sound.set_volume(0.6)
# ASSIGN 
    clock = pygame.time.Clock()
    keepGoing = True
    bullet_exists= False
    alien_bullet=False
    boss_alive=False
    boss_round=False
    # Hide the mouse pointer
    pygame.mouse.set_visible(False)
 
    # LOOP
    while keepGoing:
     
        # TIME
        clock.tick(60)
     
        # EVENT HANDLING: Player uses keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.fadeout(3000)
                keepGoing = False
            #check for keys to make player move and shoot
            if event.type == pygame.KEYDOWN:
                #checks if its is minion round or boss round
                #if minion round 1 bullet on screen at time 
                #if boss a bullet is spawned whenever a button is pressed            
                #left
                if event.key == pygame.K_a:
                    player.change_direction((0,1))
                    if alien_bullet==False:
                        bill_sound.play()
                        alien_bullet=True
                        alien_shot= mySprites.AlienShot(screen,"bulletbill.png",random.randint(0,639),alien.rect.bottom)
                        allSprites.add(alien_shot)    
                    if boss_alive==True:
                        bill_sound.play()
                        boss_shot= mySprites.AlienShot(screen,"bulletbill.png",random.randint(boss.rect.left,boss.rect.right),boss.rect.bottom)
                        bg.add(boss_shot)
                        allSprites.add(bg)   
                #right
                if event.key == pygame.K_d:
                    player.change_direction((0,-1))
                    if alien_bullet==False:
                        bill_sound.play()
                        alien_bullet=True
                        alien_shot= mySprites.AlienShot(screen,"bulletbill.png",random.randint(0,639),alien.rect.bottom)
                        allSprites.add(alien_shot)
                    if boss_alive==True:
                        bill_sound.play()
                        boss_shot= mySprites.AlienShot(screen,"bulletbill.png",random.randint(boss.rect.left,boss.rect.right),boss.rect.bottom)
                        bg.add(boss_shot)
                        allSprites.add(bg)
                #shoot
                if event.key == pygame.K_SPACE:
                    if alien_bullet==False:
                        bill_sound.play()
                        alien_bullet=True
                        alien_shot= mySprites.AlienShot(screen,"bulletbill.png",random.randint(0,639),alien.rect.bottom)
                        allSprites.add(alien_shot)    
                    if boss_alive==True:
                        bill_sound.play()
                        boss_shot= mySprites.AlienShot(screen,"bulletbill.png",random.randint(boss.rect.left,boss.rect.right),boss.rect.bottom)
                        bg.add(boss_shot)
                        allSprites.add(bg)       
                #checks if there is a fireball on the screen when space is pressed
                #if not one is created
                if event.key == pygame.K_SPACE and bullet_exists == False:
                    bullet_exists = True
                    fireball_sound.play()
                    shot= mySprites.Shot(screen,"fireball.png",player.rect.centerx)
                    allSprites.add(shot)
                
                    
        #check if our bullet reaches the end of the screen
        if bullet_exists == True:
            if shot.check_bullet()==True:
                shot.kill()
                bullet_exists= False
            # check if our bullet collides with an minion
            if pygame.sprite.spritecollide(shot, alien_group, False) and boss_alive == False:
                bullet_exists = False      
                kick_sound.play()
        
            #if the bullet does our player can shoot again and the bullet will die and
            #give player score
            for index in pygame.sprite.spritecollide(shot, alien_group, True):
                if boss_alive == False:
                    shot.kill()
                    score_keeper.player_scored()
            #check if our bullet collides with our wall group if so our bullet will die
            #and our player can shoot again
            if pygame.sprite.spritecollide(shot, wall_group, False) and boss_alive==False:
                shot.kill()
                bullet_exists = False 
            #check if our bullet collides with the boss wall
            if shot.rect.colliderect(boss_wall.rect):
                shot.kill()
                bullet_exists=False
            if shot.rect.colliderect(boss.rect):
                kick_sound.play()
                shot.kill()
                bullet_exists=False
                score_keeper.boss_lose_life()
        #check if our alien bullet is alive and reaches the end of the screen
        if alien_bullet==True:
            if alien_shot.check_bullet()==True:
                alien_shot.kill()
                alien_bullet=False
            #check if our alien bullet collides with our player if so we lose 1 life
            if alien_shot.rect.colliderect(player.rect):
                lose_life_sound.play()
                alien_bullet = False      
                alien_shot.kill()
                score_keeper.lose_life()
            #check if our alien bulelt collides with our wall group if so the bullet dies
            if pygame.sprite.spritecollide(alien_shot, wall_group, False):
                alien_shot.kill()
                alien_bullet = False 
        #Check if our boss bullet collides with our boss wall or bottom of screen and kills bullet if so
        if pygame.sprite.spritecollide(boss_wall, bg, True):
            continue
        if pygame.sprite.spritecollide(endzone, bg, True):
            continue
        #check if our boss bullet collides with our player if so kills bullet and 
        #player loses life
        for index in pygame.sprite.spritecollide(player, bg, True):
            lose_life_sound.play()
            score_keeper.lose_life()
        #if all aliens die our boss will spawn and a new wall will appear
        if score_keeper.get_aliens()<=0:
            alien_bullet=True
            boss_alive=True
            allSprites.remove(aliens,walls)
            allSprites.add(boss,boss_wall)  
        #if boss loses all lives player wins
        if score_keeper.get_boss_lives()<=0:
            keepGoing = False   
        #if play loses all lives game over
        if score_keeper.get_lives() <= 0:
            keepGoing = False   
             
        # REFRESH SCREEN
        screen.blit(background, (0, 0))
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)       
        pygame.display.flip()
    # Unhide the mouse pointer
    pygame.mouse.set_visible(True)
    # Close the game window
    pygame.time.delay(3000)
    pygame.quit()  
    
#call intro function
intro()
# Call the main function
main()      