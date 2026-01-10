import numpy as np


class Mapview:
    # lat = None
    # lon = None
    width = 0
    height = 0
    x_min = 0
    x_max = 0
    y_min = 0
    y_max = 0
    num_tiles = 1
    aspect =1

    tiles = []
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.aspect = height/width

        self.updateTiles()

        # Start at top-left tile
        self.current_tile_x = 0
        self.current_tile_y = 0
        self.update_bounds_from_tile()

    def updateTiles(self):
        x_edges = np.linspace(0, self.width, self.num_tiles + 1, dtype=int)
        y_edges = np.linspace(0, self.height, self.num_tiles + 1, dtype=int)

        # Store tiles as (xmin, xmax, ymin, ymax)
        self.tiles = []
        for i in range(self.num_tiles):
            row = []
            for j in range(self.num_tiles):
                row.append((x_edges[i], x_edges[i + 1], y_edges[j], y_edges[j + 1]))
            self.tiles.append(row)


        self.tiles = np.array(self.tiles)  # shape: (num_tiles, num_tiles, 4)
    def update_bounds_from_tile(self):
        """Update x_min/x_max/y_min/y_max from current tile coordinates."""
        self.x_min, self.x_max, self.y_min, self.y_max = self.tiles[self.current_tile_x, self.current_tile_y]

    # -------------------
    # Traversal functions
    # -------------------

    def tile_x_inc(self):
        """Move one tile to the right if possible."""
        if self.current_tile_x < self.num_tiles - 1:
            self.current_tile_x += 1
            self.update_bounds_from_tile()

    def tile_x_dec(self):
        """Move one tile to the left if possible."""
        if self.current_tile_x > 0:
            self.current_tile_x -= 1
            self.update_bounds_from_tile()

    def tile_y_inc(self):
        """Move one tile up if possible."""
        if self.current_tile_y > 0:
            self.current_tile_y -= 1
            self.update_bounds_from_tile()

    def tile_y_dec(self):
        """Move one tile down if possible."""
        if self.current_tile_y < self.num_tiles - 1:
            self.current_tile_y += 1
            self.update_bounds_from_tile()

    def set_tile(self, x_idx, y_idx):
        """Jump to a specific tile index."""
        if 0 <= x_idx < self.num_tiles and 0 <= y_idx < self.num_tiles:
            self.current_tile_x = x_idx
            self.current_tile_y = y_idx
            self.update_bounds_from_tile()

    def tiles_inc(self):

        fraction_x = self.current_tile_x / self.num_tiles
        fraction_y = self.current_tile_y / self.num_tiles

        self.num_tiles = min(20, self.num_tiles+1)
        self.updateTiles()

        self.current_tile_x = min(int(round(fraction_x * self.num_tiles)), self.num_tiles - 1)
        self.current_tile_y = min(int(round(fraction_y * self.num_tiles)), self.num_tiles - 1)
        self.update_bounds_from_tile()

    def tiles_dec(self):
        fraction_x = self.current_tile_x / self.num_tiles
        fraction_y = self.current_tile_y / self.num_tiles

        self.num_tiles = max(1, self.num_tiles-1)
        self.updateTiles()
        self.current_tile_x = min(int(round(fraction_x * self.num_tiles)), self.num_tiles - 1)
        self.current_tile_y = min(int(round(fraction_y * self.num_tiles)), self.num_tiles - 1)
        self.update_bounds_from_tile()


    def get_current_bounds(self):
        """Return current tile bounds as a tuple: (xmin, xmax, ymin, ymax)."""
        return self.x_min, self.x_max, self.y_min, self.y_max

    def reset(self):
        """Reset to top-left tile."""
        self.current_tile_x = 0
        self.current_tile_y = 0
        self.update_bounds_from_tile()