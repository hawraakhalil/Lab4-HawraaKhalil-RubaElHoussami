class Person:
    def __init__(self, name: str, age: int, email: str):
        self.name = name
        self.age = age
        self._email = email
    
    def introduce(self):
        print(f'Hello, my name is {self.name} and I am {self.age} years old.')
