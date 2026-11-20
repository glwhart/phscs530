# Checks for WU 25 (1D root finding). Run: python wu25_rootfinding_checks.py
# Change the import to point at your own code. Expected, each returning (root, f(root), evaluations):
#   bisection(f, a, b, tol, maxiter)    secant(f, x0, x1, tol, maxiter)
import math
from my_roots import bisection, secant

g = lambda x: x * x - 2
print("1. Bisection takes the predicted number of steps (evaluations = halvings + up to 3 at the ends):")
for tol in [1e-3, 1e-6, 1e-10]:
    r, fr, evals = bisection(g, 0.0, 2.0, tol, 200)
    pred = math.ceil(math.log2(2 / tol))
    good = abs(r - math.sqrt(2)) < tol and 0 <= evals - pred <= 3
    print(f"   tol = {tol:.0e}: {evals} evaluations, predicted halvings = {pred},",
          f"error = {abs(r - math.sqrt(2)):.1e}", "ok" if good else "FAIL")

print("2. Bisection refuses a bad interval:", end=" ")
try:
    out = bisection(g, 2.0, 3.0, 1e-8, 200)
    print("returned", out, "(should have raised an error or returned a clear flag)")
except Exception as err:
    print("raised", type(err).__name__, "ok")

print("3. Secant convergence order (should approach 1.6): record the error at each step yourself,")
print("   for example by printing x inside your secant function, then compute ln(e[k+1]/e[k]) / ln(e[k]/e[k-1]).")

calls = 0
def counted(x):
    global calls
    calls += 1
    return g(x)
_, _, evals = secant(counted, 1.0, 2.0, 1e-12, 100)
print(f"4. Honest counting: secant reported {evals} evaluations, f was called {calls} times",
      "ok" if evals == calls else "FAIL")
