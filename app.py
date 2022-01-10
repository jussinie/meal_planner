from typing_extensions import Self
from flask import Flask

app = Flask(__name__)

class User:

    def __init__(self, name: str, weight: float, height: int, age: int):
        self.name = name
        self.weight = weight
        self.height = height
        self.age = age

user = User("Jussi", 87.0, 186, 34)

class Ingredient:

    def __init__(self, name: str, kcal: int, carbohydrates: int, protein: int, fat: int):
        self.name = name
        self.kcal = kcal
        self.carbs = carbohydrates
        self.protein = protein
        self.fat = fat

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

@app.route("/")
def index():
    kaurahiutale = Ingredient("kaurahiutale", 100, 24, 45, 5)
    puuro = Recipe("puuro")
    puuro.add_ingredient(kaurahiutale)
    puuro.print_ingredients()
    return f'heippa {user.name}, your BMR is {calculate_bmr(user.weight, user.height, user.age, True)}'

def calculate_bmr(weight: float, height: int, age: int, male: bool):
    if male:
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
        return bmr
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
        return bmr

 