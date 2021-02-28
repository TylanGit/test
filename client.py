# Stop Imports
if __name__ == "__main__":
    # Imports
    import pygame
    import pickle
    import threading
    import sys
    import os
    from inputs import Button
    from inputs import GetInputs
    from inputs import IpAddressInput
    from inputs import PortInput
    from network import Client
    # Pygame Setup
    screen_width = 1280
    screen_height = 700
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Shooty Arena")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 12)
    text = font.render("", False, (0, 0, 0))
    # Variables
    menu_main = True
    menu_online = False
    menu_offline = False
    menu_custom = False
    menu_settings = False
    online = False
    offline = False
    custom = False
    ip_address_input = None
    port_input = None
    ip_address = None
    port = None
    network = None
    facing = 1
    # Load Images
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    cave_image_menu_background_url = resource_path("backgrounds\\background_menu.png")
    cave_image_menu_background = pygame.image.load(cave_image_menu_background_url).convert()
    cave_image_game_background_url = resource_path("backgrounds\\background_cave.png")
    cave_image_game_background = pygame.image.load(cave_image_game_background_url).convert()
    cave_image_dirt_url = resource_path("blocks\\dirt_cave.png")
    cave_image_dirt = pygame.image.load(cave_image_dirt_url).convert()
    cave_image_block_url = resource_path("blocks\\block_cave.png")
    cave_image_block = pygame.image.load(cave_image_block_url).convert()
    cave_image_player_url = resource_path("players\\player.png")
    cave_image_player = pygame.image.load(cave_image_player_url).convert()
    cave_image_player_flipped = pygame.transform.flip(cave_image_player, True, False).convert()
    cave_image_online_url = resource_path("buttons\\online.png")
    cave_image_online = pygame.image.load(cave_image_online_url).convert()
    cave_image_survival_url = resource_path("buttons\\survival.png")
    cave_image_survival = pygame.image.load(cave_image_survival_url).convert()
    cave_image_menu_url = resource_path("buttons\\menu.png")
    cave_image_menu = pygame.image.load(cave_image_menu_url).convert()
    cave_image_ip_address_url = resource_path("buttons\\ipaddress.png")
    cave_image_ip_address = pygame.image.load(cave_image_ip_address_url).convert_alpha()
    cave_image_port_url = resource_path("buttons\\port.png")
    cave_image_port = pygame.image.load(cave_image_port_url).convert_alpha()
    # Create Buttons
    cave_button_online = Button(screen, cave_image_online, 480, 450)
    cave_button_survival = Button(screen, cave_image_survival, 700, 450)
    cave_button_menu = Button(screen, cave_image_menu, 1150, 30)
    cave_button_ip_address = Button(screen, cave_image_ip_address, 5, 5)
    cave_button_port = Button(screen, cave_image_port, 50, 50)
    # Create Input Fields
    input_ip_address = IpAddressInput()
    input_port = PortInput()
    # Generate World Data
    pickle_in_url = resource_path("leveldata\\level_data.txt")
    pickle_in = open(pickle_in_url, "rb")
    tile_list = pickle.load(pickle_in)
    world_data = []
    tile_size = 20
    row_count = 0
    for row in tile_list:
        column_count = 0
        for tile in row:
            # Dirt
            if tile == 1:
                block = cave_image_dirt
                tile = pygame.transform.scale(block, (tile_size, tile_size))
                tile_rect = tile.get_rect()
                tile_rect.y = row_count * tile_size
                tile_rect.x = column_count * tile_size
                tile = (tile, tile_rect)
                world_data.append(tile)
            # Down
            if tile == 2:
                block = cave_image_block
                tile = pygame.transform.scale(block, (tile_size, tile_size))
                tile_rect = tile.get_rect()
                tile_rect.y = row_count * tile_size
                tile_rect.x = column_count * tile_size
                tile = (tile, tile_rect)
                world_data.append(tile)
            # Left
            if tile == 3:
                block = cave_image_block
                block = pygame.transform.rotate(block, 270)
                tile = pygame.transform.scale(block, (tile_size, tile_size))
                tile_rect = tile.get_rect()
                tile_rect.y = row_count * tile_size
                tile_rect.x = column_count * tile_size
                tile = (tile, tile_rect)
                world_data.append(tile)
            # Right
            if tile == 4:
                block = cave_image_block
                block = pygame.transform.rotate(block, 90)
                tile = pygame.transform.scale(block, (20,20))
                tile_rect = tile.get_rect()
                tile_rect.y = row_count * tile_size
                tile_rect.x = column_count * tile_size
                tile = (tile, tile_rect)
                world_data.append(tile)
            column_count+=1
        row_count+=1
    # Bullet Class
    class Bullet(object):
        # Init
        def __init__(self, x, y, radius, color, facing):
            self.x = x
            self.y = y
            self.radius = radius
            self.color = color
            self.facing = facing
            self.vel = 20 * facing
        # Draw
        def draw(self, screen):
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
    # Game Loop
    run = True
    pygame.font.init()
    pygame.init()
    font = pygame.font.SysFont("../fonts/Blocky.tff", 40)
    while run:
        # Tick
        clock.tick(60)
        # Main Menu
        if menu_main:
            # Background
            screen.blit(cave_image_menu_background, (0, 0))
            # Online Button
            if cave_button_online.draw():
                try:
                    port = int(9306)
                    ip_address = "192.168.1.42"
                    network = Client(ip_address, port)
                    message = network.receive_string()
                    if message == "!JOIN":
                        text = font.render("", True, (255, 255, 0))
                        menu_main = False
                        menu_online = True
                    elif message == "!FULL":
                        text = font.render("Server Full", True, (255, 255, 0))
                except:
                    text = font.render("Server Not Found", True, (255, 255, 0))
            # Survival Button
            if cave_button_survival.draw():
                pass
            # Print Text
            screen.blit(text, (530, 550))
        # Online Menu
        if menu_online:
            menu_online = False
            online = True
        # Online Game
        if online:
            # Background
            screen.blit(cave_image_game_background, (0, 0))
            # World
            for tile in world_data:
                screen.blit(tile[0], (tile[1].x, tile[1].y - 20))
            # Menu Button
            if cave_button_menu.draw():
                network.send_string("!DISSCONNECT")
                text = font.render("", True, (255, 255, 0))
                online = False
                menu_main = True
        if online:
            # Send Inputs To Server
            up, left, right, mouse_position, facing = GetInputs(facing)
            network.send_string(f"{up}@{left}@{right}@{mouse_position}@{pygame.mouse.get_pressed()}@{facing}")
            # Receive Inputs
            response = network.receive_string()
            all_bullets = network.receive_byte()
            score = network.receive_string()
            facings = network.receive_string()
            response = response.replace("[","")
            response = response.replace("]","")
            response = response.replace(" ","")
            response = response.split(",")
            facings = facings.replace("[","")
            facings = facings.replace("]","")
            facings = facings.replace(" ","")
            facings = facings.split(",")
            # Player Coordinates
            onex = int(response[0])
            oney = int(response[1])
            twox = int(response[2])
            twoy = int(response[3])
            threex = int(response[4])
            threey = int(response[5])
            fourx = int(response[6])
            foury = int(response[7])
            fivex = int(response[8])
            fivey = int(response[9])
            sixx = int(response[10])
            sixy = int(response[11])
            # Display Player One
            if facings[0] == "1":
                screen.blit(cave_image_player, (onex, oney))
            else:
                screen.blit(cave_image_player_flipped, (onex, oney))
            # Display Player Two
            if facings[1] == "1":
                screen.blit(cave_image_player, (twox, twoy))
            else:
                screen.blit(cave_image_player_flipped, (twox, twoy))
            # Display Player Three
            if facings[2] == "1":
                screen.blit(cave_image_player, (threex, threey))
            else:
                screen.blit(cave_image_player_flipped, (threex, threey))
            # Display Player 4
            if facings[3] == "1":
                screen.blit(cave_image_player, (fourx, foury))
            else:
                screen.blit(cave_image_player_flipped, (fourx, foury))
            # Display Player 5
            if facings[4] == "1":
                screen.blit(cave_image_player, (fivex, fivey))
            else:
                screen.blit(cave_image_player_flipped, (fivex, fivey))
            # Display Player 6
            if facings[5] == "1":
                screen.blit(cave_image_player, (sixx, sixy))
            else:
                screen.blit(cave_image_player_flipped, (sixx, sixy))
            # Display Bullets
            bullets = pickle.loads(all_bullets)
            for bullet in bullets[0]:
                bullet.draw(screen)
            for bullet in bullets[1]:
                bullet.draw(screen)
            for bullet in bullets[2]:
                bullet.draw(screen)
            for bullet in bullets[3]:
                bullet.draw(screen)
            for bullet in bullets[4]:
                bullet.draw(screen)
            for bullet in bullets[5]:
                bullet.draw(screen)
            # Kill Counter
            text = font.render(f"Kills: {score}", False, (255, 255, 0))
            screen.blit(text, (20, 20))
        # Event Handler
        events = pygame.event.get()
        for event in events:
            # QUIT
            if event.type == pygame.QUIT:
                run = False
        # Update Display
        pygame.display.update()
        # End Of Game Loop
    # Final Dissconnection Message
    try:
        network.send_string("!DISSCONNECT")
    except:
        pass
else:
    exit()