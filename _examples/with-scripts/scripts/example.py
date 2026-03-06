#!/usr/bin/env python3
"""
Example helper script for the with-scripts skill.

Demonstrates how to create a simple, parameterized script
that an AI agent can invoke deterministically.
"""

import argparse


def main():
    parser = argparse.ArgumentParser(description="Example skill script")
    parser.add_argument("--name", default="World", help="Name to greet")
    args = parser.parse_args()

    print(f"Hello, {args.name}! This is an example skill script.")


if __name__ == "__main__":
    main()
