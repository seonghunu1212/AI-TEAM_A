decision tree 모델 먼저 완성 후 코드 몇 줄만 수정하면 random forest 모델도 쉽게 만들 수 있어 둘 다 업로드 하였습니다. random forest 모델만 발표자료에 사용하여도 좋고, 아니면 두 모델 다 사용하여 비교하는 식으로
발표에 사용하여도 좋을 거 같습니다. 아래에는 decision tree와 random forest 모델의 특징과 decision tree에 비해 random forest를 사용하는 것의 이점, 두 모델의 결과 분석과 한계 등을 정리하였습니다.

1. Decision tree의 핵심 특징
   - 데이터를 특징값(feature) 기준으로 분할하여 예측하는 단순하고 해석이 쉬운 모델
   
장점
   - 이해하기 쉽고 해석이 뛰어남
   - 규칙 기반이라 "어떤 feature가 히트곡을 판별하는지" 직관적
   - 전처리가 크게 필요 없음
단점
   - 데이터의 작은 변화에도 매우 민감함 (불안정성)
   - 직교 분할만 함 -> 데이터 회전에 취약
   - 과적합에 매우 취약
   - 예측 성능이 최고급 모델에 비해 떨어짐
     
   -> 히트곡 분석에서의 문제점
     1. 히트곡 데이터는 본질적으로 noisy하고 복잡하여 트리가 너무 쉽게 흔들림
     2. feature 간 관계가 단순 직교 분할로 설명되기 어려움

2. Random forest의 핵심 특징
   - 여러 결정 트리를 앙상블하여 예측 결과를 집계하는 모델
   
장점
   - 여러 나무를 평균내어 불안정성이 크게 감소
   - bagging + feature subset 사용하여 과적합이 줄고 일반화 성능 증가
   - 다양한 트리를 생성 -> varience 감소
   - feature importance를 매우 신뢰성 있게 계산 가능
   - 단일 decision tree보다 성능이 훨씬 좋음
단점
   - 직관적 해석은 약해짐
   - 모델 구조가 복잡
     
   -> 히트곡 분석에서 중요한 이유
     1. 히트곡 여부는 단순 규칙보다 복합적 패턴임
     2. random forest는 다양한 관점의 트리를 만들기 때문에 히트 여부를 설명하는 복잡하고 미세한 패턴까지 포착 가능
     3. feature importance를 통해 어떤 feature가 히트곡에 상대적으로 더 기여하는지 안정적으로 측정 가능

3. 두 모델의 결과 분석
   - 두 모델의 feature importance를 살펴보면 decision tree 모델은 valence, speechiness, acousticness, tempo, energy, liveness, danceability, loudness, instrumentalness 순서,
   random forest 모델은 speechiness, tempo, acousticness, loudness, valence, energy, liveness, danceability, instrumentalness 순서를 보였다.
   두 모델 모두 speechiness와 acousticness가 상위 중요도를 보였고, danceability와 instrumentalness가 하위 중요도를 보였다.
   
   하지만 두 모델 모두 TP(실제 Hit를 Hit로 맞춘 수)가 decision tree의 경우엔 4, random forest의 경우엔 0으로 확인되었다. 이 문제에 대해 더 자세히 살펴보도록 하겠다.

5. TP가 0에 가깝게 나온 2가지 이유. 둘 중 어느 것이 더 영향을 미쳤을 지는 다른 모델들과 비교 해봐야함.
   1. 불균형 데이터에서 트리 계열 모델은 소수 클래스를 무시하는 경향이 있음.
      Hit가 데이터 전체에서 차지하는 비율이 매우 작다면, 트리 계열 모델은 이런 전략을 채택 : "Hit는 극도로 드물다 → 그냥 전부 Not-Hit라고 예측해도 정확도는 높게 나온다."
      그래서 모델은 자연스럽게 Majority Class(Non-Hit)에 몰빵한 예측을 하게 된다. 이건 랜덤 포레스트라고 해서 달라지지 않고, 오히려 더 강해진다.
   2. 음향 feature만으로 히트 여부를 설명하기 매우 어려움
      히트곡은 음향적 특성보다 아티스트 인기, 마케팅, 발매 시기, 플레이리스트 편성, 바이럴 같은 외부 요인이 훨씬 큼. 즉 feature가 약함 -> 모델이 히트 패턴을 못 잡음

6. TP가 낮다고 해서 모델이 ‘나쁜 모델’인가?
   - 결론: 아니다. (특히 Feature Importance 분석이 목적이라면 더더욱)
   이번 연구의 목표는 “히트곡에 영향을 주는 feature가 무엇인지 파악하는 것”이며, hit 여부를 완벽히 예측하는 것이 핵심 목적이 아니다.
   Random Forest의 feature importance는 예측 성능이 낮아도 안정적이며 유의미한 정보를 제공한다.
   TP가 낮은 이유는 모델의 성능 문제라기보다 문제의 구조적 한계(클래스 불균형 + feature 한계) 때문에 발생한 자연스러운 현상이다.
   즉, TP가 낮아도 feature importance 분석이라는 연구 목적에는 문제가 없다. 
     
