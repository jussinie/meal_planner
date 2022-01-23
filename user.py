class User:

    def __init__(self, name: str, weight: float, height: int, age: int):
        self.name = name
        self.weight = weight
        self.height = height
        self.age = age
        self.weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    def calculate_bmr(weight: float, height: int, age: int, male: bool):
        if male:
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
            return bmr
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
            return bmr