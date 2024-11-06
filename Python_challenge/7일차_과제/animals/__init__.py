# mammals.py

class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def speak(self):
        return "Woof!"

    def info(self):
        return f"Dog: {self.name}, Breed: {self.breed}"
