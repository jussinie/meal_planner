class Ingredient:

    def __init__(self, name: str, kcal: int, carbohydrates: float, protein: float, fat: float, salt: float):
        self.name = name
        self.kcal = kcal
        self.carbs = carbohydrates
        self.protein = protein
        self.fat = fat
        self.salt = salt