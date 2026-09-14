import pygame
import random
from heapq import heappop, heappush
import sys
import math

# =========================================================
# INITIALIZATION
# =========================================================

pygame.init()

# Window
screen_width, screen_height = 500, 600
board_height = 500

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Treasure Hunt - AI Pathfinder")

# =========================================================
# COLORS
# =========================================================

BG_COLOR = (18, 42, 58)
BOARD_COLOR = (28, 72, 82)
GRID_COLOR = (55, 103, 110)

PANEL_COLOR = (12, 28, 40)

WHITE = (245, 248, 250)
LIGHT_TEXT = (205, 220, 225)

GOLD_COLOR = (255, 205, 55)
GOLD_DARK = (180, 125, 25)

HP_COLOR = (70, 210, 110)
HP_LOW_COLOR = (225, 70, 70)

PATH_COLOR = (90, 210, 220)
TARGET_COLOR = (255, 210, 70)

DANGER_COLOR = (230, 75, 65)
OBSTACLE_COLOR = (85, 92, 98)

# =========================================================
# ICON
# =========================================================

try:
    icon = pygame.image.load("box.png")
    pygame.display.set_icon(icon)
except pygame.error:
    pass

# =========================================================
# IMAGE LOADING
# =========================================================

def load_and_scale(image_path, size=(20, 20)):
    try:
        image = pygame.image.load(image_path).convert_alpha()
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"Failed to load {image_path}: {e}")
        pygame.quit()
        sys.exit()


player_img = load_and_scale("pirate_1009968.png", (25, 25))
gold_img = load_and_scale("gold.png", (25, 25))
damage_img = load_and_scale("damagee.png", (25, 25))
obstacle_img = load_and_scale("obstacle.png", (25, 25))
# =========================================================
# GAME SETTINGS
# =========================================================

gridsize = 25
grid_width = 20
grid_height = 20

hp = 100
gold_count = 0

player_pos = [0, 0]

# =========================================================
# FONTS
# =========================================================

font_title = pygame.font.SysFont("Arial", 24, bold=True)
font_small = pygame.font.SysFont("Arial", 18, bold=True)
font_tiny = pygame.font.SysFont("Arial", 14)
font_large = pygame.font.SysFont("Arial", 46, bold=True)

# =========================================================
# POSITION GENERATOR
# =========================================================

def generate_positions(count, avoid_positions):
    positions = set()

    while len(positions) < count:
        pos = (
            random.randint(0, grid_width - 1),
            random.randint(0, grid_height - 1)
        )

        if pos not in avoid_positions:
            positions.add(pos)

    return list(positions)


avoid_positions = {(player_pos[0], player_pos[1])}

gold_positions = generate_positions(
    10,
    avoid_positions
)

total_gold = len(gold_positions)

damage_positions = generate_positions(
    20,
    avoid_positions | set(gold_positions)
)

obstacle_positions = generate_positions(
    30,
    avoid_positions |
    set(gold_positions) |
    set(damage_positions)
)

# =========================================================
# A* PATHFINDING
# =========================================================

def a_star(start, goal, obstacles):

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = []

    heappush(open_set, (0, start))

    came_from = {}

    g_score = {
        start: 0
    }

    f_score = {
        start: heuristic(start, goal)
    }

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
            (current[0], current[1] - 1)
        ]

        for neighbor in neighbors:

            if (
                0 <= neighbor[0] < grid_width
                and
                0 <= neighbor[1] < grid_height
                and
                neighbor not in obstacles
                and
                neighbor not in closed_set
            ):

                tentative_g_score = g_score[current] + 1

                if (
                    neighbor not in g_score
                    or
                    tentative_g_score < g_score[neighbor]
                ):

                    came_from[neighbor] = current

                    g_score[neighbor] = tentative_g_score

                    f_score[neighbor] = (
                        tentative_g_score
                        +
                        heuristic(neighbor, goal)
                    )

                    heappush(
                        open_set,
                        (f_score[neighbor], neighbor)
                    )

    return []


# =========================================================
# FIND NEAREST GOLD
# =========================================================

def find_nearest_gold(current_pos, gold_positions, obstacles):

    min_distance = float("inf")

    nearest_gold = None

    shortest_path = []

    for gold in gold_positions:

        path = a_star(
            tuple(current_pos),
            gold,
            obstacles
        )

        if path:

            distance = len(path)

            if distance < min_distance:

                min_distance = distance

                nearest_gold = gold

                shortest_path = path

    return nearest_gold, shortest_path


# =========================================================
# TEXT HELPER
# =========================================================

def draw_text(text, font, color, x, y):

    text_surface = font.render(
        text,
        True,
        color
    )

    screen.blit(
        text_surface,
        (x, y)
    )


# =========================================================
# DRAW BOARD
# =========================================================

def draw_board():

    # Main board
    pygame.draw.rect(
        screen,
        BOARD_COLOR,
        (0, 0, screen_width, board_height)
    )

    # Small tile shading
    for row in range(grid_height):

        for col in range(grid_width):

            tile_x = col * gridsize
            tile_y = row * gridsize

            if (row + col) % 2 == 0:

                pygame.draw.rect(
                    screen,
                    (31, 77, 87),
                    (
                        tile_x,
                        tile_y,
                        gridsize,
                        gridsize
                    )
                )

    # Grid
    for x in range(
        0,
        grid_width * gridsize,
        gridsize
    ):

        pygame.draw.line(
            screen,
            GRID_COLOR,
            (x, 0),
            (x, board_height),
            1
        )

    for y in range(
        0,
        grid_height * gridsize,
        gridsize
    ):

        pygame.draw.line(
            screen,
            GRID_COLOR,
            (0, y),
            (screen_width, y),
            1
        )


# =========================================================
# DRAW AI PATH
# =========================================================

def draw_ai_path(path):

    if not path:
        return

    points = []

    for position in path:

        center_x = (
            position[0] * gridsize
            + gridsize // 2
        )

        center_y = (
            position[1] * gridsize
            + gridsize // 2
        )

        points.append(
            (center_x, center_y)
        )

    if len(points) > 1:

        pygame.draw.lines(
            screen,
            PATH_COLOR,
            False,
            points,
            3
        )

    # Small path dots
    for point in points:

        pygame.draw.circle(
            screen,
            PATH_COLOR,
            point,
            2
        )


# =========================================================
# DRAW GOLD EFFECT
# =========================================================

def draw_gold(position, time):

    x = position[0] * gridsize + 10
    y = position[1] * gridsize + 10

    pulse = int(
        2 + math.sin(time * 0.006) * 2
    )

    pygame.draw.circle(
        screen,
        (100, 80, 25),
        (x, y),
        10 + pulse
    )

    screen.blit(
        gold_img,
        (
            position[0] * gridsize,
            position[1] * gridsize
        )
    )


# =========================================================
# DRAW TARGET
# =========================================================

def draw_target(target):

    if target is None:
        return

    x = target[0] * gridsize
    y = target[1] * gridsize

    pygame.draw.rect(
        screen,
        TARGET_COLOR,
        (
            x + 2,
            y + 2,
            gridsize - 4,
            gridsize - 4
        ),
        2
    )


# =========================================================
# DRAW HUD
# =========================================================

def draw_hud():

    pygame.draw.rect(
        screen,
        PANEL_COLOR,
        (
            0,
            board_height,
            screen_width,
            screen_height - board_height
        )
    )

    # Title
    draw_text(
        "TREASURE HUNT",
        font_title,
        WHITE,
        15,
        510
    )

    # AI status
    if current_target:

        draw_text(
            "AI: SEARCHING",
            font_tiny,
            PATH_COLOR,
            15,
            540
        )

    else:

        draw_text(
            "AI: NO TARGET",
            font_tiny,
            DANGER_COLOR,
            15,
            540
        )

    # Gold
    draw_text(
        f"GOLD  {gold_count}/{total_gold}",
        font_small,
        GOLD_COLOR,
        170,
        510
    )

    # HP label
    draw_text(
        f"HP  {hp}",
        font_small,
        WHITE,
        170,
        540
    )

    # HP bar background
    pygame.draw.rect(
        screen,
        (50, 55, 60),
        (260, 542, 220, 14)
    )

    # HP bar
    hp_width = max(
        0,
        int(220 * hp / 100)
    )

    hp_color = (
        HP_COLOR
        if hp > 30
        else HP_LOW_COLOR
    )

    pygame.draw.rect(
        screen,
        hp_color,
        (260, 542, hp_width, 14)
    )

    # Target
    if current_target:

        draw_text(
            "TARGET",
            font_tiny,
            LIGHT_TEXT,
            350,
            510
        )


# =========================================================
# GAME VARIABLES
# =========================================================

running = True

clock = pygame.time.Clock()

current_path = []

path_index = 0

current_target = None

game_over = False

game_result = None

# Find first target
current_target, current_path = find_nearest_gold(
    player_pos,
    gold_positions,
    obstacle_positions
)

if current_target:

    path_index = 0

    print(
        f"Initial target: {current_target}"
    )

else:

    print(
        "No path to any gold found."
    )


# =========================================================
# MAIN GAME LOOP
# =========================================================

try:

    while running:

        current_time = pygame.time.get_ticks()

        # -------------------------------------------------
        # EVENTS
        # -------------------------------------------------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False

            if (
                game_over
                and
                event.type == pygame.KEYDOWN
                and
                event.key == pygame.K_SPACE
            ):

                running = False

        # -------------------------------------------------
        # GAME UPDATE
        # -------------------------------------------------

        if not game_over:

            if (
                current_path
                and
                path_index < len(current_path)
            ):

                player_pos = list(
                    current_path[path_index]
                )

                path_index += 1

                player_tuple = tuple(
                    player_pos
                )

                # Damage collision
                if player_tuple in damage_positions:

                    hp -= 10

                    damage_positions.remove(
                        player_tuple
                    )

                    print(
                        f"Damage! HP: {hp}"
                    )

                # Gold collection
                if player_tuple in gold_positions:

                    gold_count += 1

                    gold_positions.remove(
                        player_tuple
                    )

                    print(
                        f"Collected gold: "
                        f"{gold_count}/{total_gold}"
                    )

                    # Find next target
                    if gold_positions:

                        (
                            current_target,
                            current_path
                        ) = find_nearest_gold(
                            player_pos,
                            gold_positions,
                            obstacle_positions
                        )

                        path_index = 0

                    else:

                        current_target = None

                        current_path = []

            # Lose condition
            if hp <= 0:

                game_over = True

                game_result = "lose"

            # Win condition
            elif gold_count >= total_gold:

                game_over = True

                game_result = "win"

        # -------------------------------------------------
        # DRAW
        # -------------------------------------------------

        draw_board()

        # Draw AI path
        if not game_over:

            draw_ai_path(
                current_path[path_index:]
            )

        # Target
        if current_target and not game_over:

            draw_target(
                current_target
            )

        # Gold
        for gold in gold_positions:

            draw_gold(
                gold,
                current_time
            )

        # Damage
        for dmg in damage_positions:

            screen.blit(
                damage_img,
                (
                    dmg[0] * gridsize,
                    dmg[1] * gridsize
                )
            )

        # Obstacles
        for obs in obstacle_positions:

            screen.blit(
                obstacle_img,
                (
                    obs[0] * gridsize,
                    obs[1] * gridsize
                )
            )

        # Player
        if not game_over:

            screen.blit(
                player_img,
                (
                    player_pos[0] * gridsize,
                    player_pos[1] * gridsize
                )
            )

        # HUD
        draw_hud()

        # -------------------------------------------------
        # WIN / LOSE SCREEN
        # -------------------------------------------------

        if game_over:

            overlay = pygame.Surface(
                (screen_width, board_height),
                pygame.SRCALPHA
            )

            overlay.fill(
                (0, 0, 0, 170)
            )

            screen.blit(
                overlay,
                (0, 0)
            )

            if game_result == "win":

                title = "TREASURE FOUND!"

                title_color = GOLD_COLOR

                subtitle = (
                    f"You collected "
                    f"{gold_count}/{total_gold} gold!"
                )

            else:

                title = "GAME OVER"

                title_color = DANGER_COLOR

                subtitle = (
                    "The pirate ran out of HP."
                )

            title_surface = font_large.render(
                title,
                True,
                title_color
            )

            title_x = (
                screen_width
                -
                title_surface.get_width()
            ) // 2

            screen.blit(
                title_surface,
                (
                    title_x,
                    190
                )
            )

            subtitle_surface = font_small.render(
                subtitle,
                True,
                WHITE
            )

            subtitle_x = (
                screen_width
                -
                subtitle_surface.get_width()
            ) // 2

            screen.blit(
                subtitle_surface,
                (
                    subtitle_x,
                    250
                )
            )

            instruction = font_tiny.render(
                "Press SPACE to close",
                True,
                LIGHT_TEXT
            )

            instruction_x = (
                screen_width
                -
                instruction.get_width()
            ) // 2

            screen.blit(
                instruction,
                (
                    instruction_x,
                    290
                )
            )

        # -------------------------------------------------
        # DISPLAY
        # -------------------------------------------------

        pygame.display.update()

        clock.tick(6)


except Exception as e:

    print(
        f"An unexpected error occurred: {e}"
    )

finally:

    pygame.quit()

    sys.exit()