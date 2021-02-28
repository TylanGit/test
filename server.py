# Stop Imports
if __name__ == "__main__":
    # Imports
    print()
    print("Importing Libraries ...")
    print()
    import pygame
    import pickle
    import socket
    import threading
    import time
    import random
    import urllib3
    from urllib.request import urlopen
    import re
    from network import Server
    print()
    # Assgin Variables
    print("Assigning Variables ...")
    print()
    ip_address_local = "ERROR"
    ip_address_public = "ERROR"
    port = 9306
    clock = pygame.time.Clock()
    tile_size = 20
    world_data = []
    full = False
    connected_players = [False, False, False, False, False, False]
    character = [None, None, None, None, None, None]
    player_positions = [[0, - 20], [0, - 20], [0, - 20], [0, - 20], [0, - 20], [0, - 20]]
    player_facings = [1, 1, 1, 1, 1, 1]
    player_bullets = [[], [], [], [], [], []]
    player_scores = [0, 0, 0, 0 ,0, 0]
    # Loading Images
    print("Loading Images ...")
    print()
    cave_image_dirt = pygame.image.load("./blocks/dirt_cave.png")
    cave_image_block = pygame.image.load("./blocks/block_cave.png")
    cave_image_player = "./players/player.png"
    # Find Ip Addresses
    print("Finding Local Ip Address ...")
    print()
    try:
        ip_address_local = "192.168.1.27"
    except:
        pass
    print("Finding Public Ip Address ...")
    print()
    try:
        data = str(urlopen("http://checkip.dyndns.com/").read())
        ip_address_public = re.compile(r"Address: (\d+.\d+.\d+.\d+)").search(data).group(1)
    except:
        pass
    # Generate World Data
    print("Generating World Data ...")
    print()
    pickle_in = open("./leveldata/level_data.txt", "rb")
    tile_list = pickle.load(pickle_in)
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
    # Generate Spawn
    print("Defining Functions ...")
    print()
    def generate_spawn():
        player_x = random.randint(4, 240) * 5
        player_y = - 20
        return player_x, player_y
    # Bullets
    class Bullet(object):
        # Init
        def __init__(self, x, y, radius, color, facing):
            self.x = x
            self.y = y
            self.radius = radius
            self.color = color
            try:
                self.facing = int(facing)
            except:
                self.facing = -1
            self.vel = 20 * self.facing
    # Player
    class Player():
        # Init
        def __init__(self):
            self.reset()
            self.alive = False
        # Update
        def update(self, up, left, right, player):
            # Change in x and y
            dx = 0
            dy = 0
            # Movement
            if up == "1" and self.jumped == False and self.in_air == False:
                self.vel_y = -15
                self.jumped = True
            else:
                self.jumped = False
            if left == "1":
                dx -= 5
            if right == "1":
                dx += 5
            # Gravity
            self.vel_y += 1.2
            if self.vel_y > 15:
                self.vel_y = 15
            dy += self.vel_y
            # Collisions
            self.in_air = True
            for tile in world_data:
                # X Axis
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # Y Axis
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.in_air = False
                    elif self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
            # Update Player Location
            self.rect.x += dx
            self.rect.y += dy
            player_location = player_positions[player]
            player_location[0] = self.rect.x
            player_location[1] = self.rect.y - 20
            return self.rect.x, self.rect.y
        # Reset
        def reset(self):
            player_x, player_y = generate_spawn()
            self.image = pygame.image.load(cave_image_player)
            self.rect = self.image.get_rect()
            self.rect.x = player_x
            self.rect.y = player_y
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.vel_y = 0
            self.jumped = False
            self.in_air = True
    # Client
    def client(player, connection, address):
        # On Connection
        print(f"User Connected: {address}, {connection}")
        print()
        network.send_string(connection, "!JOIN")
        character[player] = Player()
        shoot = None
        # Game Loop
        while True:
            # Game Tick
            clock.tick(60)
            # Receive Message
            message = network.receive_string(connection)
            # If !DISSCONNECT
            if message == "!DISSCONNECT":
                break
            # Game Code
            if message != None:
                # Seperate Inputs
                data = message.split("@")
                input_up = data[0]
                input_left = data[1]
                input_right = data[2]
                input_mouse_position = data[3]
                input_mouse_clicks = data[4]
                input_leftclick = input_mouse_clicks[1 : 5]
                facing = data[5]
                # Facing
                if facing == "1":
                    player_facings[player] = 1
                else:
                    player_facings[player] = 0
                # Player
                x, y = character[player].update(input_up, input_left, input_right, player)
                # Bullets
                playerbullets = player_bullets[player]
                if input_leftclick == "Fals":
                    shoot = True
                if input_leftclick == "True" and shoot:
                    if len(playerbullets) < 3:
                        playerbullets.append(Bullet(x+20//2, y-10, 3 ,(255,0,0), facing))
                    shoot = False
                for bullet in playerbullets:
                    if bullet.x < 1280 and bullet.x > 0:
                        bullet.x += bullet.vel
                    else:
                        playerbullets.pop(playerbullets.index(bullet))
                player_bullets[player] = playerbullets
                for bullet in player_bullets[player]:
                    if bullet.x >= player_positions[0][0] and bullet.x <= player_positions[0][0] + 20:
                        if bullet.y >= player_positions[0][1] and bullet.y <= player_positions[0][1] + 20:
                            player_scores[player] += 1
                            player_bullets[player].pop(player_bullets[player].index(bullet))
                            character[0].reset()
                    if bullet.x >= player_positions[1][0] and bullet.x <= player_positions[1][0] + 20:
                        if bullet.y >= player_positions[1][1] and bullet.y <= player_positions[1][1] + 20:
                            player_scores[player] += 1
                            player_bullets[player].pop(player_bullets[player].index(bullet))
                            character[1].reset()
                    if bullet.x >= player_positions[2][0] and bullet.x <= player_positions[2][0] + 20:
                        if bullet.y >= player_positions[2][1] and bullet.y <= player_positions[2][1] + 20:
                            player_scores[player] += 1
                            player_bullets[player].pop(player_bullets[player].index(bullet))
                            character[2].reset()
                    if bullet.x >= player_positions[3][0] and bullet.x <= player_positions[3][0] + 20:
                        if bullet.y >= player_positions[3][1] and bullet.y <= player_positions[3][1] + 20:
                            player_scores[player] += 1
                            player_bullets[player].pop(player_bullets[player].index(bullet))
                            character[3].reset()
                    if bullet.x >= player_positions[4][0] and bullet.x <= player_positions[4][0] + 20:
                        if bullet.y >= player_positions[4][1] and bullet.y <= player_positions[4][1] + 20:
                            player_scores[player] += 1
                            player_bullets[player].pop(player_bullets[player].index(bullet))
                            character[4].reset()
                    if bullet.x >= player_positions[5][0] and bullet.x <= player_positions[5][0] + 20:
                        if bullet.y >= player_positions[5][1] and bullet.y <= player_positions[5][1] + 20:
                            player_scores[player] += 1
                            player_bullets[player].pop(player_bullets[player].index(bullet))
                            character[5].reset()
                # Send Data To Client
                score = f"{player_scores[player]}"
                network.send_string(connection, f"{player_positions}")
                network.send_byte(connection, pickle.dumps(player_bullets))
                network.send_string(connection, score)
                network.send_string(connection, f"{player_facings}")
        # Close Connection
        player_location = player_positions[player]
        player_location[0] = 0
        player_location[1] = - 20
        player_scores[player] = 0
        player_bullets[player] = []
        connected_players[player] = False
        connection.close()
        print(f"User Dissconnected: {address}, {connection}")
        print()
    # Active Connections
    def active_connections():
        update_connections = -1
        while True:
            connections = threading.activeCount() - 2
            if connections != update_connections:
                time.sleep(0.1)
                print(f"Active Connections: {connections}")
                print(connected_players)
                print()
                update_connections = connections
    # Server
    def server():
        # Server Started
        print("Server Started ...")
        print(f"Local IP: {ip_address_local}")
        print(f"Public IP: {ip_address_public}")
        print()
        # Active Connections
        thread = threading.Thread(target = active_connections)
        thread.start()
        # While Server Is Running
        while True:
            # Wait For Connection
            connection, address = network.receive_connection()
            # Find Player Number
            player = 0
            for placeholder in connected_players:
                placeholder = placeholder
                if connected_players[player] == False:
                    connected_players[player] = True
                    full = False
                    break
                else:
                    full = True
                    player += 1
            # Handle Client
            if full == False:
                thread = threading.Thread(target = client, args = (player, connection, address))
                thread.start()
            else:
                print()
                print(f"Server Full Connection Failed: {address}, {connection}")
                network.send_string(connection, "!FULL")
    # Start Server
    print("Starting Server ...")
    print()
    network = Server(ip_address_local, port)
    server()
    # Exit
else:
    exit()