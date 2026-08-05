def pixel_distance(point_a, point_b, width, height):
    """Calcula la distancia en pixeles entre dos landmarks normalizados."""
    delta_x = (point_a.x - point_b.x) * width
    delta_y = (point_a.y - point_b.y) * height

    return (delta_x**2 + delta_y**2) ** 0.5


def opening_ratio(
    face,
    top_index,
    bottom_index,
    left_index,
    right_index,
    width,
    height,
):
    """Compara la apertura vertical de un rasgo con su anchura."""
    opening = pixel_distance(
        face[top_index],
        face[bottom_index],
        width,
        height,
    )
    feature_width = pixel_distance(
        face[left_index],
        face[right_index],
        width,
        height,
    )

    if feature_width == 0:
        return 0.0

    return opening / feature_width

