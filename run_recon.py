import argparse
import json

from recon import recon
from recon.config import DEFAULT_TARGET_URL


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the RECON agent against a target.")
    parser.add_argument("--target", default=DEFAULT_TARGET_URL, help="Target /chat URL")
    args = parser.parse_args()

    profile = recon(args.target)
    print(json.dumps(profile, indent=2))


if __name__ == "__main__":
    main()
