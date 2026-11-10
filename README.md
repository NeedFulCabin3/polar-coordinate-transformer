# Polar Coordinate Transformer

> Vectorized coordinate transformation and spatial validation engine in Python.

## Overview

In spatial computing, robotics simulation, and geometric data pipelines, converting raw polar coordinate datasets $(r, \theta)$ into Cartesian $(x, y)$ representations frequently introduces performance bottlenecks when handled via iterative loops. This utility addresses computational friction by leveraging vectorized NumPy array operations to process batch coordinate transformations instantly, complete with type safety and spatial boundary validation.

## How It Works

The internal workflow relies on vectorized array computing rather than element-by-element iteration:
1. **Data Ingestion:** Coordinates are collected either interactively via terminal inputs or supplied directly as array-like structures.
2. **Dimension & Constraint Validation:** Inputs are cast into 64-bit float NumPy arrays, validating shape dimensions `(N, 2)` and enforcing non-negative radial distance constraints ($r \ge 0$).
3. **Trigonometric Mapping:** Depending on user configuration, angle inputs are converted from degrees to radians using `np.radians`.
4. **Vectorized Transformation:** Cartesian coordinates are computed simultaneously across the entire array using `np.cos` and `np.sin`, delegating heavy mathematical lifting to underlying compiled C routines.
5. **Spatial Filtering:** Transformed points are evaluated against an immutable `SpatialBounds` bounding box using boolean mask arrays to extract valid spatial subsets.

## Key Features

* **Fully Vectorized Batch Processing:** Transforms large arrays of polar points in a single vectorized pass without Python loop overhead.
* **Immutable Spatial Bounding:** Utilizes frozen dataclasses (`SpatialBounds`) to manage geometric filter limits reliably.
* **Strict Type Safety & Error Handling:** Comprehensive validation checks for incorrect array shapes, negative radii, and malformed terminal inputs.
* **Interactive CLI Interface:** Built-in terminal runner enabling rapid manual coordinate entry and inspection.

## Tech Stack & Core Dependencies Breakdown

* **Python 3.10+:** Utilized for modern type hinting support (`Union`, `List`, `Tuple`) and clean dataclass syntax.
* **NumPy:** Selected for high-performance array manipulation, contiguous memory layouts, and optimized C-backend trigonometric calculations.
* **Standard Library (`dataclasses`, `typing`):** Provides clean domain modeling without external framework bloat.

## Environment & Web-Based Quick Start

### GitHub Codespaces
1. Click **Code** -> **Codespaces** -> **Create codespace on main** in your GitHub repository.
2. Once the container spins up, open your terminal.

### Local Environment Setup (`venv`)
```bash
# Clone repository
git clone [https://github.com/your-username/polar-coordinate-transformer.git](https://github.com/your-username/polar-coordinate-transformer.git)
cd polar-coordinate-transformer

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install dependencies
pip install numpy
```

### Execution
Run the interactive script:

```Bash
python main.py
```
## Repository Structure

```bash
polar-coordinate-transformer/
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── README.md
└── main.py
```

## Roadmap
**[ ] Type Stub Integration (.pyi):** Introduce dedicated type stub files to enhance static analysis support for downstream consumers.

**[ ] Async I/O Pipeline Migration:** Adapt the ingestion layer to support asynchronous stream processing for real-time sensor data feeds.

**[ ] Structured Logging Integration:** Replace standard print statements with structured logging handlers for production observability.