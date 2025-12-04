# -*- coding: utf-8 -*-
"""
Spotify Top Songs 데이터셋을 기반으로 한
히트곡 예측(Logistic Regression) 모델 코드입니다.

이 노트북은 다음 과정을 포함합니다.
1) 전처리 완료된 데이터 로드 (hit 라벨 포함)
2) 입력(feature) / 타깃(target) 분리
3) Train/Test 분리
4) StandardScaler를 활용한 스케일링
5) 로지스틱 회귀 모델 학습 (Baseline)
6) 클래스 불균형 보정(class_weight='balanced') 모델 학습
7) 두 모델의 평가 지표 비교
8) 회귀 계수를 활용한 피처 중요도 분석

※ 주의: 문자열 컬럼(key, mode, time_signature)은 사용하지 않고
   순수 숫자형 오디오 특성만 사용합니다.
"""

# ================================
# 0. 라이브러리 임포트
# ================================
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


# ================================
# 1. 데이터 로드
# ================================
"""
전처리 단계에서 hit_score 기반으로 만들어진 
'spotify_top_songs_with_hit.csv' 파일을 불러옵니다.
해당 파일에는 이미 hit(0/1) 라벨이 포함되어 있어
바로 모델 학습에 사용할 수 있습니다.
"""

DATA_PATH = "spotify_top_songs_with_hit.csv"  # 같은 폴더에 있어야 함
df = pd.read_csv(DATA_PATH)

print("[INFO] 데이터셋 로드 완료:", df.shape)
print("[INFO] 컬럼 목록:", df.columns.tolist())


# ================================
# 2. Feature / Target 정의
# ================================
"""
입력 변수(Features)로는 **숫자형 오디오 특성 10개**만 사용합니다.
(문자열 범주형: key, mode, time_signature는 제외)

문자열 feature를 그대로 쓰면
'could not convert string to float' 에러가 발생하기 때문에
이번 로지스틱 회귀에서는 제거하고 진행합니다.
"""

FEATURE_COLS = [
    "danceability", "energy", "speechiness", "acousticness",
    "instrumentalness", "liveness", "valence",
    "loudness", "tempo", "duration_ms"
]

TARGET_COL = "hit"

# 혹시라도 결측치가 있으면 제거 (안전장치)
df = df.dropna(subset=FEATURE_COLS + [TARGET_COL]).reset_index(drop=True)

X = df[FEATURE_COLS].copy()
y = df[TARGET_COL].copy()

print("[INFO] Feature Shape:", X.shape)
print("[INFO] Target 분포:")
print(y.value_counts())
print(y.value_counts(normalize=True))


# ================================
# 3. Train/Test Split
# ================================
"""
데이터를 학습용 80% / 테스트용 20%로 나눕니다.
stratify=y 옵션을 사용하여 hit=1의 비율이 학습/테스트에
동일하게 유지되도록 합니다.
"""

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("[INFO] Train Size:", X_train.shape[0])
print("[INFO] Test Size :", X_test.shape[0])


# ================================
# 4. 스케일링 (StandardScaler)
# ================================
"""
로지스틱 회귀는 각 feature의 단위(scale)에 영향을 받기 때문에
평균 0, 표준편차 1 형태로 정규화(Standardization)를 수행합니다.
"""

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# ================================
# 5. Baseline Logistic Regression
# ================================
"""
클래스 불균형(class imbalance)을 고려하지 않은
기본 로지스틱 회귀입니다.
"""

baseline_model = LogisticRegression(
    max_iter=1000,
    solver="lbfgs",
    random_state=42
)
baseline_model.fit(X_train_scaled, y_train)

y_pred_base = baseline_model.predict(X_test_scaled)

print("\n================ Baseline Logistic Regression ================")
print("Accuracy :", accuracy_score(y_test, y_pred_base))
print("Precision:", precision_score(y_test, y_pred_base))
print("Recall   :", recall_score(y_test, y_pred_base))
print("F1 Score :", f1_score(y_test, y_pred_base))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred_base))
print("\nClassification Report:\n", classification_report(y_test, y_pred_base))


# ================================
# 6. Logistic Regression (class_weight='balanced')
# ================================
"""
클래스 불균형을 보정하기 위해
class_weight='balanced' 옵션을 사용합니다.

hit=1 비율이 약 10% 수준의 불균형 데이터이므로,
소수 클래스(hit=1)에 더 큰 가중치를 주어
히트곡을 조금 더 잘 잡아내도록 유도합니다.
"""

balanced_model = LogisticRegression(
    max_iter=1000,
    solver="lbfgs",
    class_weight="balanced",
    random_state=42
)
balanced_model.fit(X_train_scaled, y_train)

y_pred_bal = balanced_model.predict(X_test_scaled)

print("\n================ Logistic Regression (Balanced) ================")
print("Accuracy :", accuracy_score(y_test, y_pred_bal))
print("Precision:", precision_score(y_test, y_pred_bal))
print("Recall   :", recall_score(y_test, y_pred_bal))
print("F1 Score :", f1_score(y_test, y_pred_bal))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred_bal))
print("\nClassification Report:\n", classification_report(y_test, y_pred_bal))


# ================================
# 7. 회귀 계수(Feature Importance) 분석
# ================================
"""
로지스틱 회귀에서 coef 값은 각 feature가
hit(1) 방향으로 예측에 얼마나 기여하는지를 나타냅니다.

양수(+) → hit=1 쪽으로 예측을 밀어줌
음수(-) → hit=0 쪽으로 기여
"""

coef_df = pd.DataFrame({
    "feature": FEATURE_COLS,
    "coef": balanced_model.coef_[0]
}).sort_values("coef", ascending=False)

print("\n================ Feature Coefficients (Balanced Model) ================")
print(coef_df)

print("\n[INFO] 로지스틱 회귀 분석 전체 완료!")