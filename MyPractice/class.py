class Car:
    def __init__(self,make,model,year):
        self.make=make
        self.year=year
        self.model=model

    def CarDetail(self):
        print(f" car is {self.make} make and launch year is {self.year}")
    
    def CarModel(self):
        print(f"car model: {self.model}")


mycar=Car("porsche","911",1969)

mycar.CarDetail()
mycar.CarModel()
        
