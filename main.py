from sep.round import RoundSeparator

R, L, n = list(map(float, input().split()))
n = int(n)

if __name__ == "main":
    sep = RoundSeparator(R,L,n)
    coeffs = sep.calc_ac()
    k = sep.calc_clausing(coeffs)