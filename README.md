# Battleship AI 🥈

## Overview

This is a Python implementation of the classic Battleship game. It was created for the Aztec AI Clubs 2025 Spring AI Tournament where contestants had 1 hour to create a battleship algorithm and compete against each other. This was my submission, landing 2nd place overall.

## Features

- AI Strategy: Implements "Hunt and Target" modes. The AI is hunting (randomly firing) until a ship is hit, when it will then enter target mode and try to sink the rest of the ship.

- Ship Placement: Ships are placed pseudorandomly to avoid placing ships in adjacent squares.

Game Mechanics: The AI take turns guessing positions, and the game continues until all ships of one player are sunk.

## Installation

Ensure you have Python installed (version 3.x recommended). Clone the repository and run:

```python battleship.py```

## How It Works

### Board Initialization:

A 2D grid represents the ocean.

Ships are randomly placed while ensuring they don't overlap or touch adjacent ships.

### Gameplay:

The player and AI take turns guessing positions.

Hits and misses are recorded on the board.

If a ship is fully hit, it's marked as sunk.

### AI Strategy:

Hunt Mode: The AI fires at random locations to find a ship.

Target Mode: Once a hit is detected, the AI attempts to sink the ship by targeting adjacent tiles.

If the AI detects a miss, it adjusts its targeting strategy.

## Possible Improvements

Rather than firing randomly, I would've preferred to fire in a checkerboard pattern (fire, skip a square, fire, etc.)

Placing one ship at the far bottom right would've helped to before more optimally against other contestants who used the default strategy

## License

This project is open-source and available under the MIT License.
