from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# ensure that the user is logged in if they are not.
@login_required(login_url='/signin')
# Create your views here.
def index(request):
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user = user_object)
   
    
    posts = Post.objects.all()
    
    context = {
        'user_profile': user_profile,
        'posts': posts
    }
    return render(request, 'index.html', context)

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            if User.objects.filter(email = email).exists():
                messages.info(request, "Email already exist. Please log in or use another email.")
                return redirect('/signup')
            elif User.objects.filter(username= username).exists():
                messages.info(request, "Username has already been taken.")
                return redirect('/signup')
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                user.save()
                messages.success(request, "User created successfully.")
                
                # log in user and redirect to the settings page.
                user_login = auth.authenticate(username = username, password = password)
                auth.login(request, user_login)
                
                # create new profile object
                user_model = User.objects.get(username = username)
                new_profile =  Profile.objects.create(user = user_model, id_user = user_model.id)
                new_profile.save()              
                return redirect('/settings')                      
        else: 
            messages.info(request, "Passwords do not match")           
            return redirect('/signup')
    else:
        return render(request, 'signup.html')

def signin(request): 
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password = password)
        if user is not None:
            auth.login(request, user)
            return  redirect('/')
        else: 
            messages.info(request, "Invalid username or password.")
            return redirect(  '/signin')
            
    else:
        return render(request, 'signin.html')
    
# handle user logout. 
@login_required(login_url='/signin')
def logout(request):
    auth.logout(request)
    return redirect('/signin')

@login_required(login_url='/signin')
def settings(request): 
    user_profile = Profile.objects.get(user = request.user)
    context = {
        'user_profile': user_profile
    }
    
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            """if theres no image being sent. """
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']
            
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        else:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']
            
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        return redirect('/settings')
    return render(request, 'settings.html', context)

# hanle uploading of posts.
@login_required(login_url='/signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        
        new_post = Post.objects.create(user=user, image=image, caption = caption)
        if new_post.save():
            messages.success(request, "Post uploaded successfully.")
        else:
            messages.info(request, "Error uploading you post. Please try again later.")
        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='/signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    
    post = Post.objects.get(id=post_id)
    
    # check if the user had liked the post before
    like_filter = LikePost.objects.filter(post_id=post_id, username= username).first()
    if like_filter ==  None:   
        # user has not liked the post.
        new_like = LikePost.objects.create(post_id=post_id, username = username)
        new_like.save()
        post.no_of_likes += 1
        post.save()
        return redirect('/')   
    else:
       # user had already liked the post before.
        like_filter.delete()
        post.no_of_likes -=1
        post.save()
        return redirect('/')

@login_required(login_url='/signin')
def profile(request, pk):
    user_object = User.objects.get(username = pk)
    user_profile = Profile.objects.get(user = user_object)
    
    user_posts = Post.objects.filter(user = pk)
    no_of_posts = len(user_posts)
    
    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'no_of_posts': no_of_posts    
    }
    return render(request, 'profile.html', context)
    