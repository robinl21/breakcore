# Sketch-Effect Visual Generator

A Python-based tool for generating glitchy, sketch-like visuals using edge detection, blob tracking, and audio-synced animations.

---

## ROADMAP

### Completed
- [x] Image Layering with Transparency and Grain
- [x] Proportional Resize
- [x] Blob Detection with Circular Sketch Outlines and Tracking Lines

### In Progress
- [ ] Edge Tracing
- [ ] Windows

### Future Goals
- [ ] Animation
- [ ] Audio Syncing

---

## 🔍 Inspired Tools to Explore
- [remove.bg](https://www.remove.bg/) for background removal.

---

## 🎨 Sketch Effects and Techniques

### OpenCV’s Simple Blob Detection

#### Process
1. **Thresholding**
   - Converts source image to multiple binary images using incremental thresholds.
   - Detects blobs at different colors and intensities.
2. **Grouping**
   - Uses BFS to group connected white pixels.
   - Applies Gaussian blur → Laplacian operator to emphasize blob centers.
3. **Merging**
   - Merges blobs with nearby centers.
   - Returns updated blob centers and radii.

---

#### Blob Detection Parameters
- `minThreshold`: Lower threshold (default: 50)
- `maxThreshold`: Upper threshold (default: 220)
- `thresholdStep`: Step size between thresholds (default: 10)
- `filterByColor`: Enable/disable color filtering (default: true)
- `blobColor`: 0 = dark blobs, 255 = bright blobs
- `filterByArea`: Minimum and maximum blob size
- `filterByCircularity`: Filter by circular shape
- `filterByInertia`: Filter by elongation (1 = circular, 0 = elongated)
- `filterByConvexity`: Filter by convexity (1 = convex, 0 = concave)

---

#### 🔗 Blob Line Tracking Algorithms

##### 1. Random Pair

##### 2. Nearest Neighbors

##### 3. Delaunay Triangulation

##### 4. Minimum Spanning Tree (MST)

##### 5. Noise-Driven Selection

---

### Edge Tracing

## Edge Detection Methods
    Canny: Clean, thin edges. 

## Find Contours
    Using edges detected, connects and creates contours. 

## Add effects:
    Glitch. 
    Jitter.  
    RGB Split. 