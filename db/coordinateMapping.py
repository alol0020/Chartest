def pixel_to_latlon(x, y, points):
    import numpy as np

    points_array = np.array(points)  # shape (N,5)

    # Sort points by y first, then x (row-major)
    points_array = points_array[np.lexsort((points_array[:,1], points_array[:,2]))]

    x_vals = np.unique(points_array[:,1])
    y_vals = np.unique(points_array[:,2])

    # Check if points form a complete grid
    if len(points_array) != len(x_vals) * len(y_vals):
        raise ValueError("Points do not form a complete rectangular grid!")

    # Reshape to 2D grids
    lat_grid = points_array[:,3].reshape(len(y_vals), len(x_vals))
    lon_grid = points_array[:,4].reshape(len(y_vals), len(x_vals))

    # Find indices of surrounding points
    i = np.searchsorted(x_vals, x) - 1
    j = np.searchsorted(y_vals, y) - 1

    i = np.clip(i, 0, len(x_vals)-2)
    j = np.clip(j, 0, len(y_vals)-2)

    # Four corners of the cell
    x0, x1 = x_vals[i], x_vals[i+1]
    y0, y1 = y_vals[j], y_vals[j+1]

    lat00, lat10 = lat_grid[j, i], lat_grid[j, i+1]
    lat01, lat11 = lat_grid[j+1, i], lat_grid[j+1, i+1]

    lon00, lon10 = lon_grid[j, i], lon_grid[j, i+1]
    lon01, lon11 = lon_grid[j+1, i], lon_grid[j+1, i+1]

    # Bilinear interpolation
    tx = (x - x0) / (x1 - x0)
    ty = (y - y0) / (y1 - y0)

    lat = (1-ty)*((1-tx)*lat00 + tx*lat10) + ty*((1-tx)*lat01 + tx*lat11)
    lon = (1-ty)*((1-tx)*lon00 + tx*lon10) + ty*((1-tx)*lon01 + tx*lon11)

    return lat, lon
