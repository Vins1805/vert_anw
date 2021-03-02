class Animal:
    def __init__(self, weight, height):
        print("Animal init begin")
        self.weight = weight
        self.height = height
        print("Animal init end")

class Lion(Animal):
    def __init__(self, weight, height, location):
        print("Lion init begin")
        super().__init__(weight, height)
        self.location = location
        print("Lion init end")

class Tiger(Animal):
    def __init__(self, weight, height, location):
        print("Tiger init begin")
        super().__init__(weight, height)
        self.location = location
        print("Tiger init end")

class Wolf(Animal):
    def __init__(self, weight, height, location):
        print("Wolf init begin")
        super().__init__(weight, height)
        self.location = location
        print("Wolf init end")

wolf = Wolf(100, 120, "forest")
