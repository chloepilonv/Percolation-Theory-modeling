import sqlite3
import numpy as np
import matplotlib.pyplot as plt

# Path to the extracted SQLite database file from Kaggle Wildires
# Download at https://www.kaggle.com/datasets/rtatman/188-million-us-wildfires/
db_file_path = '(...)/mnt/data/extracted/FPA_FOD_20170508.sqlite'

# Function to load wildfire data
def load_wildfire_data(db_path, limit=1000):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT LATITUDE, LONGITUDE, FIRE_SIZE FROM Fires LIMIT ?", (limit,))
    data = cursor.fetchall()
    conn.close()
    return data

# Function to initialize a grid for the percolation model
def initialize_grid_modified(data, grid_size=100):
    grid = np.zeros((grid_size, grid_size))
    max_lat = max([d[0] for d in data])
    min_lat = min([d[0] for d in data])
    max_lon = max([d[1] for d in data])
    min_lon = min([d[1] for d in data])

    lat_range = max_lat - min_lat
    lon_range = max_lon - min_lon

    for lat, lon, size in data:
        # Adjusting the calculation to avoid out-of-bounds indexing
        row = int(grid_size * (lat - min_lat) / lat_range) - 1
        col = int(grid_size * (lon - min_lon) / lon_range) - 1
        row = max(0, min(row, grid_size - 1))
        col = max(0, min(col, grid_size - 1))
        size = 1000 # Assign fire size to the grid cell
        grid[row, col] = size  

    return grid

# Function to simulate percolation
def simulate_percolation(grid, threshold=10):
    grid_size = len(grid)
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] >= threshold:
                for di in range(-1, 2):
                    for dj in range(-1, 2):
                        if 0 <= i + di < grid_size and 0 <= j + dj < grid_size:
                            grid[i + di][j + dj] = max(grid[i + di][j + dj], grid[i][j] - 1)
    return grid

# Load data
wildfire_data = load_wildfire_data(db_file_path)

# Initialize grid with modified function
grid = initialize_grid_modified(wildfire_data)

# Simulate percolation
simulated_grid = simulate_percolation(grid)

# Plotting the result
plt.imshow(simulated_grid, cmap='hot')
plt.colorbar()
plt.title("Wildfire Percolation Simulation")
plt.show()
