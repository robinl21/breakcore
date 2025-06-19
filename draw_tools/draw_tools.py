import cv2
import numpy as np

class DrawParams():
    def __init__(self, color=(0, 0, 255), thickness=2, lineType=cv2.LINE_AA, noise=(0,0), grain=(0,0)):
        self.color = color
        self.thickness = thickness
        self.lineType = lineType
        self.noise = noise
        self.grain = grain

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

    print("Noise", noise)
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

    Returns one normal and one b/w image
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