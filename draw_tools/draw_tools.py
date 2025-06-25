import cv2
import numpy as np
import math

class DrawParams():
    def __init__(self, color=(0, 0, 255), thickness=2, lineType=cv2.LINE_AA, noise=(0,0), grain=(0,0), num_connections=10, alg="random"):
        self.color = color
        self.thickness = thickness
        self.lineType = lineType
        self.noise = noise
        self.grain = grain

        # tracking specific
        self.num_connections = num_connections
        self.alg = alg

def add_grain(image, grain):
    """
    MUTATOR.
    Adds film-like grain to an RGB image.
    
    Args:
        image (np.ndarray): RGB image (H x W x 3) dtype=uint8
        intensity (int): Noise strength (0–255)
        alpha (float): Blending factor for grain visibility
    """
    h, w, c = image.shape
    
    # Create random noise: same shape, values in [-intensity, intensity]
    noise = np.random.randint(grain[0], grain[1], (h, w, 1), dtype=np.int16)
    
    # Repeat noise across 3 channels (R, G, B)
    noise = np.repeat(noise, 3, axis=2)

    # Add noise to original image
    noisy = image.astype(np.int16) + noise

    # Clip to [0, 255] to avoid wraparound and convert back to uint8
    noisy = np.clip(noisy, 0, 255).astype(np.uint8)

    # Blend original and noisy image to soften effect
    image[:] = cv2.addWeighted(image, 1 - 0.5, noisy, 0.5, 0)


def draw_circle(image, center, radius, drawParams: DrawParams, seed, no_grain=True):
    """
    MUTATOR.
    Draws a noisy circle on an RGB image.
    """
    cx, cy = center

    # 100 points over circle
    angles = np.linspace(0, 2 * np.pi, 100, endpoint=False)

    points = []
    rng = np.random.default_rng(seed=seed)
    for theta in angles:
        # stretch out or in according to min and max noise
        noisy_r = radius + rng.uniform(drawParams.noise[0], drawParams.noise[1])
        x = int(cx + noisy_r * np.cos(theta))
        y = int(cy + noisy_r * np.sin(theta))
        points.append((x, y))

    pts = np.array(points, dtype=np.int32).reshape((-1, 1, 2))

    # for grain, we use white on a 2D array
    cv2.polylines(image, [pts], isClosed=True, color=drawParams.color if no_grain else (255, 255, 255), thickness=drawParams.thickness, lineType=drawParams.lineType)


def random_pairing(keypoints, num_connections, seed):
    """
    Randomly pairs keypoints
    """
    connections = set()
    rng = np.random.default_rng(seed=seed)
    max_connections = min(num_connections, math.comb(len(keypoints), 2))

    # TODO: this is too slow if we saturate graph
    while len(connections) < max_connections:
        a, b = rng.choice(keypoints, size=2, replace=False)
        if (a, b) not in connections and (b, a) not in connections:
            connections.add((a, b))
    return list(connections)

def draw_tracking(image, keypoints, drawParams: DrawParams, seed, no_grain=True):
    """
    MUTATOR.
    Draws lines between keypoints on RGB image

    Various algorithms:
    - Random pairing
    - Nearest neighbor

    """
    if drawParams.alg == "random":
        lines = random_pairing(keypoints, drawParams.num_connections, seed)
        for a, b in lines:
            # Draw line between keypoints
            cv2.line(image, (int(a.pt[0]), int(a.pt[1])), (int(b.pt[0]), int(b.pt[1])), drawParams.color if no_grain else (255, 255, 255), drawParams.thickness, drawParams.lineType)

    