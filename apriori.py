import sys
from itertools import combinations


# load_transaction 함수 
## 입력 파일을 읽어서 transaction list로 변환
## 각 줄은 하나의 transaction을 의미하고, 공백과 탭으로 구분된 정수 item들을 set 형태로 저장
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


# format_itetmset 함수
## itemset을 과제 출력 형식에 맞게 문자열로 변환
## 오름차순으로 정렬하고, 중괄호 (brace)를 넣어서 감싸 반환
def format_itemset(itemset):
    sorted_items = sorted(itemset)
    return "{" + ",".join(map(str, sorted_items)) + "}"


# get_support_count 함수
## 특정 itemtset이 전체 transaction에서 몇번 등장했는지 계산하는 함수
## itemset이 transaction의 부분집합이면 해당 transaction에 등장한 것으로 계산
def get_support_count(itemset, transactions):
    count = 0
    for transaction in transactions:
        if itemset.issubset(transaction):
            count += 1
    return count


# generate_candidate 함수 -> JOIN 단계
## 이전 단계의 frequent(k-1)-itemset으로부터 k-itemset candidate 생성 
## 두 itemset의 앞부분 k-2개가 같으면 합쳐서 새로운 k-itemset 후보를 만든다.
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

# prune_candidates 함수 - PRUNE 단계
## Apriori Property 사용해서 후보들 제거한다
## candidate의 모든 (k-1)-subset이 이전단계 frequent itemset에 포함되어 있어야 유지
## 하나라도 있으면 제거
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

# apriori 함수 -> 모든 frequent itemset을 찾는 것이 목표!
## 1. frequent 1-itemset 생성
## 2. join step으로 후보 생성
## 3. prune step 적용하여 필요없는 후보들 제거
## 4. support count 계산을 하고 min_sup 이상인 값만 유지, 그 외는 제거
## 5. 더 이상 frequent itemset
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


# generate_association_rules 함수
## frequent itemset들로부터 모든 association rules을 생성하는 함수
## 크기가 2인 이상인 frequent itemset들에 대해 가능한 모든 non-empty proper subset을 ㅣeft로 잡은 이후에 나머지를 right으로 두어 rule을 만든다.
### support = support_count(itemset) / total_transactions * 100
### confidence = support_count(itemset) / support_count(left) * 100
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


# write_output 함수
## 생성된 association rules들을 출력 파일에 저장
## 출력 형식 : itemset (tab) associative_itemset (tab) support (tab) confidence
## 과제 형식 : itemset은 중괄호 형식으로 출력하고, support와 confidence 값은 소수점 둘째 자리까지 출력한다.
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

# main 함수
## 명령 인자 오류를 따로 설정
## 명령행 인자로 minimum support, 입력 파일명, 출력 파일명을 함께 입력하면
## Apriori 알고리즘을 수행한 이후 association rule을 생성하고 결과를 저장
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