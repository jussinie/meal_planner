from ingredient import Ingredient

class Recipe:

    def __init__(self, name: str):
        self.name = name
        self.ingredient_list = []

    def add_ingredient(self, ingredient: Ingredient):
        self.ingredient_list.append(ingredient)

    def print_ingredients(self):
        for ingredient in self.ingredient_list:
            print(ingredient.name)
    
    def calculate_totals_for_portion(self):
        total_calories = 0
        for ingredient in self.ingredient_list:
            total_calories += ingredient.kcal
        return total_calories