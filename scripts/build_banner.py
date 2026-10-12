"""Render scripts/banner.html to assets/banner.jpg with headless Chrome.

Run `python3 scripts/build_banner.py` after editing the banner. Needs Google
Chrome, and macOS's `sips` for the JPEG.
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
png = ROOT / "banner.png"

subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                "--force-device-scale-factor=2", "--window-size=1200,400",
                # Gives the Google Fonts time to load before the shot.
                "--virtual-time-budget=6000", f"--screenshot={png}",
                (ROOT / "scripts" / "banner.html").as_uri()], check=True, stderr=subprocess.DEVNULL)
subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "82", str(png),
                "--out", str(ROOT / "assets" / "banner.jpg")], check=True, capture_output=True)
png.unlink()
print("built assets/banner.jpg")
