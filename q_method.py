# to find simplified boolean expression
from sympy import symbols, Not, simplify_logic, Xor
from sympy.logic.boolalg import And, Or

def minterm_to_expr(minterm_bin, variables):
    term = []
    for i, bit in enumerate(minterm_bin):
        if bit == '1':
            term.append(variables[i])
        else:
            term.append(Not(variables[i]))
    return And(*term)

def try_detect_xor(minterms, num_vars, variables):
    xor_like = [i for i in range(2 ** num_vars) if bin(i).count('1') % 2 == 1]
    xnor_like = [i for i in range(2 ** num_vars) if bin(i).count('1') % 2 == 0]
    if sorted(minterms) == xor_like:
        return 'XOR', Xor(*variables)
    elif sorted(minterms) == xnor_like:
        return 'XNOR', Not(Xor(*variables))
    return None, None

def main():
    input_str = input("Enter minterms (space separated): ")
    try:
        minterms = list(map(int, input_str.strip().split()))
        if not minterms:
            return
    except:
        return

    max_val = max(minterms)
    num_vars = max_val.bit_length()
    var_names = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    variables = symbols(' '.join(var_names[:num_vars]))

    minterm_exprs = []
    for m in minterms:
        bin_str = format(m, f'0{num_vars}b')
        minterm_exprs.append(minterm_to_expr(bin_str, variables))

    sop_expr = Or(*minterm_exprs)
    simplified = simplify_logic(sop_expr, form='dnf')
    kind, smart_expr = try_detect_xor(minterms, num_vars, variables)

    print("Simplified Boolean Expression:")
    print(simplified)
    if smart_expr:
        print(f"{kind} Detected:")
        print(smart_expr)

if __name__ == "__main__":
    main()

