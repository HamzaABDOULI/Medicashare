from django.shortcuts import render
from django.db.models import Q
import datetime 
from django.conf import settings
from django.core.mail import send_mail ,BadHeaderError ,EmailMultiAlternatives
from django.shortcuts import render,redirect,reverse,HttpResponseRedirect
from .forms import UserCreationForm ,UserUpdateForm , ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404
from .models import Post ,Notification
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


#===== home page  =====#

villes = {
    'Ariana':"Ariana,36.852200,10.171650,4",
    'Beja':"Beja,36.733630,9.184856,4",
    'Ben Arous':"Ben Arous,36.745534,10.240315,4",
    'Gabes':"Gabes,33.884575,10.101886,4",
    'Gafsa':"Gafsa,34.455209,8.803775,4",
    'Jendouba':"Jendouba,36.506735,8.775372,4",
    'Kairouan':"Kairouan,35.667109,10.086506,4",
    'Kasserine':"Kasserine,35.173559,8.832664,4",
    'kebili':"kebili,33.709094,8.974199,4",
    'Kef':"Kef,36.168519,8.712620,4",
    'Mahdia':"Mahdia,35.502355,11.046392,4",
    'Manouba':"Manouba,36.801499,10.110962,4",
    'Medenine':"Medenine,33.420715,10.479190,4",
    'Monastir':"Monastir,35.742942,10.855463,4",
    'Nabeul':"Nabeul,36.496562,10.764780,4",
    'Sidi Bouzid':"Sidi Bouzid,35.095913,9.419010,4",
    'Tataouine':"Tataouine,33.001953,10.477893,4",
    'Tozeur':"Tozeur,34.137544,8.133609,4",
    'Tunis':"Tunis,36.813730,10.184009,4",
    'Zaghouan':"Zaghouan,36.406963,10.140064,4",
    'Bizerte':"Bizerte,37.289397,9.881885,4",
    'Sousse':"Sousse,35.824816,10.633118,4",
    'Sfax':"Sfax,34.783653,10.710093,4",
    'Siliana':"Siliana,36.089024,9.362840,4",
}

# villes ={'Sousse':"Sousse,35.824816,10.633118,4",
#             'Sfax':"Sfax,34.783653,10.710093,4",
#             'Siliana':"Siliana,36.089024, 9.362840,4",
#             }

@login_required(login_url='user:login')
def home(request):
    if request.method == 'POST':
        searchItem = request.POST['name']
        #searchPlace = request.POST['current_place']  ###
        choice = request.POST['type']
        c_place = request.POST['city']    ###
        if request.POST['city'] == 'All cities':       ###
            return redirect('user:search',choice=choice,title=searchItem,c_place='all')    ###
        else :
            return redirect('user:search',choice=choice,title=searchItem,c_place=c_place)       ###
    
    requestsList = Post.objects.filter(post_type='R',show_post="yes",isDonated="no",isReceived="no")
    donationsList = Post.objects.filter(post_type='D',show_post="yes",isDonated="no",isReceived="no")###.filter(Q())
    nots_not_seen = len(Notification.objects.filter(receiver=request.user,status="no"))

    page = request.GET.get('page1', 1)
    paginator = Paginator(donationsList,5)
    try:
        donations = paginator.page(page)
    except PageNotAnInteger:
        donations = paginator.page(1)
    except EmptyPage:
        donations = paginator.page(paginator.num_pages)
    
    page = request.GET.get('page2', 1)
    paginator = Paginator(requestsList, 5)
    try:
        requests = paginator.page(page)
    except PageNotAnInteger:
        requests = paginator.page(1)
    except EmptyPage:
        requests = paginator.page(paginator.num_pages)
    #to mark map 
    RequestLocations =[]    
    DonationLocations =[]    
    donationsByCity =[]
    requestsByCity =[]
    
    for r in requestsList :
        if (r.current_place not in requestsByCity ):
            requestsByCity.append(r.current_place)
            RequestLocations.append(villes[r.current_place])
    
    for d in donationsList :
        if (d.current_place not in donationsByCity ):
            donationsByCity.append(d.current_place)
            DonationLocations.append(villes[d.current_place])
    

    context={
        'requests':requests,
        'donations':donations,
        'nb_nots':nots_not_seen,
        'title':f'MedicaShare | {request.user}',
        'fullname':f'{request.user.first_name}-{request.user.last_name}',
        'villes1':DonationLocations,
        'villes2':RequestLocations,
        'max1':len(DonationLocations),
        'max2':len(DonationLocations),
    }
    return render(request,'home.html',context)

#====== register + login + logout ======#

def register(request):
    if request.user.is_authenticated :
        return redirect(f'/')
        # return redirect('profile',username=request.user.username)
    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            #username = form.cleaned_data['username']
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            messages.success(request, f' {new_user} You are registered successfuly')
            return redirect('user:login')
            
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {
        'form': form,
    })

def user_login(request):
    if request.user.is_authenticated :
        return redirect(f'/')
        # return redirect('profile',username=request.user.username)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
            # return redirect('profile',username=request.user.username)
        else:
            messages.warning(request, 'username or password incorrect ')

    return render(request, 'login.html',{'title': 'login',})

@login_required(login_url='user:login')
def user_logout(request):
    logout(request)
    return redirect('home:index')


#====== Create Post + detail + upadate + delete + search ======#

@login_required(login_url='user:login')
def newRequest(request):
    if request.method == 'POST':
        newpost =Post.create_request(request)

        messages.success(request, 'Your request was successfuly submited ')
        return redirect('user:detail',slug_title=newpost.slug_title,post_id=newpost.id )
        
    return render(request, 'newPost.html',{'title':"Add new request ","active1":"active",'page':"R",'post_type':"request"})

@login_required(login_url='user:login')
def newDonation(request):
    if request.method == 'POST':
        newpost = Post.create_donation(request)
        
        messages.success(request, 'Your donation was successfuly submited ')
        return redirect('user:detail',slug_title=newpost.slug_title,post_id=newpost.id)
       
        
    return render(request, 'newPost.html',{'title':"Add new donation","active2":"active",'page':"D",'post_type':"donation"})

@login_required(login_url='user:login')
def post_detail(request,slug_title,post_id):
    try :
        post = get_object_or_404(Post, pk=post_id)
    except :
        return render(request,'error.html')
    if request.method == 'POST':
        if Notification.objects.filter(post=post,sender=request.user,receiver=post.author).exists():
            print("*************************\n")
            print(Notification.objects.filter(post=post,sender=request.user,receiver=post.author))
            print("*************************\n")
            messages.success(request,'your request already submitted')
        else:
            new_notif =Notification(
                                    post=post,
                                    sender=request.user,
                                    receiver =post.author,
                                    status="no",
                                    type = post.post_type,
                                    )
            new_notif.save()
            messages.success(request,f'{post.author} received a msg , and may contact you sooner ')
            # return redirect('/requests/detail/{}-id={}/'.format(post.slug_title,post.id))

    
    context={
        'post':post,
        'title':'Details',
    }
    return render(request,'postDetail.html',context)
    
@login_required(login_url='user:login')
def delete_post(request,post_id):
    try:
        post_todelete = Post.objects.get(pk=post_id)
        if request.method =='POST':
            post_todelete.delete()
            messages.success(request,"your post is deleted")
            return redirect('user:privatePosts')

        context={
            'post':post_todelete,
            'title':'Delete post',
        }
        return render(request,'confirm_delete_post.html',context)
   
    except Post.DoesNotExist:
        return render(request,'error.html')
        

@login_required(login_url='user:login')   
def update_post(request,post_id):
    post_to_update = get_object_or_404(Post, pk=post_id)
    if request.method =='POST':
        post_to_update.title=request.POST['object']
        post_to_update.content=request.POST['content']
        post_to_update.current_place=request.POST['c_place']
        try :
            if request.FILES['image'] :
                post_to_update.image = request.FILES['image'] 
        except:
            pass
        post_to_update.save()
        messages.success(request,'your post was updated succesfuly ')
        return redirect('user:detail',slug_title=post_to_update.slug_title,post_id=post_to_update.id )

        #return redirect(f'/requests/detail/{post_to_update.id}/')

    context={
        'post':post_to_update,
        'title':'Update post',
    }
    return render(request,'updatePost.html',context)


@login_required(login_url='user:login')
def search(request,choice,title,c_place): ###
    dict = {"requests":"R","donations":"D"}
    postType = dict[choice]
    if c_place=='all':
        posts = Post.objects.filter(title__contains=title , post_type=postType ,show_post="yes" )
    else :    
        posts = Post.objects.filter(title__contains=title , post_type=postType , show_post="yes" ,current_place__contains=c_place)  ###############################
    return render(request,'search.html',{'posts':posts,'postType':choice})
# def search(request,choice,title):
#     dict = {"requests":"R","donations":"D"}
#     postType = dict[choice]
#     posts = Post.objects.filter(title__contains=title , post_type=postType)
#     return render(request,'search.html',{'posts':posts,'postType':choice})

#===== notifications =====#

@login_required(login_url='user:login')
def nots(request):
    nots_not_seen = len(Notification.objects.filter(receiver=request.user,status="no"))
    print("*** number of new notifs :",nots_not_seen)
    return JsonResponse({'nb_nots':nots_not_seen})

@login_required(login_url='user:login')
def notifications(request):
    notifications = Notification.objects.filter(receiver=request.user)
    notifications1 = Notification.objects.filter(receiver=request.user ,post__post_type="R")
    notifications2 = Notification.objects.filter(receiver=request.user,post__post_type="D")

    for notif in notifications :
        notif.status="yes"
        notif.save()
    context={
        'notifications':notifications,
        'title':"Notifications",
    }
    return render(request,'notifications.html',context)

@login_required(login_url='user:login')
def notif_detail(request,notif_id):
    notif = get_object_or_404(Notification,pk=notif_id)
    context={
        'notif':notif,
        'title':'Notifications',
    }
    return render(request,'notif_detail.html',context)

#===== Profile =====#

@login_required(login_url='user:login')
def privatePosts(request):

    requestsList= Post.objects.filter(author=request.user,post_type='R')
    donationsList = Post.objects.filter(author=request.user,post_type='D').reverse()
    
    page = request.GET.get('page1', 1)
    paginator = Paginator(donationsList,5)
    try:
        donations = paginator.page(page)
    except PageNotAnInteger:
        donations = paginator.page(1)
    except EmptyPage:
        donations = paginator.page(paginator.num_pages)
    
    page = request.GET.get('page2', 1)
    paginator = Paginator(requestsList, 5)
    try:
        requests = paginator.page(page)
    except PageNotAnInteger:
        requests = paginator.page(1)
    except EmptyPage:
        requests = paginator.page(paginator.num_pages)
        
    nots_not_seen = len(Notification.objects.filter(receiver=request.user,status="no"))
    context={
        'requests':requests,
        'donations':donations,
        'nb_nots':nots_not_seen,
        'title':f'MedicaShare | {request.user}',
        'fullname':f'{request.user.first_name}-{request.user.last_name}'
    }


    context={
            'title':'My posts',
            'requests':requests,
            'donations':donations,
            }
    return render(request,'privatePosts.html',context)


@login_required(login_url='user:login')
def update_profile(request,username):
    profil = get_object_or_404(User,username=username)
    if request.method == 'POST':
            user_form = UserUpdateForm(request.POST, instance=request.user)
            profile_form = ProfileUpdateForm(
                request.POST, request.FILES, instance=request.user.profile)
            if user_form.is_valid and profile_form.is_valid:
                if not (request.POST['phone_number'].isdigit()):
                    messages.warning(request, 'invalid phone number !')
                    
                else :
                    try:
                    
                        profil.profile.phone_number = request.POST['phone_number']   
                        user_form.save()
                        profile_form.save()
                        messages.success(request, 'update success !')
                    except:
                        pass
                        #messages.warning(request, 'something went wrong ! ,try again ')
                
                
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context={
        'title':'update profile ',
        'profil':profil,
        'user_form': user_form,
        'profile_form': profile_form,
    } 
    return render(request,'updateProfile.html',context)

def historique(request):
    requestHist = Post.objects.filter(author=request.user,isReceived ="yes").reverse()
    donationHist = Post.objects.filter(author=request.user,isDonated ="yes").reverse()
    
    # requestHist = Post.objects.filter(post_type="R",author=request.user,isReceived ="yes")
    
    return render(request,'historique.html',{'Rposts':requestHist,'Dposts':donationHist,})
#
# postToModify = Post.objects.get(id=id)
#     postToModify.isDonated = "yes"
#     postToModify.save()
def saveToHistorics(request,id):
    postToSave = Post.objects.get(id=id)
    if (postToSave.post_type == "R"):
        postToSave.show_post = "no"
        postToSave.isReceived = "yes"
        postToSave.save()
    elif (postToSave.post_type=="D"):
        postToSave.show_post = "no"
        postToSave.isDonated = "yes"
        postToSave.save()
    return redirect('user:historics')

'''def test(request):
    if request.method=='POST':
        subject, from_email, to = 'hello', settings.EMAIL_HOST_USER,request.POST['email']
        user = 'Hamdi HASSEN'
        text_content = 'This is an important message.'
        html_content = f'<b> <span style="color:blue;">Bonjour{user}</span> </b> <p> This is an <strong>important</strong> message.</p>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
   
    return render(request,'test.html')'''
