import sys
import time
import gmpy2
from gmpy2 import mpz

# Elevate integer string conversion limit for extreme precision
sys.set_int_max_str_digits(200000000)

# ============================================================
# Karatsuba-optimized Ring61 (3 multiplications per ring multiply)
# (x1+y1√61)(x2+y2√61) = (ac + 61·bd) + ((a+b)(c+d) - ac - bd)√61
# ============================================================
class Ring61Karatsuba:
    __slots__ = ['x', 'y']
    def __init__(self, x, y):
        self.x = mpz(x)
        self.y = mpz(y)
    
    def __add__(self, other):
        if isinstance(other, Ring61Karatsuba):
            return Ring61Karatsuba(self.x + other.x, self.y + other.y)
        return Ring61Karatsuba(self.x + mpz(other), self.y)
    
    def __mul__(self, other):
        if isinstance(other, Ring61Karatsuba):
            ac = self.x * other.x
            bd = self.y * other.y
            abcd = (self.x + self.y) * (other.x + other.y)
            return Ring61Karatsuba(ac + 61 * bd, abcd - ac - bd)
        other_mpz = mpz(other)
        return Ring61Karatsuba(self.x * other_mpz, self.y * other_mpz)
    
    def __rmul__(self, other): return self.__mul__(other)
    def __radd__(self, other): return self.__add__(other)

# ============================================================
# d=-427 Constants with Karatsuba-optimized Ring61
# ============================================================
C427K = Ring61Karatsuba(mpz("-7805727756261891959906304000"), mpz("-999421027517377348595712000"))
A427K = Ring61Karatsuba(mpz("1657145277365"), mpz("212175710912"))
B427K = Ring61Karatsuba(mpz("107578229802750"), mpz("13773980892672"))

# ============================================================
# Binary Splitting Algorithm for d=-427
# ============================================================
def bs_427_k(a, b):
    if b - a == 1:
        if a == 0:
            return mpz(1), mpz(1), A427K
        else:
            p = mpz(24) * mpz(6*a - 5) * mpz(6*a - 1) * mpz(2*a - 1)
            q = C427K * mpz(a)**3
            r = p * (A427K + B427K * a)
            return p, q, r
    m = (a + b) // 2
    pam, qam, ram = bs_427_k(a, m)
    pmb, qmb, rmb = bs_427_k(m, b)
    return pam * pmb, qam * qmb, ram * qmb + rmb * pam

def run_benchmark(digits, output_file):
    print(f"\nBenchmarking {digits:,} decimal digits of Pi for d=-427")
    n_427 = int(digits / 24.955) + 1
    print(f"Required Terms: {n_427:,}")
    
    t0 = time.perf_counter()
    P4k, Q4k, R4k = bs_427_k(0, n_427)
    t_427k = time.perf_counter() - t0
    print(f"Binary Splitting Matrix Fold Time: {t_427k:.3f} seconds")
    
    # ------------------------------------------------------------
    # Final Evaluation (High Precision Division & Sqrt)
    # ------------------------------------------------------------
    prec_bits = int(digits * 3.321928094887362) + 256
    gmpy2.get_context().precision = prec_bits
    
    t1 = time.perf_counter()
    sqrt_61 = gmpy2.sqrt(gmpy2.mpfr(61))
    
    R_val = gmpy2.mpfr(R4k.x) + gmpy2.mpfr(R4k.y) * sqrt_61
    Q_val = gmpy2.mpfr(Q4k.x) + gmpy2.mpfr(Q4k.y) * sqrt_61
    
    abs_C_Re = mpz("7805727756261891959906304000")
    abs_C_Im = mpz("999421027517377348595712000")
    abs_C_val = gmpy2.mpfr(abs_C_Re) + gmpy2.mpfr(abs_C_Im) * sqrt_61
    
    calc_pi = (gmpy2.sqrt(abs_C_val) * Q_val) / (gmpy2.mpfr(12) * R_val)
    t_eval = time.perf_counter() - t1
    print(f"Final Division & Sqrt Time: {t_eval:.3f} seconds")
    
    # Format to exact digits and wrap at 100 characters per line
    pi_str = f"{calc_pi:.{digits}f}"
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, output_file)
    
    with open(output_path, "w") as f:
        # Separate '3.' from the decimal part
        integer_part, decimal_part = pi_str.split('.')
        f.write(f"{integer_part}.\n")
        
        # Write decimal part in chunks of 100 characters
        for i in range(0, len(decimal_part), 100):
            chunk = decimal_part[i:i+100]
            f.write(f"{chunk}\n")
    
    print(f"Successfully wrote {digits:,} digits to {output_path}")
    
    last_4_digits = pi_str[-4:]
    print(f"\n========================================")
    print(f"Target Digits: {digits:,}")
    print(f"Last 4 digits: {last_4_digits}")
    print(f"========================================\n")

if __name__ == '__main__':
    run_benchmark(100000000, "pi_100M.txt")
