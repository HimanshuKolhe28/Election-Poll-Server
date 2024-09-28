import json
import requests
from django.shortcuts import render


from election_pollserver.models import State,Party,City,Election,Voter,Result
from django.http import JsonResponse
from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login


from django.views.decorators.http import require_http_methods
import functools


def get_method_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        
        if not request.method == "GET":
            return JsonResponse({
            "message": "method not allowed [GET allowed]",
        })
        return view_func(request)
    return wrapper


def sign_in(request):
    params = json.loads(request.body)
    username = params.get('username')
    password = params.get('password')

    user_instance = authenticate(username=username, password=password)

    if user_instance:
        login(request, user_instance)
        return JsonResponse(dict(
            data=dict(
                id=user_instance.id,
                first_name= user_instance.username
            )
        ))
    else:
        return JsonResponse(dict(
            message="Invalid username or password"
        ))



def state(request):

    if request.method == "POST":
        params = json.loads(request.body)

        instance = State.objects.create(
            title=params.get('title'),
            country = params.get('country')
        )
        return JsonResponse({"data": instance.obj_to_dict()})
    
    if request.method == "GET":
        from django.contrib.auth.models import User
        user = User.objects.get(username="admin")
        groups = [x.name for x in user.groups.all()]
        print("groups", groups)

        if  "MANAGER" in  groups:
            return JsonResponse({"message": "Not enough permissions"})

        params= request.GET
        response = []
        
        title = params.get('title')

        qeryset= State.objects.filter()

        if title:
            qeryset = qeryset.filter(title=title)
        
        for instance in qeryset:
            response.append(instance.obj_to_dict())
    
        return JsonResponse({"data": response})


def create_parties(request):
    if request.method =="POST":
        params = json.loads(request.body)
        instance = Party.objects.create(
            parties_name = params.get("parties_name")
        )
        return JsonResponse({
        "data": instance.obj_to_dict()
        })


def read_parties(request):
    if request.method == "GET":
        params= request.GET
        response = []
        parties_name = params.get('parties_name')
 
        qeryset= Party.objects.filter()

        if parties_name:
            qeryset = qeryset.filter(parties_name=parties_name)
        
        for instance in qeryset:
            response.append(instance.obj_to_dict())
    
        return JsonResponse({
            "message": "successfully read parties",
            "data": response
        })
    
# Update parties

def update_parties(request,pk=None):
    if request.method == "PATCH":
        print("called this api")
        params = json.loads(request.body)

        parties_name =params.get('name')
        instance = Party.objects.get(id=pk)
        instance.parties_name = parties_name
        instance.save()
        return JsonResponse({
            "message": "success",
            "data": instance.obj_to_dict()
        })

def create_cities (request):
    if request.method == "POST":
        params = json.loads(request.body)

        instance = City.objects.create(
            title = params.get('title'),
            state = State.objects.get(id=params.get('state_id'))
        )
        

        return JsonResponse({
        "message": "new state is created",
        "data": instance.obj_to_dict()
        })



def read_cities(request,pk=None):
    if request.method == "GET":
        params= request.GET
        response = []
        title = params.get('title')

        qeryset = City.objects.all()

        if title:
            qeryset = qeryset.filter(title=title)
        
        if pk:
            qeryset = qeryset.filter(id=pk)

        for instance in qeryset:
            response.append(instance.obj_to_dict())
    
        return JsonResponse({
            "message": "successfully read cities",
            "data": response
        }) 



def create_election(request,pk=None):
    if request.method == "POST":
        params= json.loads(request.body)
        party_ids = params.get('party_ids')

        current_date = datetime.now()
        instance = Election.objects.create(             
            date= current_date,

        )
        
        instance.participating_parties.add(*Party.objects.filter(id__in=party_ids))

    return JsonResponse({

        "message": "New election_id is created",
        "data": instance.obj_to_dict()

        })


def read_election(request,pk=None):
    if request.method == "GET":
        params = request.GET
        response = []
        title = params.get('title')

        qeryset= Election.objects.filter()            


        if title:
            qeryset = qeryset.filter(title=title)

         
        if pk:
            qeryset = qeryset.filter(id=pk)

        
        for instance in qeryset:
            response.append(instance.obj_to_dict())
    
        return JsonResponse({
            "message": "successfully read election",
            "data": response
        })



def create_voters(request):
    if request.method=="POST":
        params = json.loads(request.body)

        instance = Voter.objects.create(
            name = params.get('name'),
            date_of_birth = params.get('date_of_birth'),
            address = params.get('address'),
            city = City.objects.get(id=params.get('city_id')),
            election = Election.objects.get(id=params.get("election_id")),
            voted_to = Party.objects.get(id=params.get("party_ids"))


        )

        return JsonResponse({
            'message': 'Voter created successfully',
            "data":instance.obj_to_dict()
            })
       


def declare_result(request,pk=None):
    if request.method == "GET":
        params = request.GET
        election_id = params.get('election_id')

        response = []
        
        election_instance = Election.objects.get(id=election_id)
        city_qeryset = City.objects.filter(state=election_instance.state)

        all_parties = election_instance.participating_parties.all()

        for city in city_qeryset:
            queryset = Voter.objects.filter(election__id=election_id, city=city)

            party_total_voting = []

            for party in all_parties:
                party_total_voting.append(dict(
                    party_name=party.parties_name,
                    total_voting=queryset.filter(voted_to=party).count()
                ))
            

            voter_data = []
            for voter in queryset:
                voter_data.append(dict(
                    voter_name=voter.name,
                    voted_to=voter.voted_to.parties_name,
                ))

  # Sort the list of dictionaries by the 'total_voting' key
        response.sort(key=lambda x: x['result_data']['total_voting'], reverse=True)
        # Get the winning party
        winning_party = response[0]['result_data']['party_name']

            
        response.append(dict(

            city=city.obj_to_dict(),
            total_voting_count=queryset.count(),
            result_data=party_total_voting,
            voting_data=voter_data,
                ))
    
        return JsonResponse({
            "message": "success",
            "data": response,
            "winning_party": winning_party

        })






# @require_http_methods(['POST', 'GET'])
@get_method_required
def declare_result(request, pk=None):
    print("API Called")

    params = request.GET
    election_id = params.get('election_id')
    response = []

    election_instance = Election.objects.get(id=election_id)
    city_queryset = City.objects.filter(state=election_instance.state)
    all_parties = election_instance.participating_parties.all()

    for city in city_queryset:
        queryset = Voter.objects.filter(election__id=election_id, city=city)
        party_total_voting = []

        for party in all_parties:
            party_total_voting.append(dict(
                party_name=party.parties_name,
                total_voting=queryset.filter(voted_to=party).count()
            ))

        party_total_voting.sort(key=lambda x: x['total_voting'], reverse=True)
        winning_party = party_total_voting[0]
        
        voter_data = []

        for voter in queryset:
            voter_data.append(dict(
                voter_name=voter.name,
                voted_to=voter.voted_to.parties_name,
            ))

        response.append(dict(
            city=city.obj_to_dict(),
            total_voting_count=queryset.count(),
            result_data=party_total_voting,
            voting_data=voter_data,
            winning_party=winning_party,
        ))

            

        return JsonResponse({
            "message": "success",
            "data": response,
            "winning_party": winning_party
        })



def voters_status(request):
    if request.method == "GET":
        params = request.GET
        print(params,"NOT_excuted")
        start_date = params.get('start_date')
        end_date = params.get('end_date')
        voters = Voter.objects.filter(registered_at__date__gte = start_date, registered_at__date__lte = end_date)
        response = []
        response = [voter.obj_to_dict() for voter in voters]

        return JsonResponse({
            "message": "success",
            "data": response
        })


def test_API(request, pk=None):
    if request.method == "GET":
        params = request.GET
        response = []

        api_url = "http://127.0.0.1:8000/decl are_result?election_id=2"
        response = requests.get(api_url)
        data = response.json()['data']
        city_ids = []

        for item in data:
            city_details = item.get('city')
            city_ids.append({
                "id": city_details['id'],
                "title": city_details['title']
            })

        return JsonResponse({
            "message": "success",
            "city_ids": city_ids
        })


def call_tp_apiforcity(request,pk=None):
    if request.method == "POST":
        params = request.POST
        response = []
        import requests
        import json

        url = "http://127.0.0.1:8000/create_cities"

        payload = json.dumps({
            "title": "Jalgaonjamod",
            "state_id": "27"
        })
        
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return JsonResponse({
            "message": "success",
            "data": response.json()
        })
 
def Create_result(request):
    if request.method =="POST":
        params = json.loads(request.body)
        instance = Result.objects.create(
            name = params.get("name"),
            Subject = params.get("Subject")
        )
        return JsonResponse({
        "data": instance.obj_to_dict()
        })
    

def Update_result(request,pk=None):
    if request.method =="PATCH":
        params = json.loads(request.body)
        name =params.get('Student_Name')
        instance = Result.objects.get(id=pk)
        instance.name = name
        instance.save()
        return JsonResponse({
            "message": "success",
            "data": instance.obj_to_dict()
        })

def get_string(request):
    if request.method =="GET":
        params = json.loads(request.body)

a = {1,2,3,4,5}
print (type(a))