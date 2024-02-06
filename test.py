def set_values(matrix, center_point, max_distance, max_value):
    """
    Sets values in a matrix based on the distance from a center point.

    Parameters:
    - matrix: The input matrix (list of lists)
    - center_point: Tuple (row, col) representing the center point
    - max_distance: The maximum distance to consider
    - max_value: The maximum absolute value to assign at the center point

    Returns:
    - A new matrix with values set based on distance from the center point
    """
    rows = len(matrix)
    cols = len(matrix[0])
    result_matrix = [[0] * cols for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            distance = ((i - center_point[0]) ** 2 + (j - center_point[1]) ** 2) ** 0.5
            value = max_value * (1 - distance / max_distance) if distance <= max_distance else 0
            result_matrix[i][j] = max(-max_value, min(max_value, value))

    return result_matrix

# Example usage:
matrix_size = 5
center = (2, 2)
max_dist = 2.5
max_val = -1.0

matrix = [[0] * matrix_size for _ in range(matrix_size)]
result = set_values(matrix, center, max_dist, max_val)

print("Input Matrix:")
for row in matrix:
    print(row)
print("\nResult Matrix:")
for row in result:
    print(row)
