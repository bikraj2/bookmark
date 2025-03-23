from django.contrib.admin.options import messages
from django.db import reset_queries
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from actions.utils import create_action
from actions.models import Action
from .models import Contact, Profile
from .forms import LoginForm, ProfileEditForm, UserEditForm, UserRegistrationForm
# Create your views here.


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username = cd['username'],password = cd['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse("Authentication Successful")
                else:
                    return HttpResponse("Disabled account")
            else :
                return HttpResponse("Invalid Credentials")
    else:
        form = LoginForm()
        return render(
            request,
            'account/login.html',
            {
                'form': form 
            }
        )
@login_required  
def dashboard(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id',flat=True)
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related(
        'user','user__profile' ## '__' is for joing user and profile tables
    ).prefetch_related('target')[:10]
    return render(
        request,
        'account/dashboard.html',
        {'section':'dashboard','actions':actions}
    )


def register(request):
    if request.method=='POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )

            create_action(new_user,'has created an account')
            new_user.save()
            return render(
                request,
                'account/register_done.html',
                {'new_user':new_user}
            )
        else:
            return render(request,'account/register.html',{'user_form':user_form})
    else:
        user_form = UserRegistrationForm()
        return render(
            request,
            'account/register.html',
            {'user_form':user_form}
        )

@login_required 
def edit(request):
    if request.method =='POST':
        user_form = UserEditForm(
            instance=request.user,
            data = request.POST
        )
        profile_form = ProfileEditForm(
            instance= request.user.profile,
            data = request.POST,
            files= request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Profile Updated Successfully')
        else:
            messages.error(request,'Error Updating your profile')
    else:
        user_form = UserEditForm(instance = request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
            request,
            'account/edit.html',
            {
                'user_form':user_form,
                'profile_form': profile_form
            }
        )

@login_required 
def user_list(request):
    users = User.objects.filter(is_active = True)
    return render(
        request,
        'account/user/list.html',
        {'section':'people','users': users }
    )

@login_required 
def user_detail(request,username):
    user = get_object_or_404(User,username = username,is_active=True)
    return render(
        request,
        'account/user/detail.html',
        {'section':'people','user': user }
    )



@login_required 
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                create_action(request.user ,'is following',user)
                Contact.objects.get_or_create(
                        user_from = request.user,
                        user_to = user
                    )
            else:
                Contact.objects.filter(
                        user_from = request.user,
                        user_to = user
                    ).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status':'error'})
