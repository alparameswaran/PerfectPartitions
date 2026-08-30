#!/usr/bin/env python3
"""Validate perfect-partition .txt files

Usage: python check_partitions_lean.py <file.txt> <n> <D_n>

Example:
n=6: python check_partitions_lean.py 82_partitions_6_RLS.txt 6 265
"""

import sys

def is_derangement(perm):
    return all(i != v for i, v in enumerate(perm))

def parse_perm(s):
    return tuple(int(c) for c in s)

def load_blocks(path):
    text = open(path).read().strip("\n")
    raw_blocks = [b for b in text.split("\n\n") if b.strip()]
    blocks = []
    for rb in raw_blocks:
        lines = [ln.split() for ln in rb.splitlines() if ln.strip()]
        blocks.append([[parse_perm(p) for p in line] for line in lines])
    return blocks

def validate_block(block, n, d_n):
    errors = []
    seen = set()

    for li, line in enumerate(block):
        for p in line[1:]:
            if p in seen:
                errors.append(f"line {li}: derangement {p} duplicated in this partition")
            seen.add(p)
        for j in range(n):  #Latin-square/column-disjointness check
            if len({p[j] for p in line}) != n:
                errors.append(f"line {li}: column {j} repeats a value")

    expected_lines = d_n//(n - 1)
    if len(block) != expected_lines:
        errors.append(f"expected {expected_lines} lines, got {len(block)}")
    if len(seen) != d_n:
        errors.append(f"covers {len(seen)} derangements, expected D_n = {d_n}")

    return errors

def main(path, n, d_n):
    blocks = load_blocks(path)
    if not blocks:
        print("No partitions found in file.")
        return

    print(f"n = {n}, D_n = {d_n}, {len(blocks)} partition(s) in file.\n")

    all_valid = True
    for bi, block in enumerate(blocks):
        errors = validate_block(block, n, d_n)
        if errors:
            all_valid = False
            print(f"Partition {bi + 1}: INVALID")
            for e in errors:
                print(f"  - {e}")
        else:
            print(f"Partition {bi + 1}: valid")

    # Distinctness:represent each partition as a set of its lines (order-independent)
    reprs = [frozenset(tuple(line) for line in block) for block in blocks]
    dup_pairs = [
        (i + 1, j + 1)
        for i in range(len(reprs))
        for j in range(i + 1, len(reprs))
        if reprs[i] == reprs[j]
    ]

    print()
    if dup_pairs:
        all_valid = False
        print(f"Duplicate partitions found: {dup_pairs}")
    else:
        print(f"All {len(blocks)} partitions are distinct.")

    print("\nRESULT:", "ALL VALID AND DISTINCT" if all_valid else "FAILED - see errors above")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
