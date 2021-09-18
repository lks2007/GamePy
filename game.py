import pygame
import pytmx
import pyscroll
from player import Player
from commerce import Commerce
from coin import Coin
from textCoin import textCoin
import time
import random

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Pygamon - Aventure')
        tmx_data = pytmx.load_pygame("assets/map.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layers = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layers.zoom = 2
        self.map = "world"
        self.visible = False
        self.old_map = "world"

        play_position = tmx_data.get_object_by_name('player')
        with open("position.txt", "r") as f:
            position = f.read()
            if position != "":
                x, y = position.split(",")
                self.player = Player(x, y)
            else:
                self.player = Player(play_position.x, play_position.y)

        commerce_position = tmx_data.get_object_by_name('commerce')
        self.commerce = Commerce(commerce_position.x, commerce_position.y)

        self.walls = []

        for obg in tmx_data.objects:
            if obg.type == "collision":
                self.walls.append(pygame.Rect(obg.x, obg.y, obg.width, obg.height))

        self.group = pyscroll.PyscrollGroup(map_layer=map_layers, default_layer=5)
        self.group.add(self.player)
        self.group.add(self.commerce)

        enter_house = tmx_data.get_object_by_name('enter_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        self.run()

    def switch_house(self, x, y):
        self.old_map = self.map
        tmx_data = pytmx.load_pygame("assets/house2.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layers = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layers.zoom = 2

        self.walls = []

        for obg in tmx_data.objects:
            if obg.type == "collision":
                self.walls.append(pygame.Rect(obg.x, obg.y, obg.width, obg.height))

        chest = tmx_data.get_object_by_name('chest')
        self.chest_rect = pygame.Rect(chest.x, chest.y, chest.width, chest.height)

        self.group = pyscroll.PyscrollGroup(map_layer=map_layers, default_layer=5)
        self.group.add(self.player)

        exit_house = tmx_data.get_object_by_name('exit_house')
        self.enter_house_rect = pygame.Rect(exit_house.x, exit_house.y, exit_house.width, exit_house.height)

        if x == None and y == None:
            spawn_house_point = tmx_data.get_object_by_name('spawn_house')
    
            self.player.position[0] = spawn_house_point.x
            self.player.position[1] = spawn_house_point.y - 20
        else:
            self.player.position[0] = x
            self.player.position[1] = y

        self.player.save_location()
        time.sleep(1)

    def switch_world(self, x, y):
        self.old_map = self.map
        tmx_data = pytmx.load_pygame("assets/map.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layers = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layers.zoom = 2

        self.walls = []

        for obg in tmx_data.objects:
            if obg.type == "collision":
                self.walls.append(pygame.Rect(obg.x, obg.y, obg.width, obg.height))

        self.group = pyscroll.PyscrollGroup(map_layer=map_layers, default_layer=5)
        self.group.add(self.player)
        self.group.add(self.commerce)

        exit_house = tmx_data.get_object_by_name('enter_house')
        self.enter_house_rect = pygame.Rect(exit_house.x, exit_house.y, exit_house.width, exit_house.height)

        if x == None and y == None:  
            spawn_house_point = tmx_data.get_object_by_name('enter_exit_house')

            self.player.position[0] = spawn_house_point.x
            self.player.position[1] = spawn_house_point.y - 20
        else:
            self.player.position[0] = x
            self.player.position[1] = y

        self.player.save_location()
        time.sleep(1)

    def switch_inventory(self):
        tmx_data = pytmx.load_pygame("assets/inventory.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layers = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())

        self.group = pyscroll.PyscrollGroup(map_layer=map_layers, default_layer=1)

        coin = tmx_data.get_object_by_name('coin')
        self.coin_rect = pygame.Rect(coin.x, coin.y, coin.width, coin.height)
        self.coin = Coin(self.coin_rect.x, self.coin_rect.y)
        self.text = textCoin(self.coin_rect.x, self.coin_rect.y)
        self.text.updateNumber()

        self.group.center((0,0))
        self.group.add(self.coin)
        self.group.add(self.text)

        time.sleep(1)

    def update(self):
        self.group.update()

        if (self.map == 'world' and self.player.feet.colliderect(self.enter_house_rect)):
            self.map = 'house'
            self.switch_house(None, None)
            self.old_map = self.map


        if (self.map == 'house' and self.player.feet.colliderect(self.enter_house_rect)):
            self.map = 'world'
            self.switch_world(None, None)
            self.old_map = self.map
        
        if self.e == 1:
            if self.visible == True:
                self.old_map = self.map
                self.switch_inventory()
                self.map = 'inventory'
            else:
                if self.old_map == "world":
                    self.player.position = self.player.old_position
                    self.map = "world"
                    self.switch_world(self.player.old_position[0], self.player.position[1])
                else:
                    self.player.position = self.player.old_position
                    self.map = "house"
                    self.switch_house(self.player.position[0], self.player.position[1])
                    self.old_map = "house"
            
        if self.space == True and self.player.feet.colliderect(self.chest_rect) and (self.map == "world" or self.map == "house"):
            with open("coin.txt", "r+") as f:
                coin = f.read()
                coin = ''.join(x for x in coin if x.isprintable())
                f.truncate(0)

                coin = int(coin)
                coin += random.randint(1, 5)
                f.write(str(coin))
            time.sleep(1)

        for sprite in self.group.sprites():
            if sprite == self.player:
                if sprite.feet.collidelist(self.walls) > -1:
                    sprite.move_back()

    def input_handle(self):
        pressed = pygame.key.get_pressed()

        if self.visible == False:
            if pressed[pygame.K_UP]:
                self.player.move_up()
                self.player.change_animation('up')
            elif pressed[pygame.K_DOWN]:
                self.player.move_down()
                self.player.change_animation('down')
            elif pressed[pygame.K_LEFT]:
                self.player.move_left()
                self.player.change_animation('left')
            elif pressed[pygame.K_RIGHT]:
                self.player.move_right()
                self.player.change_animation('right')
        
        if pressed[pygame.K_e]:
            self.e = 1
            if self.visible == False:
                self.visible = True
            else:
                self.visible = False

        if pressed[pygame.K_e] == 0:
            self.e = 0

        if pressed[pygame.K_SPACE]:
            self.space = 1

        if pressed[pygame.K_SPACE] == 0:
            self.space = 0

    def run(self):
        clock = pygame.time.Clock()

        running = True
        
        while running:
            self.player.save_location()
            self.input_handle()
            if self.visible == False:
                self.screen = pygame.display.set_mode((800, 600))
                self.group.center(self.player.rect.center)
            elif self.visible == True:
                self.screen = pygame.display.set_mode((900, 600))

            self.update()
            self.group.draw(self.screen)
            self.screen.scroll

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    with open('position.txt', 'w') as f:
                        f.truncate(0)
                        f.write(",".join((str(round(self.player.position[0])), str(round(self.player.position[1])))))

                    print("Window close:: NOW")
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                        with open('position.txt', 'w') as f:
                            f.truncate(0)
                            f.write(",".join((str(round(self.player.position[0])), str(round(self.player.position[1])))))

                        print("Window close:: NOW")

            clock.tick(60)

        pygame.quit()