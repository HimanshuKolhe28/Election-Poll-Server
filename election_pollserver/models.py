from django.db import models


class State(models.Model):
    COUNTRY_MENU = [
        ("IND", "INDIA"),
        ("AUS", "AUSTRALIA")
    ]
    title = models.CharField(max_length=50)
    country = models.CharField(max_length=10, choices=COUNTRY_MENU, default="IND")

    def __str__(self):
        return self.title

    def obj_to_dict(self):
        data = {
            "id":self.id,
            "title":self.title,
            "country":self.country
         }
        return data 


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    def obj_to_dict(self):
        data={
            "id":self.id,
            "state":self.state.title,
            "title":self.title
        }
        return data


class Party(models.Model):
    parties_name = models.CharField(max_length=100)

    def __str__(self):
        return self.parties_name

    def obj_to_dict(self):
        data={
            "id":self.id,
            "parties_name":self.parties_name
        }
        return data
    

class Election(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateField()
    participating_parties = models.ManyToManyField(Party)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)

    def obj_to_dict(self):
        data={
            "id":self.id, 
            "title":self.title,
            "date":self.date,
            "participating_parties":[party.obj_to_dict() for party in self.participating_parties.all()]


        }
        return data


class Voter(models.Model):
    name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    address = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)  
    registered_at = models.DateTimeField(auto_now_add=True)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, null=True, blank=True)
    voted_to = models.ForeignKey(Party, on_delete=models.CASCADE, null=True, blank=True)

    def obj_to_dict(self):
        data={
            "id": self.id,
            "name":self.name,
            "date_of_birth":self.date_of_birth,
            "address":self.address,
            "city":self.city.obj_to_dict(),
            "registered_at":self.registered_at,
            "election":self.election.obj_to_dict(),
            "voted_to":self.voted_to.obj_to_dict(),
        }
        return data
    
class Result(models.Model):
    name = models.CharField(max_length=10)
    Subject = models.CharField(max_length=20)
    
    def obj_to_dict(self):
        data={
            "id":self.id,
            "name":self.name,
            "Subject":self.Subject
        }
        return data
