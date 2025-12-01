import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# =========== 1. 데이터 로드 ===========
df = pd.read_csv('spotify_top_songs_with_hit.csv')
print(f" 데이터 로드 완료: {df.shape}")

# 특징 선택
audio_features = [
    'danceability', 'energy', 'speechiness', 'acousticness',
    'instrumentalness', 'liveness', 'valence',
    'loudness', 'tempo', 'duration_ms'
]
categorical_features = ['key', 'mode', 'time_signature']

X_audio = df[audio_features].copy()
X_cat = df[categorical_features].copy()
print(f"음악 특징: {len(audio_features)}개")
print(f"범주형 특징: {len(categorical_features)}개")

# 범주형 데이터 변환
for col in categorical_features:
    le = LabelEncoder()
    X_cat[col] = le.fit_transform(X_cat[col])

X = pd.concat([X_audio, X_cat], axis=1)
y = df['hit']
print(f"범주형 데이터 숫자 변환 완료")

# 데이터 분할 (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"✓ 훈련 데이터: {len(X_train)}개")
print(f"✓ 테스트 데이터: {len(X_test)}개")

# 정규화
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print(f"✓ 데이터 정규화 완료")

# =========== 2. 모델 훈련 ===========
mlp = MLPClassifier(
    hidden_layer_sizes=(128, 64, 32),
    activation='relu',
    solver='adam',
    max_iter=500,
    random_state=42,
    early_stopping=True,
    validation_fraction=0.1
)
print(f" MLP 모델 생성")
print(f"  - 은닉층: {mlp.hidden_layer_sizes}")
print(f"  - 활성화함수: {mlp.activation}")
print(f"  - 최적화: {mlp.solver}")

# 모델 훈련
mlp.fit(X_train_scaled, y_train)
print(f" 모델 훈련 완료")
print(f"  - 반복 횟수: {mlp.n_iter_}")

# =========== 3. 모델 평가 ===========
y_pred = mlp.predict(X_test_scaled)
print(f" 테스트 데이터 예측 완료")

# 성능 지표 계산
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# 결과 출력
print(f"\n 모델 성능 지표:")
print(f"  - 정확도(Accuracy):   {accuracy:.4f}")
print(f"  - 정밀도(Precision):  {precision:.4f}")
print(f"  - 재현율(Recall):     {recall:.4f}")
print(f"  - F1-Score:          {f1:.4f}")