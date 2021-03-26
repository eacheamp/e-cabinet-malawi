from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.utils.decorators import method_decorator


from django.contrib.auth import authenticate, login, logout
from braces.views import GroupRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import MotionForm
from .models import Motion


# Error Pages #
def error_400_view(request,exception):
    return render(request,'400.html')

def error_403_view(request,exception):
    return render(request,'403.html')

def error_404_view(request,exception):
    return render(request,'404.html')

def error_500_view(request):
    return render(request,'500.html')

class new_home(TemplateView):
    template_name = 'new_home.html'

class Home(TemplateView):
    template_name = 'home.html'

class About(TemplateView):
    template_name = 'about.html'

class After_vote(LoginRequiredMixin,TemplateView):
    template_name = 'After_vote.html'

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

class Motion_pass(DetailView):
    model = Motion
    template_name = 'motion_pass.html'
    context_object_name = 'motions'

    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'

class Motion_fail(DetailView):
    model = Motion
    template_name = 'motion_fail.html'
    context_object_name = 'motions'

    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {

    }
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def e_cabinet(request):
    motions = Motion.objects.all()

    motion_paginator = Paginator(motions, 1)

    page_number = request.GET.get('page')

    page = motion_paginator.get_page(page_number)


    context = {
        'page': page,
        'count': motion_paginator.count,
    }
    return render(request, 'e-cabinet.html', context)


class VoteMotionView(GroupRequiredMixin, UpdateView):
    model = Motion
    template_name = 'vote_motion.html'
    context_object_name = 'motions'
    fields = ('title', 'ministry', 'summary', 'cabinet_vote')

    group_required = [u"Admin", u"Chair", u"Cabinet_Members"]
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def post(self, request, pk):
        motions = Motion.objects.get(pk=pk)
        if request.POST['cabinet_vote'] == '1':
            motions.Votes_Against += 1
        elif request.POST['cabinet_vote'] == '2':
            motions.Votes_Against += 1
        elif request.POST['cabinet_vote'] == '3':
            motions.Votes_Nodesc += 1
        else:
            return HttpResponse(400, 'Invalid Action')
        motions.save()
        context = {
            'motions': motions
        }
        return render(request, 'After_vote.html')

def cabinet_results(request):
    motions = Motion.objects.all()
    context = {
        'motions': motions,
    }
    return render(request, 'cabinet_results.html', context)

class Chair_Desc(GroupRequiredMixin,UpdateView):
    model = Motion
    template_name = 'chair_desc.html'
    context_object_name = 'motions'
    fields = ('title', 'summary', 'chair_vote')

    group_required = [u"Admin", u"Chair", u"Cabinet_Members"]
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def post(self, request, pk):
        motions = Motion.objects.get(pk=pk)
        if request.POST['chair_vote'] == '1':
            motions.final_vote ='Motion Approved'

        elif request.POST['chair_vote'] == '2':
            motions.final_vote = 'Motion Vetoed'

        elif request.POST['chair_vote'] == '3':
            motions.final_vote = 'Tabled Until the next Session'
        else:
            return HttpResponse(400, 'Invalid Action')
        motions .save()
        context = {
            'motions': motions,
        }
        return render(request, 'After_vote_final.html', context)


def chair_list(request):
    motions = Motion.objects.all()
    context = {
        'motions': motions,
    }
    return render(request, 'chair_motion_list.html', context)

def final_ruling(request):
    motions = Motion.objects.all()
    context = {
        'motions': motions,
    }
    return render(request, 'final_results.html', context)


# def final_vote(request):
#     if request.method =='POST':
#         if request.POST.get('Final_vote'):
#             saved_vote = Motion()
#             saved_vote.Final_vote=request.POST.get('Final_vote')
#             saved_vote.save()
#     return render(request, 'final_results.html',{'Final_vote':display_votes})

# def upload_motion(request):
#     if request.method == 'POST':
#         form = MotionForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('motion_list')
#     else:
#         form = MotionForm
#     return render(request, 'upload_motion.html', {
#         'form': form
#     })

# def motion_list(request):
#     motions = Motion.objects.all()
#     context = {
#         'motions': motions,
#     }
#     return render(request, 'motion_list.html', context)
