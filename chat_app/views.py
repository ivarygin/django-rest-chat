from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic.edit import FormView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from chat_app.forms import SignUpForm
from chat_app.models import UserProfile, Messages
from chat_app.serializers import UserProfileSerializer, MessagesSerializer


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class UsersList(APIView):

    def get(self, request):

        userId = request.GET.get('userId')
        users = UserProfile.objects.exclude(user=userId)
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data)


class MessagesList(APIView):

    def get(self, request):
        fromId = request.GET.get('fromId')
        toId = request.GET.get('toId')
        query = Q(Q(sender=fromId) & Q(receiver=toId)) | Q(Q(sender=toId) & Q(receiver=fromId))
        msgs = Messages.objects.filter(query).order_by('timestamp')
        serializer = MessagesSerializer(msgs, many=True)
        return Response(serializer.data)

    def post(self, request):
        fromId = request.POST.get('fromId', '')
        toId = request.POST.get('toId', '')
        msg = request.POST.get('msg', '')
        sender_user = User.objects.get(pk=fromId)
        receiver_user = User.objects.get(pk=toId)

        try:
            msg_obj = Messages.objects.create(sender=sender_user, receiver=receiver_user, msg=msg)
            msg_obj.save()
            return Response('add successfully', status=status.HTTP_201_CREATED)
        except:
            return Response('error')


@login_required(login_url="/login")
def index(request):
    args = {'user': request.user}
    return render(request, 'messenger.html', args)


def login_redirect(request):

    if request.user.is_authenticated:
        return redirect('/messenger')
    else:
        return redirect('/login')


def signup(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/messenger')
    else:
        form = SignUpForm()

    args = {'form': form}
    return render(request, 'signup.html', args)





