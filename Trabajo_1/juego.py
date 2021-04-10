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
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT - 10


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
            player.rect.x = x
            player.rect.y = y
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


WIDTH = 800  # Dimensiones de campo de juego
HEIGHT = 600  # Dimensiones de campo de juego
BLACK = (0, 0, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
background = pygame.image.load("assets/background.png").convert()
all_sprites = pygame.sprite.Group()
meteor_list = pygame.sprite.Group()
player = Player()
score = 0
cap = cv2.VideoCapture(0)  # Captura la imagen de nuestra camara, streaming
# Rango bajo del color que se desea capturar
azulBajo = np.array([100, 100, 20], np.uint8)
# Rango alto del color que se desea capturar
azulAlto = np.array([125, 255, 255], np.uint8)
running = True

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Shooter")

all_sprites.add(player)

for i in range(8):
    meteor = Meteor()
    all_sprites.add(meteor)
    meteor_list.add(meteor)

# -----------------------------------------------------------------------------------------------------------
# 3. EJECUCIÓN DEL JUEGO
# -----------------------------------------------------------------------------------------------------------

while running:

    ret, frame = cap.read()
    if ret == True:
        # convierte la imagen (RGB) que captura el frame a formato HSV
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # un frame que captura el color de los rangos estipulados
        mask = cv2.inRange(frameHSV, azulBajo, azulAlto)
        # Se llama a la función para mostrar en pantalla
        dibujar(mask, (255, 0, 0))
        #cv2.imshow('maskAzul', mask)# imagen binarizada
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
        if score == 5:
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
