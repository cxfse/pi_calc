# Pi Calculation via d=427 Ramanujan-Type Formula

This repository contains the implementation and theoretical documentation for a new hypergeometric series used to compute Pi ($\pi$). Based on the discriminant $d=427$ (class number $h=2$), this formula achieves a theoretical convergence rate of **24.96 digits per term**.

## The Formula

The newly discovered equation operates in the algebraic extension field $\mathbb{Q}(\sqrt{61})$:

$$
\frac{1}{\pi} = \frac{12}{\sqrt{|C_{427}|}} \sum_{n=0}^{\infty} \frac{(-1)^n (6n)!}{(3n)! (n!)^3} \cdot \frac{A + B \cdot n}{C_{427}^n}
$$

Where the base $C_{427}$ and the algebraic integer constants $A$ and $B$ strictly reside in the ring $\mathbb{Z}[\sqrt{61}]$:

- **$C_{427}$** $= -(7805727756261891959906304000 + 999421027517377348595712000\sqrt{61})$
- **$A$** $= 1657145277365 + 212175710912\sqrt{61}$
- **$B$** $= 107578229802750 + 13773980892672\sqrt{61}$

## Repository Structure

- **[`code/`](./code/)**: Contains the Python implementations for verifying the formula.
  - Includes isolated test environments for 1 Million, 10 Million, and 100 Million digits.
  - Utilizes Binary Splitting and Karatsuba Ring-Multiplication (3-mul) optimizations in the $\mathbb{Z}[\sqrt{61}]$ algebraic ring.
  - *See [`code/README.md`](./code/README.md) for detailed running instructions.*
- **[`doc/`](./doc/)**: Contains the academic papers detailing the theoretical foundation.
  - **English Paper**: `Pi_Formula_d427_Paper.pdf`
  - **Chinese Paper**: `Pi_Formula_d427_Paper_cn.pdf`

## Highlights

- **Theoretical Rate**: Surpasses the Chudnovsky algorithm ($d=163, h=1$, 14.18 digits/term) in theoretical convergence speed.
- **Engineering Verification**: Successfully verified up to 100,000,000 digits with exact Bit-Perfect matching against established Pi benchmarks.
- **Absolute Precision**: Eliminates floating-point Newton iteration in the intermediate steps, relying entirely on exact large integer arithmetic via `gmpy2`.

## Quick Start

To run the verification scripts, ensure you have Python installed along with the `gmpy2` library:

```bash
pip install gmpy2
```

Navigate to the `code/` directory and run the desired verification script:

```bash
cd code/D427_1M_Verify
python verify_1M.py
```

## Author
Xingfeng Chen - Independent Researcher
