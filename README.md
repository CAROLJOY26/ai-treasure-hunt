# 🏴‍☠️ AI Treasure Hunt

A Python-based AI treasure hunt game built with Pygame and A* pathfinding.

The game features an AI-controlled pirate that automatically navigates through a fixed maze, avoids obstacles and damage areas, and searches for the nearest treasure until all gold is collected.

## 🎮 About the Game

AI Treasure Hunt is a grid-based game where an AI-controlled pirate must navigate through a maze and collect all available gold.

The game environment contains:

- 🪙 Gold treasures
- 🪨 Obstacles
- 💥 Damage areas
- ❤️ Health points
- 🗺️ A fixed maze
- 🤖 AI-controlled movement

The AI automatically calculates paths through the maze and selects the nearest reachable gold using the A* pathfinding algorithm.

The main objective is to collect all 10 gold treasures while keeping the pirate's health above zero.

## 🤖 Artificial Intelligence

The main AI component of the project is A* (A-Star) Pathfinding.

The AI uses A* to find efficient paths through the grid while avoiding obstacles.

For each available gold location, the AI:

1. Calculates a possible path.
2. Checks whether the gold is reachable.
3. Calculates the path length.
4. Compares the available paths.
5. Selects the nearest reachable gold.
6. Moves automatically toward the selected target.
7. Repeats the process after collecting the gold.

The AI continues this process until all gold treasures have been collected.

## 🧠 A* Pathfinding

The project uses the standard A* evaluation function:

f(n) = g(n) + h(n)

Where:

- `g(n)` = cost of reaching the current position
- `h(n)` = estimated distance from the current position to the target
- `f(n)` = total estimated path cost

The game uses Manhattan distance as the heuristic:

h(n) = |x1 - x2| + |y1 - y2|

This is suitable for the game's grid-based movement.

## 🗺️ Game Environment

The game uses a fixed grid-based maze.

The maze contains different types of positions.

### 🟦 Walkable Areas

The pirate can move through normal walkable cells.

### 🪨 Obstacles

Obstacles block movement.

The pathfinding algorithm treats obstacle positions as unavailable when calculating paths.

### 💥 Damage Areas

Damage areas can be reached by the pirate, but entering one reduces health.

Each damage event reduces the pirate's health by:

10 HP

### 🪙 Gold

Gold represents the main objective of the game.

The AI searches for reachable gold and collects each treasure one by one.

## ❤️ Health System

The pirate starts with:

100 HP

Whenever the pirate reaches a damage area:

HP = HP - 10

The game continues while the pirate has health remaining.

If the pirate's health reaches zero, the game ends.

## 🏆 Win Condition

The AI wins the game when all available gold treasures have been collected.

The default game contains:

10 Gold Treasures

## 🎮 Game Features

- 🤖 Automated AI movement
- 🧠 A* pathfinding
- 🗺️ Fixed maze environment
- 🪙 Multiple treasure locations
- 🪨 Obstacles
- 💥 Damage areas
- ❤️ Health system
- 🏆 Win condition
- 🎨 Pygame graphical interface
- 📊 AI path visualization
- 🎯 Target selection
- 🏴‍☠️ Pirate character
- 🔄 Automatic navigation between targets

## 🛠️ Technologies Used

- Python 3.11
- Pygame 2.6.1
- A* Pathfinding Algorithm
- Heap Queue (`heapq`)
- Grid-based Navigation
- Artificial Intelligence
- Game Development

## 📁 Project Structure

```text
ai-treasure-hunt/
│
├── main.py
├── th.py
│
├── box.png
├── damagee.png
├── gold.png
├── obstacle.png
└── pirate_1009968.png
