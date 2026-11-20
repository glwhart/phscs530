# Checks for WU 25 (1D root finding). Run: julia wu25_rootfinding_checks.jl
# Change the include to point at your own code. Expected, each returning (root, f(root), evaluations):
#   bisection(f, a, b, tol, maxiter)    secant(f, x0, x1, tol, maxiter)
include("my_roots.jl")
using Printf

g(x) = x^2 - 2
println("1. Bisection takes the predicted number of steps (evaluations = halvings + up to 3 at the ends):")
for tol in (1e-3, 1e-6, 1e-10)
    r, fr, evals = bisection(g, 0.0, 2.0, tol, 200)
    pred = ceil(Int, log2(2 / tol))
    good = abs(r - √2) < tol && 0 <= evals - pred <= 3
    @printf("   tol = %.0e: %d evaluations, predicted halvings = %d, error = %.1e %s\n",
            tol, evals, pred, abs(r - √2), good ? "ok" : "FAIL")
end

print("2. Bisection refuses a bad interval: ")
try
    out = bisection(g, 2.0, 3.0, 1e-8, 200)
    println("returned ", out, " (should have thrown an error or returned a clear flag)")
catch err
    println("threw ", typeof(err), " ok")
end

println("3. Secant convergence order (should approach 1.6): record the error at each step yourself,")
println("   for example by printing x inside your secant function, then compute log(e[k+1]/e[k]) / log(e[k]/e[k-1]).")

const calls = Ref(0)
counted(x) = (calls[] += 1; g(x))
_, _, evals = secant(counted, 1.0, 2.0, 1e-12, 100)
@printf("4. Honest counting: secant reported %d evaluations, f was called %d times %s\n",
        evals, calls[], evals == calls[] ? "ok" : "FAIL")
