from django import forms
from django.forms.util import ErrorDict
from django.forms.forms import NON_FIELD_ERRORS
from planner.models import Client
from planner.models import Problem
from accounts.models import Profile

# Moving to crispy forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.layout import Div
from crispy_forms.bootstrap import AppendedText
from crispy_forms.layout import Submit
from crispy_forms.layout import Field
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Button


class SinginForm(forms.Form):
    """
    The sing in form
    """
    username = forms.CharField(
        max_length=200)
    password = forms.CharField(
        max_length=200,
        widget=forms.PasswordInput
    )
    remember_me = forms.BooleanField(required=False)

    def add_form_error(self, message):
        if not self._errors:
            self._errors = ErrorDict()
        if not NON_FIELD_ERRORS in self._errors:
            self._errors[NON_FIELD_ERRORS] = self.error_class()
        self._errors[NON_FIELD_ERRORS].append(message)


class ScheduleFrom(forms.Form):
    """
    Schedule Management form
    """
    profile = forms.ModelChoiceField(
        queryset=Profile.objects.are_doctors()
    )

    start = forms.CharField(
        max_length=200
    )

    end = forms.CharField(
        max_length=200
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_action = '/api/schedules/'
        self.helper.form_id = 'schedule-add-form'
        self.helper.layout = Layout(
            Div(
                AppendedText(
                    'profile',
                    '<i class="icon-user"></i>'
                )
            ),
            Div(
                Div(
                    AppendedText(
                        'start',
                        '<i data-time-icon="icon-time" data-date-icon="icon-calendar"></i>'
                    ),
                    css_class='span6'
                ),
                Div(
                    AppendedText(
                        'end',
                        '<i data-time-icon="icon-time" data-date-icon="icon-calendar"></i>'
                    ),
                    css_class='span6'
                ),
                css_class='row-fluid'
            ),
            FormActions(
                Submit('save', 'Save changes'),
                Button('cancel', 'Cancel', css_class='btn', data_dismiss='modal')
            )
        )
        super(ScheduleFrom, self).__init__(*args, **kwargs)


class ClientForm(forms.Form):
    """
    Client add form
    """
    first_name = forms.CharField(
        max_length=200
    )
    last_name = forms.CharField(
        max_length=200
    )
    telephone = forms.CharField(
        max_length=200
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_action = '/api/clients/'
        self.helper.form_id = 'client-add-form'
        self.helper.layout = Layout(
            Div(
                Div(
                    'first_name',
                    css_class='span6'
                ),
                Div(
                    'last_name',
                    css_class='span6'
                ),
                css_class='row-fluid'
            ),
            Div(
                Div(
                    'telephone',
                    css_class='span6'
                ),
                css_class='row-fluid'
            ),
            FormActions(
                Submit('save', 'Save changes'),
                Button('cancel', 'Cancel', css_class='btn', data_dismiss='modal')
            ),
        )
        super(ClientForm, self).__init__(*args, **kwargs)


class PetForm(forms.Form):
    """
    Pet form
    """
    client = forms.ModelChoiceField(
        queryset=Client.objects.all()
    )
    name = forms.CharField(
        max_length=200
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_action = '/api/pets/'
        self.helper.form_id = 'pet-add-form'
        self.helper.layout = Layout(
            Div(
                Div(
                    'client',
                    css_class='span6'
                ),
                Div(
                    'name',
                    css_class='span6'
                ),
                css_class='row-fluid'
            ),
            FormActions(
                Submit('save', 'Save changes'),
                Button('cancel', 'Cancel', css_class='btn', data_dismiss='modal')
            )
        )
        super(PetForm, self).__init__(*args, **kwargs)


class ProblemForm(forms.Form):
    """
    Problem fill in form
    """
    name = forms.CharField(
        max_length=200,
        help_text='General name of problem'
    )
    code = forms.CharField(
        max_length=200,
        help_text='Problem code name'
    )
    color = forms.CharField(
        max_length=200,
        help_text='Problem color code'
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_action = '/api/problems/'
        self.helper.form_id = 'problem-add-form'
        self.helper.layout = Layout(
            Div(
                Div(
                    'name',
                    css_class='span6'
                ),
                Div(
                    'code',
                    css_class='span6'
                ),
                css_class='row-fluid'
            ),
            Div(
                AppendedText(
                    'color',
                    '<i style="background-color: rgb(255, 146, 180)"></i>'
                ),
            ),
            FormActions(
                Submit('save', 'Save changes'),
                Button('cancel', 'Cancel', css_class='btn', data_dismiss='modal')
            )
        )
        super(ProblemForm, self).__init__(*args, **kwargs)


class VisitForm(forms.Form):
    """
    The visit form
    """

    id = forms.CharField(
    )

    from_date = forms.DateTimeField(
    )
    to_date = forms.DateTimeField(
    )
    problem = forms.ModelChoiceField(
        queryset=Problem.objects.all()
    )
    description = forms.CharField(
        widget=forms.Textarea
    )
    # client = forms.ModelChoiceField(
    #     queryset=Client.objects.all()
    # )
    client = forms.CharField(
        max_length=200
    )
    # pet = forms.ModelChoiceField(
    #     queryset=Pet.objects.all()
    # )
    pet = forms.CharField(
        max_length=200
    )
    appointment_to = forms.ModelChoiceField(
        queryset=Profile.objects.are_doctors()
    )
    appointment_by = forms.ModelChoiceField(
        queryset=Profile.objects.are_registers()
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_action = '/api/visits/'
        self.helper.form_id = 'visit-add-form'
        self.helper.layout = Layout(
            Field(
                'id', type='hidden'
            ),
            Div(
                Div(
                    AppendedText(
                        'from_date',
                        '<i data-time-icon="icon-time" data-date-icon="icon-calendar"></i>'
                    ),
                    css_class='span6',
                ),
                Div(
                    AppendedText(
                        'to_date',
                        '<i data-time-icon="icon-time" data-date-icon="icon-calendar"></i>'
                    ),
                    css_class='span6',
                ),
                css_class='row-fluid',
            ),
            Div(
                Div(
                    'client',
                    css_class='span6'
                ),
                Div(
                    'pet',
                    css_class='span6'
                ),
                css_class='row-fluid'
            ),
            Div(
                Div(
                    'problem',
                    css_class='span6'
                ),
                Div(
                    'description',
                    css_class='span6'
                ),
                css_class='row-fluid'
            ),
            Div(
                Div(
                    AppendedText(
                        'appointment_to',
                        '<i class="icon-user"></i>'
                    ),
                    css_class='span6'
                ),
                Div(
                    AppendedText(
                        'appointment_by',
                        '<i class="icon-user"></i>'
                    ),
                    css_class='span6'
                ),
                css_class='row-fluid'
            ),
            FormActions(
                Submit('save', 'Save changes'),
                Button('cancel', 'Cancel', css_class='btn', data_dismiss='modal'),
            ),
        )
        super(VisitForm, self).__init__(*args, **kwargs)
