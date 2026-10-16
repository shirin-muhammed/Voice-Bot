"""Teach a correction: python teach.py "what was heard" "what it should be"."""
import sys

import corrections

if __name__ == "__main__":
    heard, fixed = sys.argv[1], sys.argv[2]
    corrections.save(corrections.learn(heard, fixed, corrections.load()))
    print("Learned.")
