"""Test k_n pattern: 1/Fibonacci vs 1/phi^n"""
import math

phi = (1 + math.sqrt(5)) / 2
fib = [1, 1, 2, 3, 5, 8, 13]
user = [1.0, 0.7, 0.5, 0.3, 0.2, 0.1, 0.05]

print("k_n pattern comparison:")
print(f"{'step':6s} {'user':8s} {'1/Fib':8s} {'1/phi^n':10s} {'diff_Fib':10s} {'diff_phi':10s}")
for i in range(7):
    fib_k = 1.0 / fib[i]
    phi_k = 1.0 / (phi ** (i + 0.5))
    d_fib = abs(user[i] - fib_k)
    d_phi = abs(user[i] - phi_k)
    print(f"{i+1:5d}  {user[i]:7.3f} {fib_k:7.3f} {phi_k:9.3f}  {d_fib:9.4f}  {d_phi:9.4f}")

# Best fit
print()
print("Best fit analysis:")
print(f"  Total |user - 1/Fib| = {sum(abs(user[i] - 1.0/fib[i]) for i in range(7)):.4f}")
print(f"  Total |user - 1/phi^n| = {sum(abs(user[i] - 1.0/(phi**(i+0.5))) for i in range(7)):.4f}")
