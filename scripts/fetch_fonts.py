"""Fetch the paper's typefaces (SIL Open Font License) into fonts/.

Source Serif 4 and Source Sans 3 are not in every TeX Live distribution, so
the build pins exact upstream releases, checks their SHA-256 and extracts
only the faces the paper uses. Idempotent: does nothing if fonts/ is complete.
"""

from __future__ import annotations

import hashlib
import io
import sys
import zipfile
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / "fonts"
CACHE_DIR = ROOT / "data" / "raw" / "fonts"

RELEASES = [
    {
        "name": "Source Serif 4.005",
        "url": "https://github.com/adobe-fonts/source-serif/releases/download/4.005R/source-serif-4.005_Desktop.zip",
        "sha256": "549fdb8f9a682bd06944298621404969f6de77c2e422ff3b8244a1dcd6a0c425",
        "prefix": "source-serif-4.005_Desktop/OTF/",
        "faces": [
            f"SourceSerif4{opsz}-{w}.otf"
            for opsz in ("", "Caption", "Subhead", "Display")
            for w in ("Regular", "It", "Semibold", "SemiboldIt")
        ],
    },
    {
        "name": "Source Sans 3.052",
        "url": "https://github.com/adobe-fonts/source-sans/releases/download/3.052R/OTF-source-sans-3.052R.zip",
        "sha256": "a4ebbdea20b08ccbd7bf3665a9462454eefdd01d9a6307129d3b3d4672981074",
        "prefix": "OTF/",
        "faces": [f"SourceSans3-{w}.otf" for w in ("Regular", "It", "Semibold", "SemiboldIt")],
    },
]


def fetch(release: dict) -> bytes:
    cached = CACHE_DIR / Path(release["url"]).name
    if cached.exists():
        data = cached.read_bytes()
    else:
        print(f"  downloading {release['name']}")
        resp = requests.get(release["url"], timeout=120)
        resp.raise_for_status()
        data = resp.content
    digest = hashlib.sha256(data).hexdigest()
    if digest != release["sha256"]:
        sys.exit(f"checksum mismatch for {release['name']}: {digest}")
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cached.write_bytes(data)
    return data


def main() -> None:
    FONT_DIR.mkdir(exist_ok=True)
    for release in RELEASES:
        missing = [f for f in release["faces"] if not (FONT_DIR / f).exists()]
        if not missing:
            continue
        with zipfile.ZipFile(io.BytesIO(fetch(release))) as zf:
            for face in missing:
                (FONT_DIR / face).write_bytes(zf.read(release["prefix"] + face))
    print(f"fonts: {len(list(FONT_DIR.glob('*.otf')))} faces in {FONT_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
