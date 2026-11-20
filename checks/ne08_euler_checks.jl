# Checks for NE 8 (Euler's method). Run: julia ne08_euler_checks.jl
# Change the include to point at your own code. Expected:
#   euler(f, x0, x1, y0, n) -> y at x1, using n equal steps, where f(x, y) is the right-hand side.
include("my_euler.jl")
using Printf

λ = -1.3
println("1. First-order convergence (ratio should approach 2):")
for n in (20, 40, 80, 160)
    e1 = abs(euler((x, y) -> λ * y, 0.0, 1.0, 1.0, n) - exp(λ))
    e2 = abs(euler((x, y) -> λ * y, 0.0, 1.0, 1.0, 2n) - exp(λ))
    @printf("   n = %4d: error ratio = %.3f %s\n", n, e1 / e2, 1.9 < e1 / e2 < 2.1 ? "ok" : "FAIL")
end

println("2. Exact on straight lines (error should be ~1e-15):")
for n in (1, 7, 100)
    err = euler((x, y) -> 3.0, 0.0, 1.0, 1.0, n) - 4.0
    @printf("   n = %3d: error = %.1e %s\n", n, err, abs(err) < 1e-12 ? "ok" : "FAIL")
end

# 3. Agreement with the library: add your own comparison with your library solver for part (a).
