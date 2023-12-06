# Python code to implement Conway's Game Of Life
import argparse

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# setting up the values for the grid
FIRING = 0
REFRACTORY = 1
DEAD = 2
vals = [FIRING, REFRACTORY, DEAD]
colors = ['white', 'red', 'black']

def randomGrid(N, firingCellDensity):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N * N, p=[firingCellDensity, 0, 1 - firingCellDensity]).reshape(N, N)

def update(frameNum, img, grid, N):
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            # apply rules
            if grid[i, j] == FIRING:
                newGrid[i, j] = REFRACTORY
            elif grid[i, j] == REFRACTORY:
                newGrid[i, j] = DEAD
            elif grid[i, j] == DEAD:
                # Ensure that we don't get out of bounds index
                firing_neighbors = np.sum(grid[max(0, i - 1):min(N, i + 2), max(0, j - 1):min(N, j + 2)] == FIRING)

                if firing_neighbors == 2:
                    newGrid[i, j] = FIRING

    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img


# main() function
def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Brian's brain simulation")

    # add arguments
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--density', dest='density', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    args = parser.parse_args()

    # set grid size
    N = 100
    if args.N and int(args.N) > 8:
        N = int(args.N)

    # set animation update interval
    updateInterval = 50
    if args.interval:
        updateInterval = int(args.interval)

    # declare grid
    grid = np.array([])

    density = 0.7
    if args.density and 0 < float(args.density) < 1:
        density = float(args.density)
    grid = randomGrid(N, density)

    # set up animation
    fig, ax = plt.subplots()
    cmap = plt.cm.colors.ListedColormap(colors)
    bounds = [0, 1, 2, 3]  # Bounds for each value
    norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N)

    img = ax.imshow(grid, interpolation='nearest', cmap=cmap, norm=norm)

    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N,),
                                  frames=10,
                                  interval=updateInterval,
                                  save_count=50)

    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()


# call main
if __name__ == '__main__':
    main()
