import pygame
import numpy as np
import time
import pygame.midi as midi

# Initialize Pygame
pygame.init()

# Set grid size
grid_size = (40, 40)

# Set up Pygame window
cell_size = 20
width, height = grid_size[0] * cell_size, grid_size[1] * cell_size
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game of Life Music")

# Set up Pygame MIDI
midi.init()
player = midi.Output(0)
player.set_instrument(0)  # You can change the instrument (0-127) for different sounds

# Initialize the grid with random values
grid = np.random.choice([0, 1], size=grid_size)

# Define musical notes (MIDI note numbers)
notes = [60, 62, 64, 65, 67, 69, 71, 72]

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Create a copy of the grid to update
    new_grid = np.copy(grid)

    # Update the grid based on the rules of the Game of Life
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            neighbors_sum = np.sum(grid[i-1:i+2, j-1:j+2]) - grid[i, j]
            if grid[i, j] == 1:
                if neighbors_sum < 2 or neighbors_sum > 3:
                    new_grid[i, j] = 0
            else:
                if neighbors_sum == 3:
                    new_grid[i, j] = 1

    # Play notes based on the state of the grid
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            if grid[i, j] == 1:
                player.note_on(notes[i % len(notes)], velocity=64)
                time.sleep(0.1)

    # Update the grid
    grid = np.copy(new_grid)

    # Draw the grid on the Pygame window
    screen.fill((255, 255, 255))
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            color = (0, 0, 0) if grid[i, j] == 1 else (255, 255, 255)
            pygame.draw.rect(screen, color, (j * cell_size, i * cell_size, cell_size, cell_size))

    pygame.display.flip()

# Clean up
player.close()
midi.quit()
pygame.quit()
