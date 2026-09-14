import pygame
import random
from heapq import heappop, heappush
import sys


pygame.init()
screen_width, screen_height = 500, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Treasure Hunt: Collect All Gold")
try:
    icon = pygame.image.load('box.png')
    pygame.display.set_icon(icon)
except pygame.error as e:
    print(f"Failed to load icon image: {e}")
    pygame.quit()
    sys.exit()


def load_and_scale(image_path, size=(20, 20)):
    try:
        image = pygame.image.load(image_path)
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"Failed to load {image_path}: {e}")
        pygame.quit()
        sys.exit()


player_img = load_and_scale('pirate_1009968.png')
gold_img = load_and_scale('gold.png')
damage_img = load_and_scale('damagee.png')
obstacle_img = load_and_scale('obstacle.png')


player_pos = [0, 0]
gridsize = 20
grid_width, grid_height = 25, 25
hp = 100
gold_count = 0

color_white = (255, 255, 255)
color_black = (0, 0, 0)
color_blue = (0, 0, 128)


def generate_positions(count, avoid_positions):
    positions = set()
    while len(positions) < count:
        pos = (random.randint(0, grid_width - 1), random.randint(0, grid_height - 1))
        if pos not in avoid_positions:
            positions.add(pos)
    return list(positions)


avoid_positions = {(player_pos[0], player_pos[1])}
gold_positions = generate_positions(10, avoid_positions)  # 10 gold pieces
total_gold = len(gold_positions)  # Total number of gold pieces to collect
damage_positions = generate_positions(20, avoid_positions | set(gold_positions))
obstacle_positions = generate_positions(30, avoid_positions | set(gold_positions) | set(damage_positions))


def a_star(start, goal, obstacles):
    def heuristic(a, b):
        # Manhattan distance heuristic
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = []
    heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    closed_set = set()

    while open_set:
        _, current = heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        closed_set.add(current)


        neighbors = [
            (current[0] + 1, current[1]),
            (current[0] - 1, current[1]),
            (current[0], current[1] + 1),
            (current[0], current[1] - 1),
        ]

        for neighbor in neighbors:
            if (
                0 <= neighbor[0] < grid_width
                and 0 <= neighbor[1] < grid_height
                and neighbor not in obstacles
                and neighbor not in closed_set
            ):
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heappush(open_set, (f_score[neighbor], neighbor))

    return []


def find_nearest_gold(current_pos, gold_positions, obstacles):
    min_distance = float('inf')
    nearest_gold = None
    shortest_path = []

    for gold in gold_positions:
        path = a_star(tuple(current_pos), gold, obstacles)
        if path:
            distance = len(path)
            if distance < min_distance:
                min_distance = distance
                nearest_gold = gold
                shortest_path = path

    return nearest_gold, shortest_path


def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


running = True
clock = pygame.time.Clock()
current_path = []
path_index = 0
current_target = None


current_target, current_path = find_nearest_gold(player_pos, gold_positions, obstacle_positions)
if current_target:
    path_index = 0
    print(f"Initial target: {current_target} with path length {len(current_path)}")
else:
    print("No path to any gold found at initialization.")


try:
    while running:
        screen.fill(color_blue)


        font_small = pygame.font.SysFont("Arial", 30)
        draw_text(f"HP: {hp}", font_small, color_white, 10, grid_height * gridsize + 10)
        draw_text(f"Gold: {gold_count}/{total_gold}", font_small, color_white, 10, grid_height * gridsize + 50)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break 


        if current_path and path_index < len(current_path):
            player_pos = list(current_path[path_index])
            path_index += 1
            print(f"Player moved to {player_pos} (Path step {path_index}/{len(current_path)})")

            # Check for Damage
            player_tuple = tuple(player_pos)
            if player_tuple in damage_positions:
                hp -= 10
                damage_positions.remove(player_tuple)
                print(f"Hit damage at {player_tuple}! HP: {hp}")

            # Check for Gold Collection
            if player_tuple in gold_positions:
                gold_count += 1
                gold_positions.remove(player_tuple)
                print(f"Collected gold at {player_tuple}! Total Gold: {gold_count}/{total_gold}")

                # Find Next Nearest Gold
                if gold_positions:
                    current_target, current_path = find_nearest_gold(player_pos, gold_positions, obstacle_positions)
                    path_index = 0
                    if current_target:
                        print(f"New target: {current_target} with path length {len(current_path)}")
                    else:
                        print("No path to any remaining gold found.")
                else:
                    # All gold collected; victory condition will be handled below
                    pass

        # Check for Defeat Condition
        if hp <= 0:
            font_large = pygame.font.SysFont("Arial", 50)
            draw_text("You Lose!", font_large, (255, 0, 0), screen_width // 2 - 100, screen_height // 2 - 25)
            pygame.display.update()
            pygame.time.wait(2000)
            running = False

        # Check for Victory Condition
        if gold_count >= total_gold:
            font_large = pygame.font.SysFont("Arial", 50)
            draw_text("You Win!", font_large, (255, 255, 0), screen_width // 2 - 100, screen_height // 2 - 25)
            pygame.display.update()
            pygame.time.wait(2000)
            running = False

        # Draw Grid Lines
        for x in range(0, grid_width * gridsize, gridsize):
            pygame.draw.line(screen, color_white, (0, x), (grid_width * gridsize, x), 1)
        for y in range(0, grid_height * gridsize, gridsize):
            pygame.draw.line(screen, color_white, (y, 0), (y, grid_height * gridsize), 1)

        # Draw Player
        screen.blit(player_img, (player_pos[0] * gridsize, player_pos[1] * gridsize))

        # Draw Gold Pieces
        for gold in gold_positions:
            screen.blit(gold_img, (gold[0] * gridsize, gold[1] * gridsize))

        # Draw Damage Items
        for dmg in damage_positions:
            screen.blit(damage_img, (dmg[0] * gridsize, dmg[1] * gridsize))

        # Draw Obstacles
        for obs in obstacle_positions:
            screen.blit(obstacle_img, (obs[0] * gridsize, obs[1] * gridsize))

        pygame.display.update()
        clock.tick(10)  # Control the frame rate (10 FPS)

except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    pygame.quit()
    sys.exit()