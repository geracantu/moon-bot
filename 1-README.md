# moon-bot 🌙

A little daily moon report for Monterrey, Mexico. It shows the moon's phase and illumination, today's local moonrise, and the next full moon. It gives a heads-up one or two days before a full moon.

## Run it on your computer

Install [Python 3.10+](https://www.python.org/downloads/), then run from this folder:

```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python moon_bot.py
```

The output is a short Markdown report. You can run it whenever you like. The calculations use [PyEphem](https://rhodesmill.org/pyephem/) and the Monterrey coordinates 25.6866° N, 100.3161° W. Times are shown in `America/Monterrey`.

## Run it on GitHub

After this pull request is merged, open the **Actions** tab, select **Moon over Monterrey**, then click **Run workflow** to try it. Open that run to see the report under **Summary**, or expand the "Write today's moon report" step for the plain output. GitHub will also schedule it every day at 19:17 UTC (1:17 PM Monterrey time). GitHub schedules can be late or occasionally skipped, and inactivity can disable schedules in public repos after 60 days.

This first version **does not send a text, email, or notification**. The daily report stays in GitHub Actions. No account secrets or API keys are needed. If you want it sent to you later, we can add a delivery method after you choose where it should go.

A day without a moonrise is possible, so the report will say "No moonrise today" rather than showing tomorrow's time. The phase name is an eight-part approximation; moonrise and full-moon times are astronomical estimates and can differ from what you see on the horizon.
