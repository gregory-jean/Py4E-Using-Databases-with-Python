# Creating the class
class PartyAnimal:
    # All partyAnimal objects will have a var named x with a value of 0
    x = 0

    def party(self) :
        self.x = self.x + 1
        print("So far", self.x)

# Create a new instance of the PartyAnimal Class
an = PartyAnimal()

# Invoke the party method 3 times
an.party()
an.party()
an.party()