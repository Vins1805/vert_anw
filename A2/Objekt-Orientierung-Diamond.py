class Animal:
    def __init__(self, weight, height):
        print("Animal init begin")
        self.weight = weight
        self.height = height
        print("Animal init end")

class Lion(Animal):
    def __init__(self, weight, height):
        print("Lion init begin")
        super().__init__(weight, height)
        print("Lion init end")

class Tiger(Animal):
    def __init__(self, weight, height):
        print("Tiger init begin")
        super().__init__(weight, height)
        print("Tiger init end")

class Liger(Lion, Tiger):
    def __init__(self, weight, height, location):
        print("Liger init begin")
        #Tiger.__init__(weight, height, location)
        #Lion.__init__(weight, height, location)
        super().__init__(weight, height)
        self.location = location
        print("Liger init end")

liger = Liger(100, 120, "Savanna")

