from django.contrib import admin
    
from .models import State,Party,City,Election,Voter

admin.site.register(State)
admin.site.register(Party)
admin.site.register(Election)
admin.site.register(City)
admin.site.register(Voter)



