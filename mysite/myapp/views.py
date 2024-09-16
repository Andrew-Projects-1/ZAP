from django.shortcuts import render, redirect
from django.http import JsonResponse #HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime, timezone
from django.contrib import messages
from .forms import SetPasswordForm
import pytz
import hashlib
from django.views.generic.edit import UpdateView
from myapp.decorators import confirm_password

from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView

from .import models
from . import forms

# Create your views here.

def get_pub_date_str(pub_date):
    
    time_diff = datetime.now(timezone.utc) - pub_date

    local_tz = pytz.timezone('America/Los_Angeles') 
    local_dt = pub_date.replace(tzinfo=pytz.utc).astimezone(local_tz)

    # td_sec = time_diff.total_seconds()
    # #if td_sec == 0:
    # #    return str(int(td_sec)) + " seconds ago"
    # if td_sec == 1:
    #     return str(int(td_sec)) + " second ago"
    # if td_sec < 60 or td_sec == 0:
    #     return str(int(td_sec)) + " seconds ago"
    
    # td_min = divmod(td_sec, 60)[0]
    # if td_min == 1:
    #     return str(int(td_min)) + " minute ago"
    # if td_min < 60 and td_min > 1:
    #     return str(int(td_min)) + " minutes ago"
    
    # td_hr = divmod(td_min, 60)[0]
    # if td_hr == 1:
    #     return str(int(td_hr)) + " hour ago"
    # if td_hr < 24 and td_hr > 1:
    #     return str(int(td_hr)) + " hours ago"

    return local_tz.normalize(local_dt).strftime("on %b %d, %Y at %I:%M %p %Z")
    # return pub_date.strftime("on %b %d, %Y at %I:%M %p")



@login_required
def index(request, page=0):
    #return HttpResponse("CINS465 Hello World")
    current_user = request.user
    page_list = list(range(page*10, page*10 + 10, 1))
    squares_list = [x**2 for x in range(10)]
    context = {
        'current_user': current_user,
        'title': 'Zap',
        'msg': 'Hello World',
        'page_list': page_list,
        'squares_list': squares_list,
        'prev_page': page - 1,
        'next_page': page + 1,
        'page': page,
    }
    return render(request, "index.html", context=context)




@login_required
def questions(request):
    if request.method == "POST":
        q_form = forms.QuestionForm(request.POST, request.FILES)
        if q_form.is_valid() and request.user.is_authenticated:
            q_form.save(request)
            #q_form = forms.QuestionForm()
            return redirect("/questions/")
    else:
        q_form = forms.QuestionForm()
    
    context = {
        'title': "Zap ",
        'msg': "Question Forum",
        'q_form': q_form,
        # 'q_list': q_list,
    }
    return render(request, "questions.html", context=context)


@login_required
def rants(request):
    if request.method == "POST":
        r_form = forms.RantsForm(request.POST, request.FILES)
        if r_form.is_valid() and request.user.is_authenticated:
            r_form.save(request)
            #r_form = forms.QuestionForm()
            return redirect("/rants/")
    else:
        r_form = forms.RantsForm()
    
    context = {
        'title': "Zap ",
        'msg': "Rant Forum",
        'r_form': r_form,
        # 'q_list': q_list,
    }
    return render(request, "rants.html", context=context)




@login_required
def question_json(request):
    q_objects = models.QuestionModel.objects.all().order_by("-pub_date")
    q_dictionary = {}
    q_dictionary["questions"] = []
    q_dictionary["current_user"] = request.user.username
    for q in q_objects:
        temp_q = {}
        temp_q["question_text"] = q.question_text
        temp_q["pub_date"] = get_pub_date_str(q.pub_date)
        temp_q["author"] = q.author.username
        temp_q["id"] = q.id
        if q.image:
            temp_q["image"] = q.image.url
            temp_q["image_description"] = q.image_description
        else:
            temp_q["image"] = ""
            temp_q["image_description"] = ""
        a_objects = models.AnswerModel.objects.filter(question=q)
        temp_q["answers"] = []
        for ans in a_objects:
            temp_a = {}
            temp_a["answer_text"] = ans.answer_text
            temp_a["pub_date"] = get_pub_date_str(ans.pub_date)
            temp_a["author"] = ans.author.username
            temp_a["id"] = ans.id
            if ans.image:
                temp_a["image"] = ans.image.url
                temp_a["image_description"] = ans.image_description
            else:
                temp_a["image"] = ""
                temp_a["image_description"] = ""
            temp_q["answers"] += [temp_a]
        q_dictionary["questions"] += [temp_q]
    return JsonResponse(q_dictionary)


@login_required
def rants_json(request):
    r_objects = models.RantsQuestionModel.objects.all().order_by("-pub_date")
    r_dictionary = {}
    r_dictionary["rants"] = []
    r_dictionary["current_user"] = request.user.username
    for r in r_objects:
        temp_r = {}
        temp_r["question_text"] = r.question_text
        temp_r["pub_date"] = get_pub_date_str(r.pub_date)
        temp_r["author"] = r.author.username
        temp_r["id"] = r.id
        if r.image:
            temp_r["image"] = r.image.url
            temp_r["image_description"] = r.image_description
        else:
            temp_r["image"] = ""
            temp_r["image_description"] = ""
        r_objects = models.RantsAnswerModel.objects.filter(question=r)
        temp_r["answers"] = []
        for ans in r_objects:
            temp_a = {}
            temp_a["answer_text"] = ans.answer_text
            temp_a["pub_date"] = get_pub_date_str(ans.pub_date)
            temp_a["author"] = ans.author.username
            temp_a["id"] = ans.id
            if ans.image:
                temp_a["image"] = ans.image.url
                temp_a["image_description"] = ans.image_description
            else:
                temp_a["image"] = ""
                temp_a["image_description"] = ""
            temp_r["answers"] += [temp_a]
        r_dictionary["rants"] += [temp_r]
    return JsonResponse(r_dictionary)




@login_required
def answer_form(request, quest_id):
    quest = models.QuestionModel.objects.get(id=quest_id)
    if request.method == "POST":
        a_form = forms.AnswerForm(request.POST, request.FILES)
        if a_form.is_valid() and request.user.is_authenticated:
            a_form.save(request, quest_id)
            return redirect("/questions/")
    else:
        a_form = forms.AnswerForm()

    context = {
        "form": a_form,
        "quest_id": quest_id,
        "quest": quest,
    }
    return render(request, "answer.html", context=context)


@login_required
def rants_answer_form(request, quest_id):
    quest = models.RantsQuestionModel.objects.get(id=quest_id)
    if request.method == "POST":
        a_form = forms.RantsAnswerForm(request.POST, request.FILES)
        if a_form.is_valid() and request.user.is_authenticated:
            a_form.save(request, quest_id)
            return redirect("/rants/")
    else:
        a_form = forms.RantsAnswerForm()

    context = {
        "form": a_form,
        "quest_id": quest_id,
        "quest": quest,
    }
    return render(request, "rants_answer.html", context=context)




def questions_delete(request, quest_id):
    data = models.QuestionModel.objects.get(id=quest_id)
    data.delete()
    return redirect('/questions')


def rants_delete(request, quest_id):
    data = models.RantsQuestionModel.objects.get(id=quest_id)
    data.delete()
    return redirect('/rants')




def questions_answers_delete(request, quest_id):
    data = models.AnswerModel.objects.get(id=quest_id)
    data.delete()
    return redirect('/questions')


def rants_answers_delete(request, quest_id):
    data = models.RantsAnswerModel.objects.get(id=quest_id)
    data.delete()
    return redirect('/rants')




@login_required
def ind(request):
    current_user = request.user
    context = {
        'title': "Zap Messaging",
        'current_user': current_user,
    }
    return render(request, "chat/ind.html", context=context)

@login_required
def room(request, room_name):
    chat_room, created = models.Room.objects.get_or_create(name=room_name)
    current_user = request.user
    context = {
        'title': "Zap Messaging",
        'current_user': current_user,
        "room_name": room_name,
        'room': chat_room,
    }
    return render(request, "chat/room.html", context=context)







@login_required
def profile(request):
    if request.method == 'POST':
        u_form = forms.UserUpdateForm(request.POST, instance=request.user)
        p_form = forms.ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Your account has been updated!")
            return redirect('/') #Returns to homepage after update
    else:
        u_form = forms.UserUpdateForm(instance=request.user)
        p_form = forms.ProfileUpdateForm(instance=request.user.profile)

    context = {
        "u_form": u_form,
        "p_form": p_form
    }
    return render(request, 'profile.html', context)











@login_required
def community(request):
    current_user = request.user
    context = {
        'title': "Zap Community",
        'current_user': current_user,
    }
    return render(request, "community.html", context=context)


@login_required
def messaging(request):
    current_user = request.user
    context = {
        'title': "Zap Messaging",
        'current_user': current_user,
    }
    return render(request, "messaging.html", context=context)




def register(request):
    if request.method == "POST":
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            form.save(request)
            messages.info(request, f"Your account has been created! You are now able to login.")
            return redirect("/login/")
    else:
        form = forms.RegistrationForm(request.POST)

    context = {
        "form": form,
    }
    return render(request, "registration/register.html", context=context)

@login_required
def SHA(request):
    if request.method == 'POST' and 'text' in request.POST:
        text = request.POST['text']
        hashed_text = hashlib.sha256(text.encode()).hexdigest()
        response_data = {'hashed_text': hashed_text}
        return JsonResponse(response_data)
    current_user = request.user
    context = {
        'title': 'SHA',
        'current_user': current_user,
    }
    return render(request, "SHA.html", context=context)




class ConfirmPasswordView(UpdateView):
    form_class = forms.ConfirmPasswordForm
    template_name = 'confirm_password.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return self.request.get_full_path()


@confirm_password
@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('/')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'password_reset_confirm.html', {'form': form})







def logout_user(request):
    logout(request)
    messages.success(request, f"You have successfully logged out.")
    return redirect("/login/")





class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = forms.ThreadForm()
        context = {
            'form': form
        }
        return render(request, 'create_thread.html', context)
    def post(self, request, *args, **kwargs):
        form = forms.ThreadForm(request.POST)
        username = request.POST.get('username')
        try:
            receiver = User.objects.get(username=username)
            if models.ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = models.ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)
            elif models.ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = models.ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('thread', pk=thread.pk)
            if form.is_valid():
                sender_thread = models.ThreadModel(
                    user=request.user,
                    receiver=receiver
                )
                sender_thread.save()
                thread_pk = sender_thread.pk
                return redirect('thread', pk=thread_pk)
        except:
            messages.error(request, 'Invalid username')
            return redirect('create-thread')

class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = models.ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))
        context = {
            'threads': threads
        }
        return render(request, 'inbox.html', context)


class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form = forms.MessageForm()
        thread = models.ThreadModel.objects.get(pk=pk)
        message_list = models.MessageModel.objects.filter(thread__pk__contains=pk)
        context = {
            'thread': thread,
            'form': form,
            'message_list': message_list
        }
        return render(request, 'thread.html', context)

class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
        form = forms.MessageForm(request.POST, request.FILES)
        thread = models.ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver

        if form.is_valid():
            message = form.save(commit=False)
            message.thread = thread
            message.sender_user = request.user
            message.receiver_user = receiver
            message.save()
        # message = models.MessageModel(
        #     thread=thread,
        #     sender_user=request.user,
        #     receiver_user=receiver,
        #     body=request.POST.get('message')
        # )

        # message.save()

        notification = models.Notification.objects.create(
            notification_type = 4,
            from_user=request.user,
            to_user=receiver,
            thread=thread
            )
        return redirect('thread', pk=pk)

class ThreadNotification(View):
    def get(self, request, notification_pk, object_pk, *args, **kwargs):
        notification = models.Notification.objects.get(pk=notification_pk)
        thread = models.ThreadModel.objects.get(pk=object_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('thread', pk=object_pk)

class RemoveNotification(View):
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = models.Notification.objects.get(pk=notification_pk)

        notification.user_has_seen = True
        notification.save()

        return HttpResponse('Success', content_type='text/plain')