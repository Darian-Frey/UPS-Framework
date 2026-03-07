# research/p_vs_np/kronecker_stability_check.py
# Lead: Shane Hartley
#
# Numerical obstruction / stability mock-up for partitions of the form
#   λ = (n-8, 3, 2, 2, 1, 1)
# in the UPS / prismatic stability framework.
#
# This file is intentionally *symbolic*: multiplicities are mocked to
# encode the desired obstruction pattern:
#   m_λ(det_n)  = 0
#   m_λ(perm_n) > 0
# for the specific test partitions.

from dataclasses import dataclass
from typing import Tuple, Optional


Partition = Tuple[int, ...]


@dataclass
class StabilityData:
    n: int
    lam: Partition
    height: int
    theta: int
    det_wall_stable: bool
    is_prismatic_ghost: bool
    delta_pris: int
    m_det: Optional[int]
    m_perm: Optional[int]


def height(partition: Partition) -> int:
    """
    Height h(λ): number of nonzero parts.
    """
    return sum(1 for x in partition if x > 0)


def flip_invariant(partition: Partition) -> int:
    """
    Flip invariant Θ(λ) = sum_{i=2}^{h(λ)} λ_i.
    We implement this as the sum of all parts except the first.
    """
    return sum(partition[1:])


def check_determinant_wall(partition: Partition) -> bool:
    """
    Determinant Stability Wall:
      - Stable  (True)  if height h(λ) <= 5
      - Unstable(False) if height h(λ) >= 6
    """
    return height(partition) <= 5


def is_prismatic_ghost_for_det(partition: Partition, threshold: int = 8) -> bool:
    """
    A partition is a 'Prismatic Ghost for the Determinant' if
      Θ(λ) = sum_{i>=2} λ_i > threshold.
    Default threshold is 8.
    """
    return flip_invariant(partition) > threshold


def prismatic_discriminant(partition: Partition, threshold: int = 8) -> int:
    """
    Prismatic discriminant Δ_pris(λ):
      Δ_pris = max(0, Θ(λ) - threshold)
    so that Δ_pris > 0 flags a ghost beyond the determinant wall.
    """
    theta = flip_invariant(partition)
    return max(0, theta - threshold)


# --- Mock multiplicity layer -------------------------------------------------
# These are *not* computed Kronecker coefficients; they encode the intended
# obstruction pattern for the specific test partitions.

def multiplicity_det_mock(n: int, lam: Partition) -> Optional[int]:
    """
    Mock multiplicity m_λ(det_n):
      - For the target partitions, we enforce m_λ(det_n) = 0.
      - For all other inputs, return None (unknown).
    """
    targets = {
        8: (0, 3, 2, 2, 1, 1),
        9: (1, 3, 2, 2, 1, 1),
        12: (4, 3, 2, 2, 1, 1),
    }
    if n in targets and lam == targets[n]:
        return 0
    return None


def multiplicity_perm_mock(n: int, lam: Partition) -> Optional[int]:
    """
    Mock multiplicity m_λ(perm_n):
      - For the target partitions, we enforce m_λ(perm_n) > 0 (set to 1).
      - For all other inputs, return None (unknown).
    """
    targets = {
        8: (0, 3, 2, 2, 1, 1),
        9: (1, 3, 2, 2, 1, 1),
        12: (4, 3, 2, 2, 1, 1),
    }
    if n in targets and lam == targets[n]:
        return 1
    return None


def analyze_partition(n: int, lam: Partition) -> StabilityData:
    """
    Aggregate all numerical invariants for a given (n, λ).
    """
    h = height(lam)
    theta = flip_invariant(lam)
    det_stable = check_determinant_wall(lam)
    ghost = is_prismatic_ghost_for_det(lam)
    delta = prismatic_discriminant(lam)
    m_det = multiplicity_det_mock(n, lam)
    m_perm = multiplicity_perm_mock(n, lam)

    return StabilityData(
        n=n,
        lam=lam,
        height=h,
        theta=theta,
        det_wall_stable=det_stable,
        is_prismatic_ghost=ghost,
        delta_pris=delta,
        m_det=m_det,
        m_perm=m_perm,
    )


if __name__ == "__main__":
    # Target partitions:
    targets = [
        (8, (0, 3, 2, 2, 1, 1)),
        (9, (1, 3, 2, 2, 1, 1)),
        (12, (4, 3, 2, 2, 1, 1)),
    ]

    for n, lam in targets:
        data = analyze_partition(n, lam)
        print(f"n = {data.n}, λ = {data.lam}")
        print(f"  height h(λ)          = {data.height}")
        print(f"  Θ(λ)                 = {data.theta}")
        print(f"  det-wall stable?     = {data.det_wall_stable}")
        print(f"  prismatic ghost?     = {data.is_prismatic_ghost}")
        print(f"  Δ_pris(λ)            = {data.delta_pris}")
        print(f"  m_λ(det_n) (mock)    = {data.m_det}")
        print(f"  m_λ(perm_n) (mock)   = {data.m_perm}")
        print("-" * 60)
