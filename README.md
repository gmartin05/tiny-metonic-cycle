# tiny-metonic-cycle

Computes the 19-year Metonic cycle lunation alignment used to find the paschal full moon for movable-feast calculations.

```python
from tiny_metonic_cycle import MetonicCycle, compute_paschal_full_moon, compute_golden_number

cycle = MetonicCycle()
gn = cycle.golden_number(2024)        # GoldenNumber(11)
month, day = cycle.paschal_full_moon(2024)  # (3, 25) -> March 25
start = cycle.is_cycle_start(2025)   # False (2025 % 19 != 0)

# Or use the module-level shortcuts:
compute_golden_number(2024)          # GoldenNumber(11)
compute_paschal_full_moon(2024)      # (3, 25)
```

## Why this exists

Movable feasts like Easter are tied to the paschal full moon — the first ecclesiastical full moon after March 21. Rather than observing the moon astronomically each year, the Western computus uses a fixed 19-year table indexed by the golden number (\(year \bmod 19) + 1). This library implements that table lookup so calendar and liturgy software can compute paschal full-moon dates deterministically.

The trade-off is precision for stability. The tabulated dates drift from true astronomical full moons by up to a couple of days in some years. That drift is intentional: the Church adopted a fixed table so the answer is reproducible without a telescope. If you need astronomical accuracy, this library is the wrong tool.

## Exports

- `MetonicCycle` — stateless calculator class with methods `golden_number(year)`, `cycle_position(year)`, `paschal_full_moon(year)`, and `is_cycle_start(year)`.
- `GoldenNumber` — an `int` subclass constrained to 1–19.
- `compute_golden_number(year)` — module-level shortcut.
- `compute_paschal_full_moon(year)` — module-level shortcut returning `(month, day)` where month is 3 (March) or 4 (April).

## Edge cases

Year 0 is accepted and yields golden number 1, keeping the cycle continuous across the proleptic BC/AD boundary. Negative years work the same way — Python's modulo keeps results non-negative. Non-integer years raise `TypeError`; out-of-range golden numbers raise `ValueError`.

The paschal full-moon table is the Western (Gregorian) ecclesiastical convention. It does not match the Orthodox computus, which uses the Julian calendar and a different lunar correction.
