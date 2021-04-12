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
# 2. FUNCIONES Y CLASES
# -----------------------------------------------------------------------------------------------------------

# Función para escribir texto en la pantalla en unas cordenadas dadas
def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# Clase que representa nuestro jugagor
class Player(pygame.sprite.Sprite):
    # Método para inicar la clase Player
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/player.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10

    # Método para disparar
    def shoot(self, x, y):
        bullet = Bullet(self.rect.centerx, self.rect.top, x, y)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Clase que representa los meteoritos
class Meteor(pygame.sprite.Sprite):
    # Método cpara iniciar la clase Meteor
    def __init__(self):
        super().__init__()
        self.image = random.choice(meteor_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)

    # Método para actualizar las posiciones de los meteoritos
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 22:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

# Clase que representa la explosión entre los diferentes choques
class Explosion(pygame.sprite.Sprite):
    # Método cpara iniciar la clase Explosion
    def __init__(self, center):
        super().__init__()
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    # Método para actulizar y eliminar las explosiones generadas
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

# Clase que representa las balas que lanzara la nave
class Bullet(pygame.sprite.Sprite):
    # Método cpara iniciar la clase Bullet, de donde y hacia donde debe ir
    def __init__(self, x0, y0, xf, yf):
        super().__init__()
        self.image = pygame.image.load("assets/laser1.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y0
        self.rect.centerx = x0
        if yf == y0:
            self.speedy = 0
        elif yf-y0 > 0:
            self.speedy = 10
        else:
            self.speedy = -10
        if xf == x0:
            self.speedx = 0
        elif xf-x0 > 0:
            self.speedx = 10
        else:
            self.speedx = -10

    # Método para modificar la trayectoria de la bala y eliminar cuando salgan de la pantalla
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.bottom < 0 or self.rect.x < 0:
            self.kill()

# Método para dibujar en un frame las mascaras de los colores detectados
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
            # Indicar si el color es azul para llevarle las posiciones del centro del área al Player
            if color == (255, 0, 0):
                player.rect.centerx = x
                player.rect.centery = y
            else:  # Si es otro color, se pasan las posiciones a donde deben ir las balas
                player.shoot(x, y)
            # Mejora el contorno, lo suabisa eliminando los picos
            nuevoContorno = cv2.convexHull(c)
            # Se dibuja un circulo en el frame con los puntos del centro del área
            cv2.circle(frame, (x, y), 7, (0, 255, 0), -1)
            font = cv2.FONT_HERSHEY_SIMPLEX  # Se asigna una fuente
            cv2.putText(frame, '{},{}'.format(x, y), (x+10, y), font, 0.75,
                        (0, 255, 0), 1, cv2.LINE_AA)  # Se pone un texto en el frame
            # Dibujar el contorno de los objetos capturados en el frame
            cv2.drawContours(frame, [nuevoContorno], 0, color, 3)

# Método de la pantalla principal con las instrucciones del juego


def show_go_screen():
    screen.blit(background, [0, 0])  # Pone una imagen de fondo
    draw_text(screen, "SPACE GAME", 65, WIDTH // 2,
              HEIGHT / 4)  # Dibuja el nombre del juego
    draw_text(screen, "La nave seguira el movimiento de un objeto azul",
              20, WIDTH // 2, HEIGHT // 2)  # Instrucción del juego
    draw_text(screen, "Dispara poniendo otro objeto de color rojo en pantalla ",
              20, WIDTH // 2, (HEIGHT // 2)+20)  # Instrucción del juego
    draw_text(screen, "Si te impactan 10 meteoritos pierdes el juego  ",
              20, WIDTH // 2, (HEIGHT // 2)+40)  # Instrucción del juego
    draw_text(screen, "Preiona una tecla para iniciar", 17,
              WIDTH // 2, HEIGHT * 3/4)  # Instrucción del juego
    pygame.display.flip()  # Inicia la pantalla para el juego
    waiting = True
    while waiting:  # ciclo para permanecer en la pantalla de inicio
        clock.tick(60)
        for event in pygame.event.get():  # Capturar los eventos del sistema
            if event.type == pygame.QUIT:  # Condición para salir del juego
                pygame.quit()
                cap.release()
                cv2.destroyAllWindows()
            if event.type == pygame.KEYUP:  # Condición para iniciar del juego
                waiting = False
# -----------------------------------------------------------------------------------------------------------
# 3. INICIALIZAR VARIABLES
# -----------------------------------------------------------------------------------------------------------


# Captura la imagen de nuestra camara, streaming
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # Dimensiones de campo de juego
# Dimensiones de campo de juego
HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
BLACK = (0, 0, 0)  # Definir un color

pygame.init()  # Iniciar la librería paygame para el juego
pygame.mixer.init()  # Iniciar la librería paygame para el juego
# Pasar dimensiones a la pantalla donde se mostrará el juego
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Mostrar nombre del juego en la pantalla
pygame.display.set_caption("SPACE GAME")
# clock que controlara las velocidades a las que se moveran los objetos en el juego
clock = pygame.time.Clock()

meteor_images = []
meteor_list = ["assets/meteorGrey_big1.png", "assets/meteorGrey_big2.png", "assets/meteorGrey_big3.png", "assets/meteorGrey_big4.png",
               "assets/meteorGrey_med1.png", "assets/meteorGrey_med2.png", "assets/meteorGrey_small1.png", "assets/meteorGrey_small2.png",
               "assets/meteorGrey_tiny1.png", "assets/meteorGrey_tiny2.png"]  # Lista de los meteoritos que usaremos en el juego
for img in meteor_list:  # Agregar todos los meteoritos a meteor_images y convertirlos para poder usarlos
    meteor_images.append(pygame.image.load(img).convert())

explosion_anim = []
for i in range(9):  # Agregar las imagenes que representan las explosiones
    file = "assets/regularExplosion0{}.png".format(i)
    img = pygame.image.load(file).convert()
    img.set_colorkey(BLACK)
    img_scale = pygame.transform.scale(img, (70, 70))
    explosion_anim.append(img_scale)

# Asignar una imagen al fondo de pantalla
background = pygame.image.load("assets/background.png").convert()

# Rango bajo del color amarillo
amarilloBajo = np.array([15, 100, 20], np.uint8)
# Rango alto del color amarillo
amarilloAlto = np.array([45, 255, 255], np.uint8)
azulBajo = np.array([100, 100, 20], np.uint8)  # Rango bajo del color azul
azulAlto = np.array([125, 255, 255], np.uint8)  # Rango alto del color azul
# redBajo1 = np.array([0, 100, 20], np.uint8)# Rangos bajos del color que se desea capturar
# redAlto1 = np.array([0, 255, 255], np.uint8)# Rangos altos del color que se desea capturar
# redBajo2 = np.array([173, 100, 20], np.uint8)# Rangos bajos del color que se desea capturar
# redAlto2 = np.array([179, 255, 255], np.uint8)# Rangos altos del color que se desea capturar

game_over = True  # Variable para controlar el fin y el inicio del juego
running = True  # Variable para definir cuando el juego este corriendo

# -----------------------------------------------------------------------------------------------------------
# 3. EJECUCIÓN DEL JUEGO
# -----------------------------------------------------------------------------------------------------------

while running:  # ciclo principal del juego

    ret, frame = cap.read()  # Capturar la imagen de la camara
    # Función espejo para los movimientos se tomen acordes a los que hace el jugador frente a la camara
    frame = cv2.flip(frame, 1)
    if ret == True:  # Cerificar que se este capturando una imagen
        # convierte la imagen (RGB) que captura el frame a formato HSV
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Determinar el rango para el colore azul, imagen binarizada
        maskAzul = cv2.inRange(frameHSV, azulBajo, azulAlto)
        # Determinar el rango para el colore amarillo, imagen binarizada
        maskAmarillo = cv2.inRange(frameHSV, amarilloBajo, amarilloAlto)
        # maskRojo_1 = cv2.inRange(frameHSV, redBajo1,redAlto1)# Determinar el primer rango para el colore rojo
        # maskRojo_2 =cv2.inRange(frameHSV, redBajo2, redAlto2)# Determinar el segundo rango para el colore rojo
        # maskRojo = cv2.add(maskRojo_1,maskRojo_2)# Determinar el rango para el color rojo, imagen binarizada
        # función para mostrar en pantalla lo que captura la camara en el rango y color determinado
        dibujar(maskAzul, (255, 0, 0))
        # función para mostrar en pantalla lo que captura la camara en el rango y color determinado
        dibujar(maskAmarillo, (0, 255, 255))
        # dibujar(maskRojo, (0, 0, 255))# función para mostrar en pantalla lo que captura la camara en el rango y color determinado
        # cv2.imshow('maskAzul', mask)# Mostrar imagen binarizada
        cv2.imshow('frame', frame)  # mostrar el frame
        if cv2.waitKey(1) & 0xFF == ord('s'):  # condición para terminar la ejecución
            break

    if game_over:  # Condición para la ventana de inicio
        show_go_screen()  # Llamar a la función para iniciar el juego o terminarlo
        game_over = False
        # Lista para guardar todos los objetos del juego
        all_sprites = pygame.sprite.Group()
        meteor_list = pygame.sprite.Group()  # Lista para guardar los meteoritos de juego
        bullets = pygame.sprite.Group()  # Lista para guardar las balas de juego
        player = Player()  # instanciar un Player
        # Agregar el Player a la lista de sprites y objetos
        all_sprites.add(player)

        for i in range(8):  # Crear los meteoritos y a gregarlos a las listas correpondietnes
            meteor = Meteor()
            all_sprites.add(meteor)
            meteor_list.add(meteor)

        score = 10  # Valor en que iniciara el score

    clock.tick(60)
    for event in pygame.event.get():  # Capturar los eventos
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()  # Actualizar todos los sprites u objetos del juego

    # Capturar las colisiones entre metoritos y las balas
    hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
    for hit in hits:  # Instanciar las explosiones de acuerdo a los choques entre meteoritos y balas
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        meteor = Meteor()  # Crea los meteoritos que fueron destruidos
        all_sprites.add(meteor)
        meteor_list.add(meteor)

    # Capturar las colisiones entre metoritos y la nave
    hits = pygame.sprite.spritecollide(player, meteor_list, True)
    for hit in hits:  # Recorre las colisiones
        score -= 1  # Resta un punto al score
        meteor = Meteor()  # Crea el meteorito destruido por el choque
        all_sprites.add(meteor)
        meteor_list.add(meteor)
        # Crea la explosión que genera el impacto
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        if score == 0:  # Condición para saber si se acabaron las vidas y el juego inica o termina
            game_over = True

    # Dibuja el fondo de pantalla en las cordenadas [0,0]
    screen.blit(background, [0, 0])
    all_sprites.draw(screen)  # Dibuja todos los sprites u objetos
    # Dibuja el score en pantalla
    draw_text(screen, str(score), 25, WIDTH // 2, 10)
    pygame.display.flip()  # muestra los cambios actualizados

pygame.quit()  # Finaliza el pygame
cap.release()
cv2.destroyAllWindows()  # Finaliza y termina todas las ventanas
