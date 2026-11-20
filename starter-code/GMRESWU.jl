using LinearAlgebra
A = [6 2 1; 2 3 1; 1 1 1]
b1 = [1, 2, 0]
x0 = [0, 0, 0]
r0 = b1 - A*x0
β = norm(r0)
H = zeros(4,3)

q1 = r0/β
v = A*q1
H[1,1] = q1⋅v
q2 = v - H[1,1]*q1
abs(q1⋅q2) < 1e-14 # Yep
H[2,1] = norm(q2)
q2 /= H[2,1]

# H[:2,:1] x - β )
y = H[1:2,1:1]\[β,0]
x1 = x0 + q1*y[1]
r = b1 - A*x1

v = A*q2
H[1,2] = v⋅q1
v -= H[1,2]*q1
H[2,2] = q2⋅v
v -= H[2,2]*q2
v⋅q1 < 1e-14 # Yep
v⋅q2 < 1e-14 # Yep
H[3,2] = norm(v)
q3 = v/H[3,2]

y = H[1:3,1:2]\[β,0,0]
x2 = x0 + hcat(q1,q2)*y
r2 = b1 - A*x2

v = A*q3
H[1,3] = v⋅q1
v -= H[1,3]*q1
H[2,3] = v⋅q2
v -= H[2,3]*q2
H[3,3] = v⋅q3
v -= H[3,3]*q3
H[4,3] = norm(v)

y = H[1:4,1:3]\[β,0,0,0]
x3 = x0 + hcat(q1,q2,q3)*y
r3 = b1 - A*x3                          

x1
x2