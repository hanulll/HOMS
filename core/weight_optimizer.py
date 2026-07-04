"""
==========================================================
HOMS Weight Optimizer
==========================================================
"""

from __future__ import annotations

import json

from pathlib import Path


class WeightOptimizer:

    DEFAULT = {

        "average": 0.50,

        "recent": 0.30,

        "today": 0.20,

    }

    def __init__(

        self,

    ):

        self.path = Path(

            "~/HOMS/data/forecast_weights.json"

        ).expanduser()

    # ------------------------------------------------------
    # 현재 가중치
    # ------------------------------------------------------

    def load(

        self,

    ):

        if not self.path.exists():

            return dict(

                self.DEFAULT

            )

        with open(

            self.path,

            "r",

            encoding="utf-8",

        ) as f:

            return json.load(

                f

            )

    # ------------------------------------------------------
    # 저장
    # ------------------------------------------------------

    def save(

        self,

        weights,

    ):

        with open(

            self.path,

            "w",

            encoding="utf-8",

        ) as f:

            json.dump(

                weights,

                f,

                indent=4,

                ensure_ascii=False,

            )

    # ------------------------------------------------------
    # 최근 가중치
    # ------------------------------------------------------

    def current(

        self,

    ):

        return self.load()

    # ------------------------------------------------------
    # 가중치 변경
    # ------------------------------------------------------

    def update(

        self,

        average=None,

        recent=None,

        today=None,

    ):

        weights = self.load()

        if average is not None:

            weights[
                "average"
            ] = round(

                average,

                4,

            )

        if recent is not None:

            weights[
                "recent"
            ] = round(

                recent,

                4,

            )

        if today is not None:

            weights[
                "today"
            ] = round(

                today,

                4,

            )

        total = (

            weights["average"]

            +

            weights["recent"]

            +

            weights["today"]

        )

        weights = {

            k: round(

                v / total,

                4,

            )

            for k, v in weights.items()

        }

        self.save(

            weights,

        )

        return weights


    # ------------------------------------------------------
    # 자동 최적화
    # ------------------------------------------------------

    def optimize(

        self,

        average_error,

    ):

        weights = self.load()

        if average_error > 20:

            weights["today"] += 0.05

            weights["average"] -= 0.03

            weights["recent"] -= 0.02

        elif average_error > 10:

            weights["today"] += 0.02

            weights["average"] -= 0.01

            weights["recent"] -= 0.01

        total = (

            weights["average"]

            +

            weights["recent"]

            +

            weights["today"]

        )

        for key in weights:

            weights[key] = round(

                weights[key] / total,

                4,

            )

        self.save(

            weights,

        )

        return weights

    # ------------------------------------------------------
    # Grid Search
    # ------------------------------------------------------

    def optimize_grid(

        self,

        scores,

    ):

        best_error = 999999.0

        best = self.load()

        for avg in range(

            30,

            71,

            5,

        ):

            for recent in range(

                10,

                51,

                5,

            ):

                today = 100 - avg - recent

                if today < 0:

                    continue

                error = scores(

                    avg / 100,

                    recent / 100,

                    today / 100,

                )

                if error < best_error:

                    best_error = error

                    best = {

                        "average": round(

                            avg / 100,

                            2,

                        ),

                        "recent": round(

                            recent / 100,

                            2,

                        ),

                        "today": round(

                            today / 100,

                            2,

                        ),

                    }

        self.save(

            best,

        )

        return best
