from django import forms
from django.core import validators
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from . import models

from django.contrib.auth.hashers import check_password
from django.utils import timezone


def must_not_be_all_caps(value):
    if value.isupper():
        raise forms.ValidationError("Must not be in all caps. No need to shout!")
    return value    


class QuestionForm(forms.Form):
    question_field = forms.CharField(
        label="Your Question", 
        max_length=280, 
        validators = [
            validators.MinLengthValidator(5),   #(5, message = "You need more characters!")
            must_not_be_all_caps
        ]
    )   
    image = forms.ImageField(label="Image File", required=False)
    image_description = forms.CharField(
        label="Image Description",
        max_length=280,
        required=False,
        validators = [
            validators.MinLengthValidator(5),   #(5, message = "You need more characters!")
            must_not_be_all_caps
        ]
    )
    def save(self, request):
        q_instance = models.QuestionModel()
        q_instance.question_text = self.cleaned_data["question_field"]
        q_instance.author = request.user
        q_instance.image = self.cleaned_data["image"]
        q_instance.image_description = self.cleaned_data["image_description"]
        q_instance.save()
        return q_instance

class AnswerForm(forms.Form):
    answer_field = forms.CharField(
        label="Your Answer", 
        max_length=280, 
        validators = [
            validators.MinLengthValidator(5),   #(5, message = "You need more characters!")
            must_not_be_all_caps
        ]
    )
    image = forms.ImageField(label="Image File", required=False)
    image_description = forms.CharField(
        label="Image Description",
        max_length=280,
        required=False,
        validators = [
            validators.MinLengthValidator(5),   #(5, message = "You need more characters!")
            must_not_be_all_caps
        ]
    )
    def save(self, request, quest_id):
        a_instance = models.AnswerModel()
        a_instance.answer_text = self.cleaned_data["answer_field"]
        a_instance.author = request.user
        a_instance.image = self.cleaned_data["image"]
        a_instance.image_description = self.cleaned_data["image_description"]
        q_instance = models.QuestionModel.objects.get(id=quest_id)
        a_instance.question = q_instance
        a_instance.save()
        return a_instance  

class RantsForm(forms.Form):
    question_field = forms.CharField(
        label="Your Question", 
        max_length=280, 
        validators = [
            validators.MinLengthValidator(5),   #(5, message = "You need more characters!")
            must_not_be_all_caps
        ]
    )   
    image = forms.ImageField(label="Image File", required=False)
    image_description = forms.CharField(
        label="Image Description",
        max_length=280,
        required=False,
        validators = [
            validators.MinLengthValidator(5),   #(5, message = "You need more characters!")
            must_not_be_all_caps
        ]
    )
    def save(self, request):
        r_instance = models.RantsQuestionModel()
        r_instance.question_text = self.cleaned_data["question_field"]
        r_instance.author = request.user
        r_instance.image = self.cleaned_data["image"]
        r_instance.image_description = self.cleaned_data["image_description"]
        r_instance.save()
        return r_instance

class RantsAnswerForm(forms.Form):
    answer_field = forms.CharField(
        label="Your Answer", 
        max_length=280, 
        validators = [
            validators.MinLengthValidator(5),   #(5, message = "You need more characters!")
            must_not_be_all_caps
        ]
    )
    image = forms.ImageField(label="Image File", required=False)
    image_description = forms.CharField(
        label="Image Description",
        max_length=280,
        required=False,
        validators = [
            validators.MinLengthValidator(5),   #(5, message = "You need more characters!")
            must_not_be_all_caps
        ]
    )
    def save(self, request, quest_id):
        a_instance = models.RantsAnswerModel()
        a_instance.answer_text = self.cleaned_data["answer_field"]
        a_instance.author = request.user
        a_instance.image = self.cleaned_data["image"]
        a_instance.image_description = self.cleaned_data["image_description"]
        q_instance = models.RantsQuestionModel.objects.get(id=quest_id)
        a_instance.question = q_instance
        a_instance.save()
        return a_instance  


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label="Username", 
        required=False,
        widget= forms.TextInput(
            attrs={
                'placeholder':'Enter Desired Username',
                'required': 'True',
            }
        )
    )
    password1 = forms.CharField(
        label="Password", 
        required=False,
        widget= forms.PasswordInput(
            attrs={
                'placeholder':'Enter Desired Password',
                'required': 'True',
            }
        )
    )
    password2 = forms.CharField(
        label="Password Confirmation", 
        required=False,
        widget= forms.PasswordInput(
            attrs={
                'placeholder':'Re-enter Desired Password',
                'required': 'True',
            }
        )
    )
    # email = forms.EmailField(label="Email", required=True)
    email = forms.EmailField(
        label="Email", 
        required=False,
        widget= forms.TextInput(
            attrs={
                'placeholder':'Enter Email Address',
                'required': 'True',
            }
        )
    )
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        help_texts = {
            'username': "",
            'email': "",
            'password1': "",
            'password2': "",
        }
        error_messages = {
            'password1': {
                'max_length': "",
            },
        }
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("username", "email")
        labels={
            'username': "Update your username",
            'email': "Update your email address",
        }
        help_texts = {
            'username': "",
            'email': "",
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ('image',)
        labels={
            'image': "Update Image"
        }
        help_texts = {
            'image': "Suuuuup" #dafsdfasfdasdfsadfsadf
        }


class ConfirmPasswordForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('confirm_password', )

    def clean(self):
        cleaned_data = super(ConfirmPasswordForm, self).clean()
        confirm_password = cleaned_data.get('confirm_password')
        if not check_password(confirm_password, self.instance.password):
            self.add_error('confirm_password', 'Password does not match.')

    def save(self, commit=True):
        user = super(ConfirmPasswordForm, self).save(commit)
        user.last_login = timezone.now()
        if commit:
            user.save()
        return user


class ThreadForm(forms.Form):
  username = forms.CharField(label='', max_length=100)
class MessageForm(forms.ModelForm):
  body = forms.CharField(label='', max_length=1000)

  image = forms.ImageField(label="Image File", required=False)

  class Meta:
    model = models.MessageModel
    fields = ['body', 'image']