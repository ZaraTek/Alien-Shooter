import pygame
import random
import pygame.mixer
import pygame.font

# Initialize pygame
pygame.init()
pygame.mixer.init()
pygame.font.init()

# Create Screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Alien Shooter")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Font and Sounds
font = pygame.font.Font("space_invaders.ttf", 24)
shootSound = pygame.mixer.Sound("shoot_sound.wav")
hitSound = pygame.mixer.Sound("hit.wav")
explosionSound = pygame.mixer.Sound("explosion.wav")
levelUpSound = pygame.mixer.Sound("level_up.wav")
pygame.mixer.music.load("music.wav")
pygame.mixer.music.play(-1)


# Player
playerImg = pygame.image.load('spaceship.png')
playerImg = pygame.transform.scale(playerImg, (45, 45))
playerX = 370
playerY = 480
moveLeft = False
moveRight = False
health = 100
score = 0
playerSpeed = 0.2
levelUpRequirement = 20

def player(x, y):
    screen.blit(playerImg, (x, y))


# Shooting
bulletImg = pygame.image.load('bullet.png')
bulletImg = pygame.transform.scale(bulletImg, (25, 25))
bulletX = playerX + 10
bulletY = playerY - 50
bullets = []

def shoot(x, y):
    bullets.append({"x": x, "y": y})
    shootSound.play()
    

# Aliens
alienImg = pygame.image.load('alien.png')
alienImg = pygame.transform.scale(alienImg, (50, 40))
aliens = []
alienSpeed = 0.1

def spawn(): 
    if len(aliens) < 999999:
        x = random.randint(100, 700)
        y = random.randint(50, 150)
        aliens.append({"x": x, "y": y})

SPAWN_ALIEN_EVENT = pygame.USEREVENT + 1
alienSpawnTime = 2000.0
pygame.time.set_timer(SPAWN_ALIEN_EVENT, int(alienSpawnTime))


# Collision Detector
def collision(bulletX, bulletY, alienX, alienY):
    bulletRect = bulletImg.get_rect()
    bulletRect.x = bulletX
    bulletRect.y = bulletY
    alienRect = alienImg.get_rect()
    alienRect.x = alienX
    alienRect.y = alienY
    
    return bulletRect.colliderect(alienRect)


# Level Up
level = 1
leveledUp = False
def levelUp():
    global alienSpeed, leveledUp, level, alienSpawnTime, levelUpText, levelUpSurface, playerSpeed
    alienSpeed += 0.005
    alienSpawnTime *= 0.9
    playerSpeed += 0.02
    pygame.time.set_timer(SPAWN_ALIEN_EVENT, int(alienSpawnTime))
    leveledUp = True;
    level += 1
    levelUpSound.play()
    

# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))
    healthText = "Health: " + str(health)
    healthSurface = font.render(healthText, True, (255, 255, 255))
    screen.blit(healthSurface, (10, 10))

    scoreText = "Score: " + str(score)
    scoreSurface = font.render(scoreText, True, (255, 255, 255))
    screen.blit(scoreSurface, (10, 40))

    levelUpText = "Level: " + str(level)
    levelUpSurface = font.render(levelUpText, True, (255, 255, 255))
    screen.blit(levelUpSurface, (670, 10))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moveLeft = True
            if event.key == pygame.K_RIGHT:
                moveRight = True

            if event.key == pygame.K_SPACE:
                shoot(playerX+10, playerY-50)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moveLeft = False
            if event.key == pygame.K_RIGHT:
                moveRight = False

        if event.type == SPAWN_ALIEN_EVENT:
            spawn()

    if moveLeft:
        playerX -= playerSpeed
    if moveRight:
        playerX += playerSpeed

    if score != 0 and score % 20 == 0 and leveledUp == False:
        levelUp()
    if score % 20 != 0:
        leveledUp = False

    # Update bullet positions
    for bullet in bullets:
        bullet["y"] -= 0.3  # Adjust the bullet speed here

    # Draw bullets
    for bullet in bullets:
        screen.blit(bulletImg, (bullet["x"], bullet["y"]))

    # Remove bullets that have gone off the screen
    bullets = [bullet for bullet in bullets if bullet["y"] > 0]
    
    # Draw Aliens
    for alien in aliens:
        screen.blit(alienImg, (alien["x"], alien["y"]))
        alien["y"] += alienSpeed

        # Check Collision
        for bullet in bullets:
            if collision(bullet["x"], bullet["y"], alien["x"], alien["y"]):
                bullets.remove(bullet)
                aliens.remove(alien)
                score += 10
        
        # Check Invasion
        if alien["y"] >= 480:
            health -= 10
            aliens.remove(alien)
            hitSound.play()


    player(playerX, playerY)
    pygame.display.update()

pygame.quit()
