from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from piston.handler import BaseHandler
from piston.utils import rc
from planner.models import Client
from planner.models import Pet
from planner.models import Visit
from planner.models import Problem
from planner.models import Schedule
from accounts.models import Profile
from django.core import serializers


class ProfileHandler(BaseHandler):
    model = Profile

    def read(self, request, profile_id=None):
        if profile_id:
            return Profile.objects.get(id=profile_id)
        else:
            return Profile.objects.all()

    def create(self, request):
        if request.content_type:
            data = request.data
            try:
                User.objects.get(username=data['username'])
                return rc.DUPLICATE_ENTRY
            except User.DoesNotExist:
                if data['password1'] == data['password2']:
                    data['password'] = data['password1']
                else:
                    return rc.NOT_FOUND

                doctors_group = Group.objects.get(name='Doctors')
                profile = User.objects.create_user(
                    data['username'],
                    data['email'],
                    data['password']
                )
                profile.groups.add(doctors_group)
                profile.is_staff = False
                profile.save()

                return rc.CREATED

        else:
            super(Profile, self).create(request)

    def update(self, request):
        return rc.NOT_IMPLEMENTER

    def delete(self, request):
        return rc.NOT_IMPLEMENTER


class ScheduleHandler(BaseHandler):
    model = Schedule

    def read(self, request):
        return Schedule.objects.works_today()

    def create(self, request):
        if request.content_type:
            data = request.data
            schedule = Schedule(
                profile=Profile.objects.get(id=data['profile']),
                start=data['start'],
                end=data['end']
            )
            schedule.save()
            return rc.CREATED
        else:
            super(Schedule, self).create(request)

    def update(self, request):
        return rc.NOT_IMPLEMENTER

    def delete(self, request):
        return rc.NOT_IMPLEMENTER


class ProblemHandler(BaseHandler):
    model = Problem

    def read(self, request):
        return Problem.objects.all()

    def create(self, request):
        if request.content_type:
            data = request.data
            problem = Problem(
                name=data['name'],
                code=data['code'],
                color=data['color']
            )
            problem.save()
            return rc.CREATED
        else:
            super(Problem, self).create(request)

    def update(self, request):
        if request.content_type:
            data = request.data
            problem = Problem

            try:
                problem = Problem.objects.get(id=data['id'])
            except problem.DoesNotExist:
                return rc.NOT_FOUND

            problem.name = data['name']
            problem.code = data['code']
            problem.color = data['color']

            problem.save()

            return rc.ALL_OK
        else:
            super(Problem, self).create(request)

    def delete(self, request):
        return rc.NOT_IMPLEMENTER


class PetHandler(BaseHandler):
    """
    Pet model handler
    """
    model = Pet

    def read(self, request, client_id=None):
        """
        Get method returning, depending on the client_id parameter
        """
        if client_id:
            return Pet.objects.filter(client__id=client_id).values('id', 'name')
        else:
            return Pet.objects.all()

    def create(self, request):
        if request.content_type:
            data = request.data

            pet = Pet(
                name=data['name'],
                client=Client.objects.get(id=data['client'])
            )
            pet.save()
            return rc.CREATED
        else:
            super(Pet, self).create(request)

    def update(self, request):
        if request.content_type:
            data = request.data
            pet = Pet

            try:
                pet = Pet.objects.get(id=data['id'])
            except pet.DoesNotExist:
                return rc.NOT_FOUND

            pet.name = data['name']
            pet.client = Client.objects.get(id=data['client'])

            pet.save()
            return rc.ALL_OK
        else:
            super(Pet, self).create(request)

    def delete(self, request):
        return rc.NOT_IMPLEMENTER


class VisitHandler(BaseHandler):
    model = Visit

    fields = (
        'visits', ('id'),
        'from_date',
        'to_date',
        'client',
        'telephone',
        'client_id',
        'pet',
        'pet_id',
        'problem_id',
        'problem',
        'description',
        'appointment_to',
        'appointment_by'
    )

    def read(self, request, timestamp=None):
        if timestamp:
            return Visit.objects.on_that_day(timestamp)
        else:
            return Visit.objects.all()

    def create(self, request):
        if request.content_type:
            data = request.data

            visit = Visit(
                from_date=data['from_date'],
                to_date=data['to_date'],
                problem=Problem.objects.get(
                    id=data['problem']
                ),
                description=data['description'],
                client=Client.objects.find_or_create(
                    full_name=data['client']
                ),
                pet=Pet.objects.find_or_create(
                    name=data['pet'],
                    client=Client.objects.find_or_create(
                        full_name=data['client'],
                        telephone=data['telephone']
                    )
                ),
                appointment_to=User.objects.get(
                    id=data['appointment_to']
                ),
                appointment_by=User.objects.get(
                    id=data['appointment_by']
                )
            )
            visit.save()
            return rc.CREATED
        else:
            super(Visit, self).create(request)

    def update(self, request):
        if request.content_type:
            data = request.data

            print data

            visit = Visit

            try:
                visit = Visit.objects.get(id=data['id'])
            except visit.DoesNotExist:
                return rc.NOT_FOUND

            visit.from_date = data['from_date']
            visit.to_date = data['to_date']
            visit.problem = Problem.objects.get(
                id=data['problem']
            )
            visit.description = data['description']
            visit.client = Client.objects.find_or_create(
                full_name=data['client'],
                telephone=data['telephone']
            )
            visit.pet = Pet.objects.find_or_create(
                name=data['pet'],
                client=Client.objects.find_or_create(
                    full_name=data['client'],
                    telephone=data['telephone']
                )
            )
            visit.appointment_to = User.objects.get(
                id=data['appointment_to'])
            visit.appointment_by = User.objects.get(
                id=data['appointment_by'])

            visit.save()

            return rc.ALL_OK
        else:
            super(Visit, self).create(request)

    def delete(self, request):
        return rc.NOT_IMPLEMENTER


class ClientHandler(BaseHandler):
    model = Client

    def read(self, request):
        results_list = []
        for client in Client.objects.all():
            results_list.append({
                'id': client.id,
                'full_name': client.first_name + ' ' + client.last_name,
                'first_name': client.first_name,
                'last_name': client.last_name
            })
        return results_list

    def create(self, request):
        if request.content_type:
            data = request.data

            client = Client
            try:
                client = Client.objects.get(
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    telephone=data['telephone']
                )
                return rc.DUPLICATE_ENTRY
            except client.DoesNotExist:
                client = Client(
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    telephone=data['telephone']
                )
                client.save()
                return rc.CREATED
        else:
            super(Client, self).create(request)

    def update(self, request):
        if request.content_type:
            data = request.data

            client = Client

            try:
                client = Client.objects.get(
                    id=data['id']
                )
                client.first_name = data['first_name']
                client.last_name = data['last_name']
                client.telephone = data['telephone']
                client.save()
                return rc.ALL_OK
            except client.DoesNotExist:
                return rc.NOT_FOUND
        else:
            super(Client, self).create(request)

    def delete(self, request):
        return rc.NOT_IMPLEMENTER
