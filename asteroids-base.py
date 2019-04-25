# -*- coding: utf-8 -*-

# Importando as bibliotecas necessárias.
import pygame
from os import path
import random 

# Estabelece a pasta que contem as figuras.
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')
# Dados gerais do jogo.
WIDTH = 480 # Largura da tela
HEIGHT = 600 # Altura da tela
FPS = 60 # Frames por segundo

# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#classe jogador que representa a nave
class Player(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self):
    
        # Costrutor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
    
        # Carregando a imagem de fundo.
        player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
        self.image = player_img
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(player_img, (50, 38))
        
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        #Centraliza embaixo da tela.
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        
        # Velocidade da nave
        self.speedx = 0
        
        #Melhora a colisão estabelecendo um raio de um circulo
        self.radius = 25
        
    #Metodo que atualiza a posição da navinha
    def update(self):
        self.rect.x += self.speedx
        
        #Mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
            
    

# Inicialização do Pygame.
pygame.init()
pygame.mixer.init()

# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome do jogo
pygame.display.set_caption("Asteroids")

#Variavel para o ajuste de velocidade
clock = pygame.time.Clock()

# Carrega o fundo do jogo
background = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()

#Carrega os sons do jogo
pygame.mixe.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)
boom_sound = pygame.mixer.Sound(path.join(snd_dir, 'expl3.wav'))


#Criar uma nave. O construtor será chamado automaticamente
player = Player()

#Criar um grupo de sprites e adiciona a nave
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

class Mob(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self):
    
        # Costrutor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
    
        # Carregando a imagem de fundo.
        player_img = pygame.image.load(path.join(img_dir, "meteorBrown_med1.png")).convert()
        self.image = player_img
        
        # Diminuindo o tamanho da imagem.
        #self.image = pygame.transform.scale(player_img, (50, 38))
        
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        #Centraliza embaixo da tela.
        self.rect.centerx = random.randrange(0, WIDTH)
        self.rect.bottom = random.randrange(-100, -40)
        
        # Velocidade da nave
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(2, 9)
        
        #Melhora a colisão estabelecendo um raio de um circulo
        self.radius = int(self.rect.width * .85 / 2)
        
    #Metodo que atualiza a posição da navinha
    def update (self):
        self.rect.x +=self.speedx
        self.rect.y += self.speedy

mobs = pygame.sprite.Group()

i = 0
while i < 8:        
    #Criar uma nave. O construtor será chamado automaticamente
    mob = Mob()
    #Criar um grupo de sprites e adiciona a nave
    mobs.add(mob)
    all_sprites.add(mob)
    
    i+=1    
    
# Comando para evitar travamentos.
try:
    
    # Loop principal.
    pygame.mixer.music.play(loops=-1)
    running = True
    while running:
        
        #Ajusta a velocidade do jogo.
        clock.tick(FPS)
        
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            
            # Verifica se foi fechado
            if event.type == pygame.QUIT:
                running = False
            
            #Verifica se apertoou alguma tecla.
            if event.type == pygame.KEYDOWN:
                #Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_LEFT:
                    player.speedx = - 8
                if event.key == pygame.K_RIGHT:
                    player.speedx = 8
            
            #Verifica se soltou alguma tecla.
            if event.type == pygame.KEYUP:
                #Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_LEFT:
                    player.speedx = 0
                if event.key == pygame.K_RIGHT:
                    player.speedx = 0
            
        # Depois de processar os eventos.
        # Atualizar a acao de cada sprite.
        all_sprites.update()
        
        #Verifica se houve colisão entre nave e meteoro
        hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
        if hits:
            #Toca o som da colisão
            boom_sound.play()
            time.sleep(1) #Precisa esperar sendo fecha
            
            running = False
                
    
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
        
finally:
    pygame.quit()
