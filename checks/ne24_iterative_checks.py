# Checks for NE 24 (Jacobi, Gauss-Seidel, SOR). Run: python ne24_iterative_checks.py
# Change the import to point at your own code. Expected, each returning (x, converged, iterations):
#   jacobi(A, b, tol, maxiter)    gauss_seidel(A, b, tol, maxiter)    sor(A, b, omega, tol, maxiter)
import math
import numpy as np
from my_iterative import jacobi, gauss_seidel, sor

def tridiag(n):
    return 2 * np.eye(n) - np.eye(n, k=1) - np.eye(n, k=-1)

rng = np.random.default_rng()
n = 50
A = rng.uniform(-1, 1, (n, n)) + n * np.eye(n)
b = rng.uniform(-1, 1, n)
print("1. It solves the system:")
for name, solve in [("Jacobi", jacobi), ("Gauss-Seidel", gauss_seidel)]:
    x, conv, k = solve(A, b, 1e-10, 1000)
    res = np.linalg.norm(b - A @ x) / np.linalg.norm(b)
    diff = np.linalg.norm(x - np.linalg.solve(A, b), np.inf)
    print(f"   {name}: converged = {conv}, iterations = {k}, residual = {res:.1e}, difference from built-in = {diff:.1e}")

T, ones = tridiag(20), np.ones(20)
_, _, kj = jacobi(T, ones, 1e-8, 100000)
_, _, kg = gauss_seidel(T, ones, 1e-8, 100000)
print(f"2. Gauss-Seidel vs Jacobi on the tridiagonal matrix: {kg} / {kj} = {kg / kj:.2f} (should be about 0.5)",
      "ok" if 0.4 < kg / kj < 0.6 else "FAIL")

xs, _, ks = sor(T, ones, 1.0, 1e-8, 100000)
xg, _, _ = gauss_seidel(T, ones, 1e-8, 100000)
print(f"3. SOR with omega = 1: {ks} iterations vs Gauss-Seidel {kg}",
      "ok" if ks == kg and np.allclose(xs, xg) else "FAIL")

w = 2 / (1 + math.sin(math.pi / 21))
_, _, kw = sor(T, ones, w, 1e-8, 100000)
print(f"4. SOR with omega = {w:.3f}: {kw} iterations, {kg / kw:.1f} times fewer than Gauss-Seidel (should be about 10)")

_, conv, k = jacobi(np.array([[1.0, 2.0], [2.0, 1.0]]), np.array([1.0, 1.0]), 1e-8, 50)
print(f"5. Honest failure: converged = {conv} after {k} iterations", "ok" if not conv else "FAIL")
