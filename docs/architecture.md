# HOMS Architecture

Version : v2.0

Last Update : 2026-07-04

---

# 목적

HOMS(Hanul Order Management System)는
치킨 매장 운영을 위한 AI 기반 운영 플랫폼이다.

운영 안정성을 최우선으로 하며,
모든 기능은 독립적인 Engine 구조를 기반으로 개발한다.

---

# 전체 구조

```
                Sales Data
                     │
                     ▼
            Pipeline 2130 / 2355
                     │
                     ▼
             Database Engine
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
 Learning Engine           Backtest Engine
        │                         │
        └────────────┬────────────┘
                     ▼
             Forecast Engine
                     │
                     ▼
           Predictor Framework
        ┌──────┬──────┬──────┬──────┐
        ▼      ▼      ▼      ▼
     Recent Weekday Seasonal Today
                     │
                     ▼
            (Future Weight Engine)
                     │
                     ▼
             Recipe Engine
                     │
                     ▼
           Inventory Engine
                     │
                     ▼
             Order Engine
                     │
                     ▼
          Telegram Report Engine
```

---

# Engine 구성

## Recipe Engine

메뉴 판매량을 원재료 사용량으로 변환한다.

---

## Inventory Engine

현재 재고

입고

사용량

예상 재고를 계산한다.

---

## Forecast Engine

판매량을 예측한다.

Predictor Framework의 결과를 사용할 수 있다.

---

## Predictor Framework

Forecast Engine의 AI 보조 계층

현재

- Recent Predictor
- Weekday Predictor
- Seasonal Predictor
- Today Predictor

향후

- Weight Engine
- Confidence Engine
- Weather Predictor
- Holiday Predictor
- Event Predictor

---

## Learning Engine

Forecast 오차를 학습한다.

---

## Backtest Engine

Forecast 정확도를 검증한다.

---

## Order Engine

예상 부족 재고를 계산하고

발주량을 결정한다.

---

## Telegram Engine

운영 결과를 Telegram으로 전송한다.

---

# 개발 원칙

모든 신규 기능은

Predictor

또는

독립 Engine

형태로 개발한다.

기존 Engine 수정은 최소화한다.

---

# 목표

HOMS를

치킨 매장 전용 AI 운영 플랫폼으로 발전시킨다.
