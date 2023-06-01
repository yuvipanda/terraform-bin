import os
import subprocess
import sys

def main():
    returncode = 0

    for filepath in sys.argv[1:]:
        proc = subprocess.run([
            'terraform',
            'fmt',
            '-diff',
            '-check',
            filepath
        ])

        if proc.returncode != 0:
            returncode = proc.returncode

    sys.exit(returncode)
