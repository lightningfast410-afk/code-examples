"""32_cli_tool.py — A command-line tool with argparse, tested in-process.

Demonstrates: a real CLI shape — subcommands, required
arguments, and friendly errors — with the logic separated from
argument parsing so it can be tested without spawning a
process. Run it for real with: python3 32_cli_tool.py count <file>
Run: python3 32_cli_tool.py
"""

import argparse
import sys


def count_words(text):
    return len(text.split())


def build_parser():
    parser = argparse.ArgumentParser(description="Tiny text tool.")
    sub = parser.add_subparsers(dest="command", required=True)
    count = sub.add_parser("count", help="count words in a file")
    count.add_argument("path", help="path to a text file")
    greet = sub.add_parser("greet", help="print a greeting")
    greet.add_argument("--name", default="world")
    return parser


def run(argv):
    args = build_parser().parse_args(argv)
    if args.command == "count":
        try:
            text = open(args.path, encoding="utf-8").read()
        except OSError as exc:
            return f"error: cannot read {args.path}: {exc}"
        return f"{args.path}: {count_words(text)} words"
    return f"hello, {args.name}!"


def main():
    # Self-test: parse and run without leaving this process.
    assert run(["greet", "--name", "coder"]) == "hello, coder!"
    assert run(["greet"]) == "hello, world!"
    assert count_words("one two  three") == 3
    missing = run(["count", "/definitely/not/a/real/file.txt"])
    assert missing.startswith("error: cannot read")
    print("PROOF: greet works with and without --name")
    print(f"PROOF: missing file handled: {missing[:60]}...")
    print("TIP: try: python3 32_cli_tool.py greet --name Ada")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(run(sys.argv[1:]))
    else:
        main()
