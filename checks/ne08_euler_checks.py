# Checks for NE 8 (Euler's method). Run: python ne08_euler_checks.py
# Change the import to point at your own code. Expected:
#   euler(f, x0, x1, y0, n) -> y at x1, using n equal steps, where f(x, y) is the right-hand side.
import math
from my_euler import euler

lam = -1.3
print("1. First-order convergence (ratio should approach 2):")
for n in [20, 40, 80, 160]:
    e1 = abs(euler(lambda x, y: lam * y, 0.0, 1.0, 1.0, n) - math.exp(lam))
    e2 = abs(euler(lambda x, y: lam * y, 0.0, 1.0, 1.0, 2 * n) - math.exp(lam))
    print(f"   n = {n:4d}: error ratio = {e1 / e2:.3f}", "ok" if 1.9 < e1 / e2 < 2.1 else "FAIL")

print("2. Exact on straight lines (error should be ~1e-15):")
for n in [1, 7, 100]:
    err = euler(lambda x, y: 3.0, 0.0, 1.0, 1.0, n) - 4.0
    print(f"   n = {n:3d}: error = {err:.1e}", "ok" if abs(err) < 1e-12 else "FAIL")

# 3. Agreement with the library: add your own comparison with your library solver for part (a).
