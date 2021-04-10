import cv2
import numpy as np
import pygame
import random

cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
kernel= np.ones((15,15), np.uint8)

WIDTH = 800
HEIGHT = 600

BLACK = (0, 0, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()
global x ,y
x = WIDTH // 2
y = HEIGHT - 10

def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/player.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10

    def update(self):
        self.rect.x = x
        self.rect.y = y


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/meteorGrey_med1.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 22:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


# Cargar fondo.
background = pygame.image.load("assets/background.png").convert()


all_sprites = pygame.sprite.Group()
meteor_list = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

score = 0
for i in range(8):
    meteor = Meteor()
    all_sprites.add(meteor)
    meteor_list.add(meteor)


# Game Loop
running = True
while running:
    check, frame= cap.read()                    #Lee lo que hay en cap, que es la captura del video de la cámara web 
    frame1= cv2.flip(frame,1)                    #Crea un efecto espejo
    a= frame1[:,:,1]                             #Se extrae la componente azul de la imagen
    a= cv2.subtract(a,cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY )) #Se resta la componente azul con la imagen del frame pero en escala de grises
    
    
    ret,a= cv2.threshold(a,30,255,cv2.THRESH_BINARY) #Con la función Threshold se binariza para que solo se vean los objetos azules
    a=cv2.blur(a,(2,2))                           #Se difumina la imagen para que se tome el objeto azul con más claridad
    a=cv2.dilate(a,kernel,iterations=1)           #Se realiza una dilatación para que la imagen se vea mas grande y definida
    a=cv2.Canny(a,100,150)                        #Se obtiene el contorno del objeto azul en pantalla
  
    borders, cnts= cv2.findContours(a.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #Se toma la posición del objeto en la pantalla y se guarda en una matriz de matrices.
    x=0
    y=0
    for b in borders:
        area = cv2.contourArea(b)
        M =cv2.moments(b)
        if(M["m00"]==0):
            M["m00"]=1
        x=int(M["m10"]/M["m00"])
        y=int(M["m01"]/M["m00"])
        
                                
        cv2.circle(frame1,(x,y),7,(0,255,0),-1)
        font =cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame1,'{},{}'.format(x,y),(x+10,y),font,0.75,(0,255,0),1,cv2.LINE_AA)
        nuevocontorno=cv2.convexHull(b)
        cv2.drawContours(frame, [nuevocontorno],0,(255,0,0),3)
    cv2.imshow('frame',frame1)
    cv2.imshow('a',a)
    # Keep loop running at the right speed
    clock.tick(60)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    hits = pygame.sprite.spritecollide(player, meteor_list, True)
    for hit in hits:
        score += 1
        if score == 3:
            running = False
    #Draw / Render
    screen.blit(background, [0, 0])
    all_sprites.draw(screen)

    # Marcador
    draw_text(screen, str(score), 25, WIDTH // 2, 10)

    # *after* drawing everything, flip the display.
    pygame.display.flip()

cap.release()
cv2.destroyAllWindows()
pygame.quit()
