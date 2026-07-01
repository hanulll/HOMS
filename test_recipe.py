from core.recipe_engine import RecipeEngine

engine = RecipeEngine()

print(engine.calculate("허니콤보", 1))
print(engine.calculate("교촌콤보", 1))
print(engine.calculate("살살후라이드", 1))

sales = {
    "교촌콤보": 10,
    "레드콤보": 5,
    "허니한마리": 3,
}

print(engine.calculate_usage(sales))
