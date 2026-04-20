# Frequent Pattern Mining (Apriori Algorithm)

데이터 사이언스 과제 #1로 수행한 **Frequent Pattern Mining 프로젝트**입니다.  
본 프로젝트에서는 Apriori 알고리즘을 직접 구현하여 **frequent itemset 탐색 및 association rule 생성**을 수행하였습니다.

---

## 프로젝트 개요

- **목표**: 거래 데이터로부터 빈번한 패턴(Frequent Itemset)을 찾고, 연관 규칙(Association Rule)을 생성
- **알고리즘**: Apriori Algorithm
- **언어**: Python
- **입력**: Transaction 데이터 (각 줄 = 하나의 거래)
- **출력**: Association Rule (support, confidence 포함)

---

## 주요 기능

### 1️⃣ Transaction 데이터 로드
- 입력 파일을 읽어 각 거래를 `set` 형태로 변환
- 공백/탭 기반 parsing 처리

---

### 2️⃣ Apriori 알고리즘 구현

#### ✔ L1 생성
- 1-itemset의 support count 계산
- minimum support 이상만 유지

#### ✔ JOIN 단계
- 이전 frequent (k-1)-itemset을 기반으로 k-itemset 후보 생성

#### ✔ PRUNE 단계
- Apriori Property 적용  
  → 모든 부분집합이 frequent한 경우만 유지

#### ✔ Support Count 계산
- 후보 itemset이 transaction에 포함되는 횟수 계산

---

### 3️⃣ Association Rule 생성

- frequent itemset으로부터 가능한 모든 rule 생성
- 계산 지표:
  - **Support (%)**
  - **Confidence (%)**

```text
Support = (itemset 등장 횟수 / 전체 transaction 수) × 100
Confidence = (itemset 등장 횟수 / left subset 등장 횟수) × 100
```

### 4️⃣ 결과 출력

	•	출력 형식:
~~~python
{A} {B} support confidence
~~~
- 소수점 둘째 자리까지 formatting

---
## 실행 방법
~~~bash
python3 apriori.py <min_support_percent> <input_file> <output_file>
~~~



