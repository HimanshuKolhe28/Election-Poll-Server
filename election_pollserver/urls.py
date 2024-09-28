from django.urls import path
from django.contrib import admin 
from election_pollserver.views import state, create_parties, read_parties,update_parties, create_cities,\
    read_cities, create_election, read_election, create_voters, declare_result, test_API, call_tp_apiforcity, voters_status,Create_result,Update_result,\
    sign_in


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sign_in', sign_in),

    path('state', state),
    path('create_parties',create_parties),
    path('read_parties',read_parties),
    path('update_parties/<int:pk>',update_parties),
    path('create_cities',create_cities),
    path('read_cities',read_cities),
    path('create_election',create_election),
    path('read_election',read_election),
    path('create_voters',create_voters),
    path('declare_result',declare_result),
    path('test_API',test_API),
    path('call_tp_apiforcity',call_tp_apiforcity),
    path('voters_status/',voters_status),
    path('Create_result',Create_result),
    path('Update_result/<int:pk>',Update_result)
]
