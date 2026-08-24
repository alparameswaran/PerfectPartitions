FILENAME = "reduced5.txt"
TARGET_CLIQUE_SIZE = 11
OUTPUT_FILENAME = "5_RLS_Perfect_Partitions.txt"



# Load reduced Latin squares
def load_squares(filename):
    squares = []
    full_lines = []
    with open(filename) as f:
        for line in f:
            rows = line.strip().split()
            if not rows:
                continue
            derangements = frozenset(rows[1:])
            squares.append(derangements)
            full_lines.append(rows)
    return squares, full_lines



# Build R_5 graph
def build_graph(der_sets):
    n = len(der_sets)
    adjacency = [set() for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            if der_sets[i].isdisjoint(der_sets[j]):
                adjacency[i].add(j)
                adjacency[j].add(i)

    return adjacency



#Clique search
def find_cliques(adjacency, k):
    n = len(adjacency)
    cliques = []

    def backtrack(current_clique, candidates):
        # Found clique
        if len(current_clique) == k:
            cliques.append(current_clique[:])
            return

        # Not enough candidates left
        if len(current_clique) + len(candidates) < k:
            return

        for i, v in enumerate(candidates):
            # Only keep neighbors of v
            new_candidates = [
                u for u in candidates[i+1:]
                if u in adjacency[v]
            ]

            backtrack(current_clique + [v], new_candidates)

    backtrack([], list(range(n)))
    return cliques





#Write cliques (partitions) as RLS lines
def write_cliques(cliques, full_lines, filename):
    with open(filename, "w") as f:
        for clique in cliques:
            for v in clique:
                f.write(" ".join(full_lines[v]) + "\n")
            f.write("\n")  # blank line between partitions



def main():
    der_sets, full_lines = load_squares(FILENAME)
    adjacency = build_graph(der_sets)
    n = len(adjacency)

    cliques = find_cliques(adjacency, TARGET_CLIQUE_SIZE)

    print(f"Total cliques found: {len(cliques)}\n")

    write_cliques(cliques, full_lines, OUTPUT_FILENAME)



if __name__ == "__main__":
    main()