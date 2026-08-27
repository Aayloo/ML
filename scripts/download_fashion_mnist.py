"""Download the public Fashion-MNIST dataset for chapter 15.

The raw .gz files (~29 MB total) are intentionally excluded from the git repo
to keep it lightweight. Run from the repository root:

    python scripts/download_fashion_mnist.py
"""

import urllib.request
from pathlib import Path

BASE_URL = (
    "https://github.com/zalandoresearch/fashion-mnist/raw/master/data/fashion"
)
FILES = [
    "train-images-idx3-ubyte.gz",
    "train-labels-idx1-ubyte.gz",
    "t10k-images-idx3-ubyte.gz",
    "t10k-labels-idx1-ubyte.gz",
]
OUT_DIR = (
    Path(__file__).resolve().parents[1]
    / "archive"
    / "15_图像分类"
    / "data"
    / "fashion"
)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        dest = OUT_DIR / name
        if dest.exists() and dest.stat().st_size > 0:
            print(f"skip  {name} (already exists)")
            continue
        url = f"{BASE_URL}/{name}"
        print(f"fetch {name} ...")
        urllib.request.urlretrieve(url, dest)
        print(f"  -> {dest} ({dest.stat().st_size / 1e6:.1f} MB)")
    print("done")


if __name__ == "__main__":
    main()
