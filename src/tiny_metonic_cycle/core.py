"""Core implementation of the Metonic cycle lunation alignment.

The Metonic cycle is the observation that 235 synodic months (lunations)
are very nearly equal to 19 solar years. After 19 years, the phases of
the moon recur on the same calendar dates. This recurrence is the
foundation of computus — the calculation of Easter and other movable
feasts whose dates depend on the paschal full moon (the first full moon
after the ecclesiastical vernal equinox, fixed at March 21 in the
Western tradition).

We use the classic "golden number" scheme documented by the Venerable
Bede and standardised in medieval computistical tables. The golden
number for year Y is (Y mod 19) + 1, and it indexes a table of paschal
full-moon dates. These dates are the tabulated full moons used by the
Western (Gregorian/Julian) computus, not the astronomical full moons
observed at any particular longitude.

Astronomical precision is explicitly out of scope. The tabulated dates
are the ecclesiastical convention, and that is what movable-feast
calendars require.
"""


# The golden number cycle is 19 years. We represent it as 0..18
# internally so the modulo arithmetic is clean, then expose 1..19
# (the traditional numbering) via GoldenNumber.
_CYCLE_LENGTH = 19

# The 19 paschal full-moon dates in the Western computus, indexed by
# golden number minus one. Each entry is (month, day) where month is
# 3 (March) or 4 (April). These are the standard tabulated values used
# by the Gregorian computus since the 1582 reform; they match the
# Julian computus as well because the lunar equation is independent of
# the solar calendar correction.
#
# Why these specific dates? The Church settled on a fixed 19-year
# lunar table so that Easter could be computed reproducibly without
# astronomical observation. The dates below are the result of that
# table; they drift slowly relative to true astronomy, which is the
# whole point — a stable, agreed convention.
_PASCHAL_FULL_MOON = [
    (4, 14),  # GN  1
    (4, 3),   # GN  2
    (3, 23),  # GN  3
    (4, 11),  # GN  4
    (3, 31),  # GN  5
    (4, 18),  # GN  6
    (4, 8),   # GN  7
    (3, 28),  # GN  8
    (4, 16),  # GN  9
    (4, 5),   # GN 10
    (3, 25),  # GN 11
    (4, 13),  # GN 12
    (4, 2),   # GN 13
    (3, 22),  # GN 14
    (4, 10),  # GN 15
    (3, 30),  # GN 16
    (4, 17),  # GN 17
    (4, 7),   # GN 18
    (3, 27),  # GN 19
]


class GoldenNumber(int):
    """The golden number of a year in the 19-year Metonic cycle.

    Golden numbers run from 1 to 19. Two years share the same golden
    number if and only if they are 19 years apart. This is a subclass
    of ``int`` so it behaves naturally in arithmetic and comparisons,
    while carrying the semantic meaning of a cycle index.
    """

    __slots__ = ()

    def __new__(cls, value: int) -> "GoldenNumber":
        if not isinstance(value, int):
            raise TypeError("golden number must be an integer")
        if value < 1 or value > _CYCLE_LENGTH:
            raise ValueError(
                f"golden number must be in 1..{_CYCLE_LENGTH}, got {value}"
            )
        return super().__new__(cls, value)

    def __repr__(self) -> str:
        return f"GoldenNumber({int(self)})"


class MetonicCycle:
    """Compute the Metonic cycle position and paschal full moon for a year.

    This class is stateless; each method takes the year as an argument.
    It exists as a namespace so callers can hold a single instance and
    call methods on it, which is convenient when wiring the calculator
    into a larger computus pipeline.
    """

    __slots__ = ()

    def golden_number(self, year: int) -> GoldenNumber:
        """Return the golden number (1..19) for ``year``.

        The golden number is ``(year mod 19) + 1``. Year 0 conventionally
        yields golden number 1, which keeps the cycle continuous across
        the BC/AD boundary in the proleptic numbering used by
        computistical tables.
        """
        if not isinstance(year, int):
            raise TypeError("year must be an integer")
        return GoldenNumber((year % _CYCLE_LENGTH) + 1)

    def cycle_position(self, year: int) -> int:
        """Return the zero-based position (0..18) of ``year`` in the cycle.

        Position 0 corresponds to golden number 1. This is useful when
        indexing your own 19-element tables.
        """
        if not isinstance(year, int):
            raise TypeError("year must be an integer")
        return year % _CYCLE_LENGTH

    def paschal_full_moon(self, year: int) -> tuple[int, int]:
        """Return the (month, day) of the paschal full moon for ``year``.

        Month is 3 (March) or 4 (April). The date is the ecclesiastical
        tabulated full moon, not an astronomical observation.
        """
        gn = self.golden_number(year)
        return _PASCHAL_FULL_MOON[int(gn) - 1]

    def is_cycle_start(self, year: int) -> bool:
        """Return True if ``year`` is the first year of its Metonic cycle.

        A cycle starts when the golden number is 1, i.e. ``year % 19 == 0``.
        """
        if not isinstance(year, int):
            raise TypeError("year must be an integer")
        return year % _CYCLE_LENGTH == 0


def compute_golden_number(year: int) -> GoldenNumber:
    """Module-level convenience wrapper for :meth:`MetonicCycle.golden_number`."""
    return MetonicCycle().golden_number(year)


def compute_paschal_full_moon(year: int) -> tuple[int, int]:
    """Module-level convenience wrapper for :meth:`MetonicCycle.paschal_full_moon`."""
    return MetonicCycle().paschal_full_moon(year)
