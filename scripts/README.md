# Scripts 폴더 사용 가이드

## popularity_hit_analysis.py

유명도(popularity)가 히트 여부에 영향을 미치는지 분석하는 스크립트입니다.

### 사용 방법

#### Cursor (로컬 환경)
```bash
# 프로젝트 루트에서 실행
python scripts/popularity_hit_analysis.py
```

#### Colab
1. 프로젝트를 Colab에 업로드하거나 Git으로 클론
2. 데이터 파일 위치 확인 (`data/songs_normalize.csv`)
3. 다음 코드로 실행:

```python
# Colab에서 실행 예시
import os
os.chdir('/content/your-project-path')  # 프로젝트 경로로 이동
exec(open('scripts/popularity_hit_analysis.py').read())
```

또는 직접 실행:
```python
!python scripts/popularity_hit_analysis.py
```

### 입력 파일
- `data/songs_normalize.csv` (또는 프로젝트 루트의 `songs_normalize.csv`)

### 출력 파일
- `data/songs_normalize_with_hit.csv` (또는 프로젝트 루트의 `songs_normalize_with_hit.csv`)
  - `hit` 컬럼이 추가된 데이터셋

### 주요 기능
1. 데이터 로드 및 기본 정보 확인
2. 히트곡 레이블 생성 (상위 10% 기준)
3. 히트곡 vs 비히트곡 평균 유명도 비교 분석

