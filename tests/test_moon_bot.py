import unittest
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from moon_bot import moonrise_today, phase, report


class MoonBotTests(unittest.TestCase):
    def test_report_uses_local_day(self):
        # 02:00 UTC is still the previous evening in Monterrey.
        text = report(datetime(2026, 9, 26, 2, tzinfo=timezone.utc))
        self.assertIn("September 25, 2026", text)
        self.assertIn("Monterrey time", text)

    def test_phase_is_valid(self):
        name, emoji, illumination = phase(datetime(2026, 9, 25, tzinfo=timezone.utc))
        self.assertTrue(name)
        self.assertTrue(emoji)
        self.assertGreaterEqual(illumination, 0)
        self.assertLessEqual(illumination, 100)

    def test_moonrise_matches_local_day_when_present(self):
        now = datetime(2026, 9, 25, 12, tzinfo=ZoneInfo("America/Monterrey"))
        rising = moonrise_today(now)
        if rising is not None:
            self.assertEqual(rising.date(), now.date())

    def test_full_moon_alert(self):
        # The phase function determines the future full moon, so inspect a
        # known date near full moon rather than relying on a hard-coded phase.
        import ephem
        from moon_bot import utc_datetime
        upcoming = utc_datetime(ephem.next_full_moon("2026/09/01"))
        two_days_before = upcoming.astimezone(ZoneInfo("America/Monterrey")).date()
        from datetime import timedelta
        day = two_days_before - timedelta(days=2)
        noon = datetime(day.year, day.month, day.day, 12, tzinfo=ZoneInfo("America/Monterrey"))
        self.assertIn("Heads-up: full moon in 2 days", report(noon))


if __name__ == "__main__":
    unittest.main()
