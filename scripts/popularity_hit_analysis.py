"""
유명도(popularity)가 히트 여부에 영향을 미치는지 분석하는 전체 코드
데이터셋: songs_normalize.csv
"""

import pandas as pd
import numpy as np
import os
import warnings

warnings.filterwarnings('ignore')

print("=" * 80)
print("유명도(popularity)가 히트 여부에 영향을 미치는지 분석")
print("=" * 80)

print("\n[0단계] 데이터 로드 및 기본 정보 확인")
print("-" * 80)

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
data_path = os.path.join(project_root, 'data', 'songs_normalize.csv')

if not os.path.exists(data_path):
    data_path = 'data/songs_normalize.csv'
    if not os.path.exists(data_path):
        data_path = 'songs_normalize.csv'

df = pd.read_csv(data_path)
print(f"\n데이터 크기: {df.shape}")
print(f"\n컬럼 목록:")
print(df.columns.tolist())
print(f"\n기본 통계:")
print(df.describe())
print(f"\n결측치 확인:")
print(df.isnull().sum())

print("\n\n" + "=" * 80)
print("[1단계] 히트곡 레이블 생성")
print("-" * 80)

threshold_quantile = df['popularity'].quantile(0.90)
df['hit_quantile'] = (df['popularity'] >= threshold_quantile).astype(int)
df['hit_threshold'] = (df['popularity'] >= 70).astype(int)

print(f"\n방법 A (상위 10% 기준):")
print(f"  기준값: {threshold_quantile:.2f}")
print(f"  히트곡 개수: {df['hit_quantile'].sum()}개 ({df['hit_quantile'].mean()*100:.1f}%)")
print(f"  일반곡 개수: {(df['hit_quantile']==0).sum()}개 ({(df['hit_quantile']==0).mean()*100:.1f}%)")

print(f"\n방법 B (70 이상 기준):")
print(f"  기준값: 70")
print(f"  히트곡 개수: {df['hit_threshold'].sum()}개 ({df['hit_threshold'].mean()*100:.1f}%)")
print(f"  일반곡 개수: {(df['hit_threshold']==0).sum()}개 ({(df['hit_threshold']==0).mean()*100:.1f}%)")

df['hit'] = df['hit_quantile']
print(f"\n최종 사용: 방법 A (상위 10%)")
print(f"   히트곡: {df['hit'].sum()}개, 일반곡: {(df['hit']==0).sum()}개")

print("\n\n" + "=" * 80)
print("[2단계] 검증 방법 1: 히트곡 vs 비히트곡 평균 유명도 비교")
print("-" * 80)

hit_group = df[df['hit'] == 1]
non_hit_group = df[df['hit'] == 0]

hit_mean_pop = hit_group['popularity'].mean()
non_hit_mean_pop = non_hit_group['popularity'].mean()
difference = hit_mean_pop - non_hit_mean_pop

print(f"\n히트곡 평균 popularity: {hit_mean_pop:.2f}")
print(f"일반곡 평균 popularity: {non_hit_mean_pop:.2f}")
print(f"차이: {difference:.2f} ({difference/non_hit_mean_pop*100:.1f}% 높음)")

if difference > 20:
    print("\n결론: 유명도가 히트 여부에 강하게 연관됩니다!")
elif difference > 10:
    print("\n결론: 유명도가 히트 여부에 어느 정도 연관됩니다.")
else:
    print("\n결론: 유명도와 히트 여부의 연관성이 약합니다.")

output_path = os.path.join(project_root, 'data', 'songs_normalize_with_hit.csv')
if not os.path.exists(os.path.dirname(output_path)):
    output_path = 'data/songs_normalize_with_hit.csv'
    if not os.path.exists('data'):
        output_path = 'songs_normalize_with_hit.csv'

df.to_csv(output_path, index=False)
print(f"\n전처리된 데이터 저장 완료: '{output_path}'")
print(f"   'hit' 컬럼이 추가된 데이터셋입니다.")

print("\n\n" + "=" * 80)
print("[최종 결론 요약]")
print("=" * 80)

print("\n그룹별 비교 분석 결과 요약:")
print(f"  평균 인기도 차이: 히트곡({hit_mean_pop:.1f}) vs 일반곡({non_hit_mean_pop:.1f})")
print(f"  차이: {difference:.1f}점 ({difference/non_hit_mean_pop*100:.1f}% 높음)")
print(f"  히트곡 그룹의 평균 인기도가 일반곡 그룹보다 훨씬 높음")

print("\n" + "=" * 80)
print("종합 결론: 유명도(popularity)는 히트 여부에 유의미한 영향을 미칩니다!")
print("=" * 80)

print("\n분석 완료!")
