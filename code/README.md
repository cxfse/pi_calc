# Pi Computation using d=427 Ramanujan-Type Formula

This repository contains the engineering implementations for the ultra-fast Ramanujan-type series based on the discriminant $d=427$. The formula operates over the algebraic integer ring $\mathbb{Z}[\sqrt{61}]$ and achieves an unprecedented net convergence rate of **24.96 decimal digits per term**.

## Directory Structure

- `D427_1M_Verify/`: Contains the script to verify $\pi$ to 1,000,000 decimal digits.
- `D427_10M_Verify/`: Contains the script to verify $\pi$ to 10,000,000 decimal digits.
- `D427_100M_Verify/`: Contains the script to verify $\pi$ to 100,000,000 decimal digits.

Each directory contains a self-contained, runnable Python script that executes the calculation and exports the results to a local `.txt` file.

## Prerequisites

The scripts require Python 3 and the `gmpy2` library for arbitrary-precision arithmetic.

```bash
pip install gmpy2
```

## Execution Instructions

Navigate to any of the directories and run the corresponding script. For example, to verify the 1 Million digit calculation:

```bash
cd D427_1M_Verify
python verify_1M.py
```

### Expected Output
The script will calculate $\pi$ using the Binary Splitting algorithm combined with Karatsuba ring optimization. Upon completion, it will:
1. Output the matrix fold time and the final division/sqrt projection time.
2. Write the exact computed digits to a `.txt` file in the same directory (e.g., `pi_1M.txt`).
3. Print the last 4 decimal digits of the computed result to the console for quick visual verification.

## Methodological Highlights
These engineering scripts reflect the theoretical breakthroughs described in our paper. They utilize:
1. **Binary Splitting Algorithm**: Ensuring an $O(N \log^3 N)$ overall time complexity.
2. **Karatsuba Ring Optimization**: Reducing the number of large integer multiplications in the $\mathbb{Z}[\sqrt{61}]$ ring from 4 down to 3 per multiplication step.
3. **Floating-Point Isolation**: The millions of iterations are executed entirely within the exact integer domain. The high-precision square root and division are delayed until the very final step, fundamentally eliminating any accumulated truncation errors.
