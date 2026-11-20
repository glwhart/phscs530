# Example checks

Some handouts end with "Checks your code must pass". Those checks are written so you can do them in any
language. These files are examples in Julia and Python. Each one calls your own functions: change the
`include` or `import` line at the top to point at your code, then run it. "ok" means a check passed.
"FAIL" means your code is probably wrong; look for the bug before you submit.

| File | Assignment | Your functions |
|---|---|---|
| `ne08_euler_checks.*` | NE 8, Euler's method | `euler(f, x0, x1, y0, n)` |
| `ne24_iterative_checks.*` | NE 24, Jacobi, Gauss-Seidel, SOR | `jacobi(A, b, tol, maxiter)`, `gauss_seidel(...)`, `sor(A, b, ω, tol, maxiter)` |
| `wu25_rootfinding_checks.*` | WU 25, 1D root finding | `bisection(f, a, b, tol, maxiter)`, `secant(f, x0, x1, tol, maxiter)` |

If your functions take their arguments in a different order or return different things, adjust the
calls in the check file, not your method.
