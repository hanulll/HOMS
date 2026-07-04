"""
HOMS Predictor Manager

기능
- Predictor 통합 관리
- Recent Predictor
- Weekday Predictor
- Seasonal Predictor
- Today Predictor
- 예측 결과 합성
"""

from __future__ import annotations

from typing import Dict

from .recent_predictor import RecentPredictor
from .weekday_predictor import WeekdayPredictor
from .seasonal_predictor import SeasonalPredictor
from .today_predictor import TodayPredictor


class PredictorManager:

    def __init__(self):

        self.recent = RecentPredictor()

        self.weekday = WeekdayPredictor()

        self.seasonal = SeasonalPredictor()

        self.today = TodayPredictor()

    # ------------------------------------------------------
    # Sales Prediction
    # ------------------------------------------------------

    def predict(
        self,
    ) -> Dict[str, float]:

        print("[Predictor] Manager Start")

        recent_sales = self.recent.predict()

        print("[Predictor] Recent OK")

        weekday_sales = self.weekday.predict()

        print("[Predictor] Weekday OK")

        seasonal_sales = self.seasonal.predict()

        print("[Predictor] Seasonal OK")

        today_sales = self.today.predict()

        print("[Predictor] Today OK")

        menus = (

            set(recent_sales)

            |

            set(weekday_sales)

            |

            set(seasonal_sales)

            |

            set(today_sales)

        )

        result = {}

        for menu in menus:

            recent = recent_sales.get(
                menu,
                0.0,
            )

            weekday = weekday_sales.get(
                menu,
                0.0,
            )

            seasonal = seasonal_sales.get(
                menu,
                0.0,
            )

            today = today_sales.get(
                menu,
                0.0,
            )

            values = [

                recent,

                weekday,

                seasonal,

                today,

            ]

            values = [

                value

                for value in values

                if value > 0

            ]

            if not values:

                continue

            result[menu] = round(

                sum(values)

                /

                len(values),

                2,

            )

        print("[Predictor] Complete")

        return result

# ==========================================================
# END OF FILE
# ==========================================================
