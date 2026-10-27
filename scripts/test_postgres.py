"""Run tests against temporary local PostgreSQL binaries; no cloud credentials used."""

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlencode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bin-dir", required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    (root / "work").mkdir(exist_ok=True)
    binaries = args.bin_dir.resolve()
    # Short UNIX socket path; no TCP listener and no persistent service installation.
    with tempfile.TemporaryDirectory(prefix="bobalab-pg-") as folder:
        runtime = Path(folder)
        data = runtime / "data"
        log = runtime / "postgres.log"
        subprocess.run(
            [
                str(binaries / "initdb"),
                "-D",
                str(data),
                "-U",
                "postgres",
                "--auth=trust",
                "--no-locale",
                "-E",
                "UTF8",
            ],
            check=True,
            stdout=subprocess.DEVNULL,
        )
        started = False
        try:
            subprocess.run(
                [
                    str(binaries / "pg_ctl"),
                    "-D",
                    str(data),
                    "-l",
                    str(log),
                    "-o",
                    f"-F -k {runtime} -h ''",
                    "-w",
                    "start",
                ],
                check=True,
                stdout=subprocess.DEVNULL,
            )
            started = True
            env = dict(os.environ)
            env["TEST_DATABASE_URL"] = "postgresql://postgres@/postgres?" + urlencode(
                {"host": str(runtime), "sslmode": "disable"}
            )
            return subprocess.run(
                [sys.executable, "-m", "pytest", "-q"], cwd=root, env=env
            ).returncode
        finally:
            if started:
                subprocess.run(
                    [str(binaries / "pg_ctl"), "-D", str(data), "-m", "fast", "-w", "stop"],
                    check=True,
                    stdout=subprocess.DEVNULL,
                )


if __name__ == "__main__":
    raise SystemExit(main())
