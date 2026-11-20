# Checks for NE 24 (Jacobi, Gauss-Seidel, SOR). Run: julia ne24_iterative_checks.jl
# Change the include to point at your own code. Expected, each returning (x, converged, iterations):
#   jacobi(A, b, tol, maxiter)    gauss_seidel(A, b, tol, maxiter)    sor(A, b, ω, tol, maxiter)
include("my_iterative.jl")
using LinearAlgebra, Printf

tridiag(n) = 2I(n) - diagm(1 => ones(n - 1), -1 => ones(n - 1))

n = 50
A = 2rand(n, n) .- 1 + n * I
b = 2rand(n) .- 1
println("1. It solves the system:")
for (name, solve) in (("Jacobi", jacobi), ("Gauss-Seidel", gauss_seidel))
    x, conv, k = solve(A, b, 1e-10, 1000)
    @printf("   %s: converged = %s, iterations = %d, residual = %.1e, difference from built-in = %.1e\n",
            name, conv, k, norm(b - A * x) / norm(b), norm(x - A \ b, Inf))
end

T, o = Matrix{Float64}(tridiag(20)), ones(20)
_, _, kj = jacobi(T, o, 1e-8, 100_000)
xg, _, kg = gauss_seidel(T, o, 1e-8, 100_000)
@printf("2. Gauss-Seidel vs Jacobi on the tridiagonal matrix: %d / %d = %.2f (should be about 0.5) %s\n",
        kg, kj, kg / kj, 0.4 < kg / kj < 0.6 ? "ok" : "FAIL")

xs, _, ks = sor(T, o, 1.0, 1e-8, 100_000)
@printf("3. SOR with ω = 1: %d iterations vs Gauss-Seidel %d %s\n", ks, kg, ks == kg && xs ≈ xg ? "ok" : "FAIL")

ω = 2 / (1 + sin(π / 21))
_, _, kw = sor(T, o, ω, 1e-8, 100_000)
@printf("4. SOR with ω = %.3f: %d iterations, %.1f times fewer than Gauss-Seidel (should be about 10)\n", ω, kw, kg / kw)

_, conv, k = jacobi([1.0 2.0; 2.0 1.0], [1.0, 1.0], 1e-8, 50)
@printf("5. Honest failure: converged = %s after %d iterations %s\n", conv, k, conv ? "FAIL" : "ok")
