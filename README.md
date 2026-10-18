# Chaotic Fractal Based RNG Algorithm

A software random number generator that uses chaotic dynamics inside a regular polygon. A point moves through the polygon under a nonlinear, deterministic rule, and its spatial evolution is encoded into a bitstream. The number of polygon sides acts as a tunable source of geometric complexity.

**Authors:** K Dhiraj, M Vaishnavi, Dr. Srisakthi Saravanan
School of Computer Science and Engineering (SCOPE), Vellore Institute of Technology, Chennai, India

---

## Overview

Traditional PRNGs rely on arithmetic recurrences, which can suffer from periodicity and predictability. Chaotic-map generators are sensitive to initial conditions but are often computationally heavy, deterministic if parameters leak, and sometimes fail statistical suites.

This project proposes a lightweight alternative that:

- Uses only basic math (trigonometry, XOR, bit shifts, modulo).
- Confines the state to a compact space (polygon x scalar interval), so trajectories never diverge.
- Treats polygon dimension (number of vertices) as an extra tunable parameter without changing the algorithm.

## How It Works

The algorithm has five stages (see Fig. 1 in the paper):

| Stage | Algorithm | Description |
|-------|-----------|-------------|
| 1 | Regular Polygon Initialization | Builds a regular n-gon (n >= 3) from edge length `a`: circumradius `R = a / (2 sin(pi/n))`, center, initial angle via `atan2`, and vertices sampled every `2pi/n`. |
| 2 | Next Point Generation | From the current point `P` and scalar `V`, builds a bidirectional ray along direction `theta`, finds the two boundary intersections, picks the farthest, and moves `P' = P + V (I* - P)`. Since `V < 1`, `P'` stays strictly inside the polygon. |
| 3 | Direction Determination | Quantizes `x`, `y` (`floor(1000x)`, `floor(1000y)`), XORs them, applies a shift/mask/XOR transform `((B << 3) & (2^16 - 1)) ^ (B >> 2)`, then `theta = B' mod 360`. |
| 4 | Next V Computation | `M = sin(pi x) + cos(e^y) + V`, take the fractional part, rescale: `V' = 0.1 + 0.899 * abs(M mod 1)`, keeping `V` in [0.1, 0.999]. |
| 5 | Binary Encoding | Scales coordinates by 10^4, computes `S = floor(x~ * y~)`, and outputs `bin(S)`. |

### State and inputs

- **State:** `(P, V)` in `Polygon x [0.1, 0.999]`
- **Seed:** an initial interior point `P0` and initial scalar `V0`
- **Parameters:** number of sides `n`, edge length `a`

## Theoretical Properties (summary)

- **Forward invariance and compactness:** the state space is compact and the update map keeps every trajectory inside it. No divergence or blow-up.
- **Local expansion:** `|dV'/dx| = 0.899 pi |cos(pi x)|` exceeds 1 on a set of positive measure, giving regions of exponential divergence.
- **Positive Lyapunov exponent / topological entropy:** argued for orbits that visit the expanding region with positive frequency (a lower-bound argument, not a full proof of chaos for all seeds).
- **Symbolic dynamics:** modular folding and direction quantization induce a symbolic encoding.

## Reported Results

| Evaluation | Result |
|------------|--------|
| NIST SP 800-22 (2^20 points, each (x, y) converted to a 32-bit string) | P-values above the 0.01 threshold on all tests reported (e.g. Approximate Entropy 0.534, Block Frequency 0.740, Cumulative Sums Fwd 0.637, FFT 0.534, Serial 0.388, Linear Complexity 0.213, Longest Run 0.122, Rank 0.122) |
| NIST SP 800-90B (non-IID, first 1M bits) | H_original = 7.638 bits/byte, H_bitstring = 0.8647 bits/bit |
| Assessed min-entropy | **6.918 bits per byte** (about 86.5% efficiency) |
| Polygon-degree study (Monobit) | Randomness increases with number of sides (degrees 4, 7, 10 tested) |
| Runtime | Scales linearly with number of iterations |

Tests listed for NIST SP 800-22: Frequency, Block Frequency, Runs, Longest Run of Ones, Rank, FFT, Approximate Entropy, Linear Complexity, Serial, Cumulative Sums.

## Visualization

Generated points are plotted with Python's `turtle` package, for example 100 points in a square (Fig. 2) and 500 points in an octagon (Fig. 3).

## Suggested Project Structure

```
.
├── README.md
├── polygon.py        # Algorithm 1: regular polygon initialization
├── next_point.py     # Algorithm 2: ray-polygon intersection and point update
├── direction.py      # Algorithm 3: XOR / bit-mix direction
├── next_v.py         # Algorithm 4: scalar V update
├── encode.py         # Algorithm 5: binary encoding
├── rng.py            # Main loop producing the bitstream
├── visualize.py      # Turtle-based plotting
└── tests/            # NIST SP 800-22 / 800-90B harness
```

*(Adjust to match your actual files.)*

## Usage (pseudocode)

```python
poly = init_polygon(a=..., n=...)        # Algorithm 1
P, V = seed_point, seed_V                # P strictly inside polygon, V in [0.1, 0.999]
bits = []
for _ in range(T):
    result = next_point(P, V, poly)      # Algorithms 2 and 3
    if result is None:
        break
    P, _ = result
    V = next_v(P, V)                     # Algorithm 4
    bits.append(encode(P))               # Algorithm 5
bitstream = "".join(bits)
```

## Testing

- **NIST SP 800-22:** run the official suite on the generated bitstream and check that P-values exceed 0.01.
- **NIST SP 800-90B:** use the non-IID entropy estimation tool on the output (the paper used the truncated 1M-bit option).

## Applications

Cryptographic key material, hashing salts/IVs and nonces, digital watermarking, Monte Carlo simulation, procedural generation in games, frequency-hopping sequences in wireless systems, and validator scheduling in blockchains.

## Limitations and Caveats

- The generator is **deterministic**: output is fully reproducible from the seed `(P0, V0)` and polygon parameters, so seeds must be kept secret and high-entropy for any security use.
- Min-entropy of about 6.9 bits/byte means raw output is not uniformly random; use a conditioner/extractor before cryptographic use.
- The authors note that further testing on standardized data is needed before cryptographic verification.
- Chaos claims (Lyapunov exponent, topological entropy) rely on conditions about orbit behavior rather than a complete proof.
- Floating-point precision can affect reproducibility across platforms.
- Do not use for production cryptography without independent review.

## Citation

```
K. Dhiraj, M. Vaishnavi, and S. Saravanan, "Chaotic Fractal Based RNG Algorithm,"
School of Computer Science and Engineering (SCOPE), Vellore Institute of Technology, Chennai, India.
```

## Contact

Corresponding author: Dr. Srisakthi Saravanan, srisakthi.saravanan@vit.ac.in
