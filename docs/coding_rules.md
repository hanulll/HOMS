# HOMS Coding Rules

Version : v2.0

Last Update : 2026-07-04

---

# 목적

HOMS는 실제 치킨 매장에서 운영되는 AI 플랫폼이다.

모든 개발은 운영 안정성을 최우선으로 한다.

---

# 기본 원칙

1.
운영 중인 기능은 절대 깨지 않는다.

2.
기존 Engine 수정은 최소화한다.

3.
새로운 기능은 가능한 독립 모듈로 개발한다.

4.
Predictor 구조를 우선 사용한다.

5.
Fallback 구조를 항상 고려한다.

---

# 개발 순서

Step 1.
설계

↓

Step 2.
영향 분석

↓

Step 3.
문서 작성

↓

Step 4.
구현

↓

Step 5.
Engine 연결

↓

Step 6.
테스트

↓

Step 7.
Git Commit

↓

Step 8.
운영 적용

---

# 코드 작성 규칙

- 들여쓰기 완료된 코드만 작성한다.
- 복사해서 바로 사용할 수 있는 코드만 작성한다.
- nano 기준으로 설명한다.
- 수정 위치를 명확하게 안내한다.
- 삭제 범위를 먼저 설명한다.
- 붙여넣을 코드를 제공한다.
- 테스트 방법까지 제공한다.

---

# Git Rules

기능 하나당 Commit 하나

예)

feat(predictor): add predictor framework

fix(order): inventory bug

refactor(recipe): optimize recipe engine

docs: update architecture

---

# Documentation Rules

새로운 기능은 반드시 문서를 작성한다.

architecture.md

roadmap.md

changelog.md

관련 기능 문서

---

# Engine Priority

Recipe Engine

↓

Inventory Engine

↓

Forecast Engine

↓

Predictor

↓

Order Engine

↓

Learning Engine

↓

Backtest Engine

---

# Release Policy

Alpha

↓

Beta

↓

Stable

↓

Production

---

# HOMS Goal

치킨 매장 운영을 위한 최고의 AI 운영 플랫폼 구축
