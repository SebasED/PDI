# ----------Conceptos básicos de PDI----------------------------
# ----------Por: John Sebastian Estrada Durango. johns.estrada@udea.edu.co CC 1037502955 --------------------------
# -----------Daniel Steve Blandon -----------------------------------
# -----------Curso de Procesamiento Digital de Imágenes ------------------------------------------------------
# ---------- 19 Abril de 2021 --------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------
# 1. IMPORTANDO LAS LIBRERÍAS NECESARIAS
# ------------------------------------------------------------------------------------------------------------

import pygame
import cv2
import random
import numpy as np

# -----------------------------------------------------------------------------------------------------------
# 2. MÉTODOS Y CLASES
# -----------------------------------------------------------------------------------------------------------


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
    
    def shoot(self,x,y):
        bullet = Bullet(self.rect.centerx, self.rect.top,x,y)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(meteor_images)
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

class Explosion(pygame.sprite.Sprite):
	def __init__(self, center):
		super().__init__()
		self.image = explosion_anim[0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 50 # how long to wait for the next frame VELOCITY OF THE EXPLOSION

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(explosion_anim):
				self.kill() # if we get to the end of the animation we don't keep going.
			else:
				center = self.rect.center
				self.image = explosion_anim[self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x0, y0, xf, yf):
        super().__init__()
        self.image = pygame.image.load("assets/laser1.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y0
        self.rect.centerx = x0
        if yf-y0>0:
            self.speedy = 10
        else: self.speedy = -10
        if xf-x0>0:
            self.speedx = 10
        else: self.speedx = -10
        
    
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.bottom < 0 or self.rect.x<0:
            self.kill()

def dibujar(mask, color):
    # Se obtienen los contornos de las imagenes que entren en el rango del color definido
    contornos, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # for para eliminar los contornos que hacen ruido y dejar el que necesitamos

    for c in contornos:
        area = cv2.contourArea(c)  # Encuentra el área del contorno
        if area > 3000:
            M = cv2.moments(c)  # función para encontrar el centro del área
            if (M["m00"] == 0):
                M["m00"] = 1  # se asigna 1 en caso que sea cero para la división
            # Se identifica el punto x del centro del área
            x = int(M["m10"]/M["m00"])
            # Se identifica el punto y del centro del área
            y = int(M["m01"]/M["m00"])
            
            player.rect.centerx = x
            player.rect.centery = y
            # Mejora el contorno, lo suabisa eliminando los picos
            nuevoContorno = cv2.convexHull(c)
            # Se difuba un circulo en el frame con los puntos del centro del área
            cv2.circle(frame, (x, y), 7, (0, 255, 0), -1)
            font = cv2.FONT_HERSHEY_SIMPLEX  # Se asigna una fuente
            cv2.putText(frame, '{},{}'.format(x, y), (x+10, y), font, 0.75,
                        (0, 255, 0), 1, cv2.LINE_AA)  # Se pone un texto en el frame
            cv2.drawContours(frame, [nuevoContorno], 0, (255, 0, 0), 3)

def disparar(mask, color):
    # Se obtienen los contornos de las imagenes que entren en el rango del color definido
    contornos, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # for para eliminar los contornos que hacen ruido y dejar el que necesitamos

    for c in contornos:
        area = cv2.contourArea(c)  # Encuentra el área del contorno
        if area > 3000:
            M = cv2.moments(c)  # función para encontrar el centro del área
            if (M["m00"] == 0):
                M["m00"] = 1  # se asigna 1 en caso que sea cero para la división
            # Se identifica el punto x del centro del área
            x = int(M["m10"]/M["m00"])
            # Se identifica el punto y del centro del área
            y = int(M["m01"]/M["m00"])
            
            player.shoot(x,y)
            # Mejora el contorno, lo suabisa eliminando los picos
            nuevoContorno = cv2.convexHull(c)
            # Se difuba un circulo en el frame con los puntos del centro del área
            cv2.circle(frame, (x, y), 7, (0, 255, 0), -1)
            font = cv2.FONT_HERSHEY_SIMPLEX  # Se asigna una fuente
            cv2.putText(frame, '{},{}'.format(x, y), (x+10, y), font, 0.75,
                        (0, 255, 0), 1, cv2.LINE_AA)  # Se pone un texto en el frame
            cv2.drawContours(frame, [nuevoContorno], 0, (255, 0, 0), 3)

# -----------------------------------------------------------------------------------------------------------
# 3. INICIALIZAR VARIABLES
# -----------------------------------------------------------------------------------------------------------



cap = cv2.VideoCapture(0)  # Captura la imagen de nuestra camara, streaming
WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) # Dimensiones de campo de juego
HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # Dimensiones de campo de juego


BLACK = (0, 0, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()

meteor_images = []
meteor_list = ["assets/meteorGrey_big1.png", "assets/meteorGrey_big2.png", "assets/meteorGrey_big3.png", "assets/meteorGrey_big4.png",
				"assets/meteorGrey_med1.png", "assets/meteorGrey_med2.png", "assets/meteorGrey_small1.png", "assets/meteorGrey_small2.png",
				"assets/meteorGrey_tiny1.png", "assets/meteorGrey_tiny2.png"]
for img in meteor_list:
	meteor_images.append(pygame.image.load(img).convert())

explosion_anim = []
for i in range(9):
	file = "assets/regularExplosion0{}.png".format(i)
	img = pygame.image.load(file).convert()
	img.set_colorkey(BLACK)
	img_scale = pygame.transform.scale(img, (70, 70))
	explosion_anim.append(img_scale)

background = pygame.image.load("assets/background.png").convert()

all_sprites = pygame.sprite.Group()
meteor_list = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
bullets = pygame.sprite.Group()

score = 0

# Rango bajo del color que se desea capturar
azulBajo = np.array([100, 100, 20], np.uint8)
# Rango alto del color que se desea capturar
azulAlto = np.array([125, 255, 255], np.uint8)

# Rangos bajos del color que se desea capturar
redBajo1 = np.array([0, 100, 20], np.uint8)
redAlto1 = np.array([0, 255, 255], np.uint8)
# Rangos altos del color que se desea capturar
redBajo2 = np.array([173, 100, 20], np.uint8)
redAlto2 = np.array([179, 255, 255], np.uint8)

running = True

for i in range(8):
    meteor = Meteor()
    all_sprites.add(meteor)
    meteor_list.add(meteor)

# -----------------------------------------------------------------------------------------------------------
# 3. EJECUCIÓN DEL JUEGO
# -----------------------------------------------------------------------------------------------------------

while running:

    ret, frame = cap.read()
    frame= cv2.flip(frame,1)    
    if ret == True:
        # convierte la imagen (RGB) que captura el frame a formato HSV
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # un frame que captura el color de los rangos estipulados
        mask = cv2.inRange(frameHSV, azulBajo, azulAlto)
        maskRojo_1 = cv2.inRange(frameHSV, redBajo1,redAlto1)
        maskRojo_2 =cv2.inRange(frameHSV, redBajo2, redAlto2)
        maskRojo = cv2.add(maskRojo_1,maskRojo_2)
        # Se llama a la función para mostrar en pantalla
        dibujar(mask, (255, 0, 0))
        # cv2.imshow('maskAzul', mask)# imagen binarizada
        disparar(maskRojo, (0, 0, 255))
        cv2.imshow('frame', frame)  # muestra el frame
        if cv2.waitKey(1) & 0xFF == ord('s'):  # condición para terminar la ejecución
            break
    # Update
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
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        if score == 200:
            running = False
    #Draw / Render
    screen.blit(background, [0, 0])
    all_sprites.draw(screen)

    # Marcador
    draw_text(screen, str(score), 25, WIDTH // 2, 10)

    # *after* drawing everything, flip the display.
    pygame.display.flip()

pygame.quit()
cap.release()
cv2.destroyAllWindows()
