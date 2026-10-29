import unittest

from tiny_metonic_cycle import (
    MetonicCycle,
    GoldenNumber,
    compute_paschal_full_moon,
    compute_golden_number,
)


class TestGoldenNumber(unittest.TestCase):
    def test_one_based(self):
        # Year 1 in the proleptic scheme gives golden number 2,
        # because year 0 gives golden number 1.
        self.assertEqual(int(GoldenNumber(1)), 1)
        self.assertEqual(int(GoldenNumber(19)), 19)

    def test_out_of_range_raises(self):
        with self.assertRaises(ValueError):
            GoldenNumber(0)
        with self.assertRaises(ValueError):
            GoldenNumber(20)
        with self.assertRaises(ValueError):
            GoldenNumber(-1)

    def test_non_int_raises(self):
        with self.assertRaises(TypeError):
            GoldenNumber(1.5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            GoldenNumber("1")  # type: ignore[arg-type]

    def test_is_int_subclass(self):
        gn = GoldenNumber(7)
        self.assertIsInstance(gn, int)
        self.assertEqual(gn + 1, 8)
        self.assertEqual(gn, 7)

    def test_repr(self):
        self.assertEqual(repr(GoldenNumber(3)), "GoldenNumber(3)")


class TestMetonicCycleGoldenNumber(unittest.TestCase):
    def setUp(self):
        self.cycle = MetonicCycle()

    def test_year_zero_is_golden_one(self):
        # The cycle is anchored so year 0 -> golden number 1.
        self.assertEqual(int(self.cycle.golden_number(0)), 1)

    def test_cycle_repeats_every_19_years(self):
        for y in (1, 100, 2024, -500):
            self.assertEqual(
                int(self.cycle.golden_number(y)),
                int(self.cycle.golden_number(y + 19)),
            )

    def test_known_values(self):
        # Hand-checked: 2024 % 19 = 10, so golden number = 11.
        self.assertEqual(int(self.cycle.golden_number(2024)), 11)
        # 2000 % 19 = 5, golden number = 6.
        self.assertEqual(int(self.cycle.golden_number(2000)), 6)

    def test_negative_year(self):
        # Python's % keeps the result non-negative, so the cycle is
        # continuous across the BC/AD boundary.
        self.assertEqual(int(self.cycle.golden_number(-1)), 19)
        self.assertEqual(int(self.cycle.golden_number(-19)), 1)

    def test_non_int_year_raises(self):
        with self.assertRaises(TypeError):
            self.cycle.golden_number(2024.5)  # type: ignore[arg-type]


class TestCyclePosition(unittest.TestCase):
    def setUp(self):
        self.cycle = MetonicCycle()

    def test_zero_based(self):
        self.assertEqual(self.cycle.cycle_position(0), 0)
        self.assertEqual(self.cycle.cycle_position(18), 18)
        self.assertEqual(self.cycle.cycle_position(19), 0)

    def test_matches_golden_number(self):
        for y in range(-50, 50):
            pos = self.cycle.cycle_position(y)
            gn = int(self.cycle.golden_number(y))
            self.assertEqual(pos + 1, gn)


class TestPaschalFullMoon(unittest.TestCase):
    def setUp(self):
        self.cycle = MetonicCycle()

    def test_returns_month_day_tuple(self):
        result = self.cycle.paschal_full_moon(2024)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        month, day = result
        self.assertIn(month, (3, 4))
        self.assertIsInstance(month, int)
        self.assertIsInstance(day, int)

    def test_all_golden_numbers_have_valid_dates(self):
        # Every position in the cycle must produce a sensible March/April date.
        for offset in range(19):
            month, day = self.cycle.paschal_full_moon(offset)
            self.assertIn(month, (3, 4))
            if month == 3:
                self.assertGreaterEqual(day, 21)
                self.assertLessEqual(day, 31)
            else:
                self.assertGreaterEqual(day, 1)
                self.assertLessEqual(day, 18)

    def test_known_value(self):
        # Year 2024: golden number 11 -> March 25.
        self.assertEqual(self.cycle.paschal_full_moon(2024), (3, 25))

    def test_cycle_repeats(self):
        self.assertEqual(
            self.cycle.paschal_full_moon(2024),
            self.cycle.paschal_full_moon(2024 + 19),
        )

    def test_table_completeness(self):
        # The internal table has exactly 19 entries, one per golden number.
        dates = set()
        for offset in range(19):
            dates.add(self.cycle.paschal_full_moon(offset))
        # Not all dates are unique (some share values in some tables),
        # but we must have 19 lookups succeed without error.
        self.assertEqual(len([self.cycle.paschal_full_moon(i) for i in range(19)]), 19)


class TestIsCycleStart(unittest.TestCase):
    def setUp(self):
        self.cycle = MetonicCycle()

    def test_multiples_of_19(self):
        self.assertTrue(self.cycle.is_cycle_start(0))
        self.assertTrue(self.cycle.is_cycle_start(19))
        self.assertTrue(self.cycle.is_cycle_start(-19))
        self.assertTrue(self.cycle.is_cycle_start(2025 - (2025 % 19)))

    def test_non_multiples(self):
        self.assertFalse(self.cycle.is_cycle_start(1))
        self.assertFalse(self.cycle.is_cycle_start(18))
        self.assertFalse(self.cycle.is_cycle_start(2024))


class TestModuleLevelFunctions(unittest.TestCase):
    def test_compute_golden_number(self):
        self.assertEqual(int(compute_golden_number(2024)), 11)
        self.assertIsInstance(compute_golden_number(2024), GoldenNumber)

    def test_compute_paschal_full_moon(self):
        self.assertEqual(compute_paschal_full_moon(2024), (3, 25))
        self.assertEqual(compute_paschal_full_moon(0), _gn1_pfm())


def _gn1_pfm():
    """Helper: the paschal full moon for golden number 1."""
    return (4, 14)


if __name__ == "__main__":
    unittest.main()
