# Data files

Data the handouts ask you to load. Files with both a Julia (`.jld2`) and a Python (`.npz`) version hold
the same data.

## In this folder

| File | Assignment |
|---|---|
| `NoisyFunction.dat` | WU 1, preliminaries |
| `noisy-data.csv` | NE 14, basic fitting |
| `renumFCC-k2-reducedm.jld2`, `renumFCC-k2-reducedm-python.npz` | NE 19, QR |
| `weathered-face.jpg` | NE 21, SVD and NMF |
| `LEDfailures.csv` | NE 29, nonlinear fitting |
| `convexoptimization-x0.txt` | NE 30, convex optimization |

## Large files: download from the release

These are too large to keep in the repository. Download the ones you need from
<https://github.com/glwhart/phscs530/releases/tag/data> into this folder.

| File | Size | Assignment |
|---|---|---|
| `LUDecompJulia.jld2`, `LUDecompM1.npz` | 8 MB each | WU 16, LU decomposition |
| `preconditioningWUjulia.jld2`, `preconditioningWUpython.npz` | 8 MB each | WU 23, preconditioning |
| `fittingRealData-julia.jld2`, `fittingRealData-python.npz` | 44 MB each | NE 17 and NE 19, fitting real data |
| `renumFCC-k2-mwide.jld2`, `renumFCC-k2-mwide-python.npz` | 56 MB each | NE 19, QR |

With the GitHub command-line tool you can fetch one directly, for example
`gh release download data -R glwhart/phscs530 -p LUDecompM1.npz -D data`.
