from scipy.optimize import linprog

# Coeficienții funcției obiectiv (profit net pe unitate - vrem să maximizăm)
profit_per_unit = [-30, -50, -25]  # folosim minus pentru că linprog minimizează

# Matricea A pentru constrângeri de tip „<=”
A = [
    [40, 60, 30],    # cost total <= buget
    [-1,  0,  0],    # x1 >= 500  -> -x1 <= -500
    [ 0, -1,  0],    # x2 >= 300
    [ 0,  0, -1],    # x3 >= 400
    [ 1,  0,  0],    # x1 <= 3000
    [ 0,  1,  0],    # x2 <= 2000
    [ 0,  0,  1],    # x3 <= 2500
]

# Vectorul b corespunzător lui A
b = [
    200000,  # buget
    -500,    # x1 >= 500
    -300,    # x2 >= 300
    -400,    # x3 >= 400
    3000,    # x1 <= 3000
    2000,    # x2 <= 2000
    2500     # x3 <= 2500
]

# Limitările variabilelor (cantități pozitive)
bounds = [(0, None), (0, None), (0, None)]

# Rezolvăm problema de optimizare liniară
result = linprog(c=profit_per_unit, A_ub=A, b_ub=b, bounds=bounds, method="highs")

# Extragem soluția
quantities = result.x if result.success else None
total_profit = -result.fun if result.success else None

print(f"Cantități: {quantities}")
print(f"Profit total: {total_profit}")

