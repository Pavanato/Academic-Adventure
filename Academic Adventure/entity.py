import pygame
from support import import_folder

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, animations={}):
        self.import_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.status = 'idle'
        self.animations = animations['idle'][self.frame_index]
        self.image = self.animations
        self.rect = self.image.get_rect(topleft = pos)

    def import_assets(self):
        images_path = path
        self.animations = animation

        for animation in self.animations.keys():
            full_path = images_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]

    def get_status(self):
        pass

path = 'graphics/character/'
animation = {'idle':[], 'fall':[], 'menino_andando_direita':[], 'menino_andando_esquerda':[], 'run':[], 'jump':[]}

class Player(Entity):
    def __init__(self, pos, animations=animation):
        super().__init__(pos, animations)
        # Player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

        # Player status
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def get_input(self):
        keys = pygame.key.get_pressed()

        # Adding motion controls
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        
        # Adding jump controls (space, up or w)
        if self.on_ground and keys[pygame.K_SPACE]:
            self.jump()
        elif self.on_ground and keys[pygame.K_UP]:
            self.jump()
        elif self.on_ground and keys[pygame.K_w]:
            self.jump()

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x > 0:
                self.status = 'menino_andando_direita'
            elif self.direction.x < 0:
                self.status = 'menino_andando_esquerda'
            else:
                self.status = 'idle'

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()

print(dir(Player))
