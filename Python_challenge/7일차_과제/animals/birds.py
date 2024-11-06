# birds.py

class Eagle:
    def __init__(self, name, wingspan):
        self.name = name
        self.wingspan = wingspan

    def speak(self):
        return "Screech!"

    def info(self):
        return f"Eagle: {self.name}, Wingspan: {self.wingspan} meters"
