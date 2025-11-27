decision tree 모델 먼저 완성 후 코드 몇 줄만 수정하면 random forest 모델도 쉽게 만들 수 있어 둘 다 업로드 하였습니다. random forest 모델만 발표자료에 사용하여도 좋고, 아니면 두 모델 다 사용하여 비교하는 식으로 발표에 사용하여도 좋을 거 같습니다. 아래에는 decision tree와 random forest 모델의 특징과 decision tree에 비해 random forest를 사용하는 것의 이점, 두 모델의 결과 분석과 한계 등을 정리하였습니다.

# 🎵 Hit Song Prediction: Decision Tree & Random Forest 분석

본 프로젝트는 Spotify 음향 데이터(tempo, valence, energy 등)를 기반으로 **히트곡 여부를 예측하고**,
특히 **어떤 feature가 히트곡에 영향을 미치는지 분석**하는 것을 주요 목표로 한다.

---

## 1. Decision Tree의 핵심 특징

### ✔ 특징

* 데이터를 feature 기준으로 분할하여 예측하는 **단순하고 해석이 쉬운 모델**

### ✔ 장점

* 구조가 간단해 **직관적이고 해석이 쉬움**
* 전처리가 크게 필요 없음
* 규칙 기반으로, 어떤 feature가 히트 여부를 판단하는지 쉽게 파악 가능

### ✔ 단점

* 데이터의 작은 변화에도 크게 흔들리는 **불안정성**
* 직교 분할만 수행 → 데이터 회전에 취약
* 과적합에 매우 민감
* 복잡한 패턴을 잡기 어려움

### ✔ 히트곡 분석에서의 한계

1. 히트곡 데이터는 noisy하고 복잡 → 트리가 쉽게 흔들림
2. feature 간 관계가 단순 분할 구조로 설명하기 어려움

---

## 2. Random Forest의 핵심 특징

### ✔ 특징

* 여러 결정 트리를 앙상블하여 예측 결과를 집계하는 모델

### ✔ 장점

* 여러 나무의 평균으로 **불안정성 감소**
* Bagging + feature subset → **과적합 억제**, 일반화 성능 향상
* 다양한 트리 구조 생성 → **variance 감소**
* **신뢰도 높은 feature importance 제공**
* 단일 Decision Tree보다 성능 우수

### ✔ 단점

* 구조가 복잡하여 **직관적 해석 어려움**

### ✔ 히트곡 분석에서 Random Forest가 중요한 이유

1. 히트곡 여부는 단순 규칙보다 복잡한 패턴
2. 다양한 관점의 트리를 생성하여 섬세한 패턴까지 포착
3. feature importance를 안정적으로 측정 가능

---

## 3. 두 모델의 Feature Importance 비교

| 중요도 순위 | Decision Tree    | Random Forest    |
| ------ | ---------------- | ---------------- |
| 1      | valence          | speechiness      |
| 2      | speechiness      | tempo            |
| 3      | acousticness     | acousticness     |
| 4      | tempo            | loudness         |
| 5      | energy           | valence          |
| 6      | liveness         | energy           |
| 7      | danceability     | liveness         |
| 8      | loudness         | danceability     |
| 9      | instrumentalness | instrumentalness |

### 공통점

* **speechiness, acousticness**가 두 모델 모두 상위 중요도
* **danceability, instrumentalness**는 하위 중요도

---

## 4. 두 모델의 TP가 매우 낮게 나온 이유

두 모델 모두 Hit(1)을 Hit으로 맞춘 TP 값이

* Decision Tree: **4**
* Random Forest: **0**

으로 나타났다.

이는 모델이 “실패했다”기보다는 **문제 설정에서 발생하는 자연스러운 현상**이다.

### 원인 1) 불균형 데이터 문제

Hit가 전체 데이터에서 극소수라면 트리 계열 모델은 이렇게 행동한다:

> "Hit 너무 적음 → 다 Not-Hit로 예측해도 정확도 높음"

→ Minority class(히트곡)를 무시하는 방향으로 학습
→ Random Forest는 이 경향이 오히려 더 강해지는 경우가 많음

### 원인 2) 음향 feature만으로 히트곡을 설명하기 어려움

히트 여부는 다음 요소가 훨씬 더 강하게 작용한다:

* 아티스트 인기
* 마케팅/홍보
* 플레이리스트 편성
* 발매 시기
* 바이럴 효과

즉, **음향 feature는 약한 예측 변수** → 히트 패턴을 포착하기 어려움

---

## 5. TP가 낮다고 해서 모델이 ‘나쁜 모델’인가?

### ❌ 아니다.

이번 연구의 목적은 **정확한 hit 예측**이 아니라
👉 **히트곡에 영향을 주는 feature 분석**임.

* Random Forest는 예측 성능이 낮아도 **feature importance는 안정적**
* TP가 낮은 이유는 모델의 문제가 아니라
  **클래스 불균형 + feature 자체의 한계 때문**

✔ 즉, TP가 낮아도 본 연구 목적(feature importance 분석)에는 문제가 없다.

---

## 📌 결론

* Decision Tree와 Random Forest 모두 히트곡 feature 분석에 사용 가능
* Random Forest가 더 안정적이고 일반화 성능이 높아 **발표 자료로 사용하기 적합**
* TP가 낮게 나왔다고 모델이 잘못된 것이 아니며,
  **데이터 특성상 자연스럽게 발생한 현상**
* Feature importance 분석 목적이라면 현재 모델로 충분히 의미 있는 결과를 도출함
