import sys
from itertools import combinations


def load_transactions(input_file):
    transactions = []
    with open(input_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            items = set(map(int, line.split()))
            transactions.append(items)
    return transactions


def format_itemset(itemset):
    sorted_items = sorted(itemset)
    return "{" + ",".join(map(str, sorted_items)) + "}"


def get_support_count(itemset, transactions):
    count = 0
    for transaction in transactions:
        if itemset.issubset(transaction):
            count += 1
    return count


def generate_candidates(prev_frequents, k):
    candidates = set()
    prev_list = list(prev_frequents)

    for i in range(len(prev_list)):
        for j in range(i + 1, len(prev_list)):
            a = sorted(prev_list[i])
            b = sorted(prev_list[j])

            if a[:k - 2] == b[:k - 2]:
                candidate = frozenset(prev_list[i] | prev_list[j])
                if len(candidate) == k:
                    candidates.add(candidate)

    return candidates


def prune_candidates(candidates, prev_frequents):
    pruned = set()

    for candidate in candidates:
        all_subsets_frequent = True
        for subset in combinations(candidate, len(candidate) - 1):
            if frozenset(subset) not in prev_frequents:
                all_subsets_frequent = False
                break
        if all_subsets_frequent:
            pruned.add(candidate)

    return pruned


def apriori(transactions, min_support_percent):
    total_transactions = len(transactions)
    min_support_count = total_transactions * (min_support_percent / 100.0)

    all_frequents = dict()
    support_counts = dict()

    # L1 생성
    item_count = dict()
    for transaction in transactions:
        for item in transaction:
            itemset = frozenset([item])
            item_count[itemset] = item_count.get(itemset, 0) + 1

    current_frequents = set()
    for itemset, count in item_count.items():
        if count >= min_support_count:
            current_frequents.add(itemset)
            support_counts[itemset] = count

    k = 1
    if current_frequents:
        all_frequents[k] = current_frequents

    # L2 이상 생성
    while current_frequents:
        k += 1

        candidates = generate_candidates(current_frequents, k)
        candidates = prune_candidates(candidates, current_frequents)

        candidate_count = dict()
        for candidate in candidates:
            count = get_support_count(candidate, transactions)
            if count >= min_support_count:
                candidate_count[candidate] = count

        current_frequents = set(candidate_count.keys())

        if current_frequents:
            all_frequents[k] = current_frequents
            support_counts.update(candidate_count)

    return all_frequents, support_counts, total_transactions


def generate_association_rules(all_frequents, support_counts, total_transactions):
    rules = []

    for k in all_frequents:
        if k < 2:
            continue

        for frequent_itemset in all_frequents[k]:
            itemset_support_count = support_counts[frequent_itemset]
            itemset_support_percent = (itemset_support_count / total_transactions) * 100

            items = list(frequent_itemset)

            for r in range(1, len(items)):
                for left_tuple in combinations(items, r):
                    left = frozenset(left_tuple)
                    right = frequent_itemset - left

                    left_support_count = support_counts[left]
                    confidence = (itemset_support_count / left_support_count) * 100

                    rules.append((
                        left,
                        right,
                        round(itemset_support_percent, 2),
                        round(confidence, 2)
                    ))

    return rules


def write_output(rules, output_file):
    with open(output_file, "w") as f:
        for left, right, support, confidence in rules:
            line = (
                f"{format_itemset(left)}\t"
                f"{format_itemset(right)}\t"
                f"{support:.2f}\t"
                f"{confidence:.2f}\n"
            )
            f.write(line)


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 apriori.py <min_support_percent> <input_file> <output_file>")
        sys.exit(1)

    min_support_percent = float(sys.argv[1])
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    transactions = load_transactions(input_file)
    all_frequents, support_counts, total_transactions = apriori(transactions, min_support_percent)
    rules = generate_association_rules(all_frequents, support_counts, total_transactions)
    write_output(rules, output_file)


if __name__ == "__main__":
    main()