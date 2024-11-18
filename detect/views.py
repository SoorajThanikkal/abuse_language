from django.shortcuts import render,redirect,HttpResponse
from .models import *
from profanity_check import predict, predict_prob
import instaloader
# Create your views here.


def index(request):
    return render(request, 'index.html')

def home(request):
    if 'user_id' in request.session:
        try:
            userid= request.session['user_id']
            user = UserReg.objects.get(id=userid)
            print('User')
            if BlockedUsers.objects.filter(user=user,blocked_status=True).exists():
                print( "User blocked")
                alert="<script>alert('You are not allowed to this page because you are blocked'); window.location.href='/index/';</script>"
                return HttpResponse(alert)
        except Exception as e:
            print(e)
            alert="<script>alert('unexpected error occured'); window.location.href='/index/';</script>"
            return HttpResponse(alert)
    return render(request, 'home.html')

def userReg(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        if UserReg.objects.filter(email=email).exists():
            alert = "<script>alert('Email already exists');window.location.href='/user_reg/';</script>"
            return HttpResponse(alert)
        if UserReg.objects.filter(name=name).exists():
            alert = "<script>alert('Username already taken');window.location.href='/user_reg/';</script>"
            return HttpResponse(alert)
        try:
            user = UserReg(name=name, email=email, password=password, phone_number=phone)
            user.save()
            return redirect('user_login')
        except Exception as e:
            alert = "<script>alert('Error while registering user');window.location.href='/user_reg/';</script>"
            print(e)
            return HttpResponse(alert)
    return render(request, 'user_reg.html')

def userLogin(request):
    if request.method == 'POST':
        email= request.POST.get('email')
        password= request.POST.get('password')
        try:
            user = UserReg.objects.get(email=email, password=password)
            if user:
                request.session['user_id'] = user.id
                return redirect('home')
            else:
                alert="<script>alert('Invalid email or password');window.location.href='/user_login/';</script>"
                return HttpResponse(alert)
        except UserReg.DoesNotExist:
            alert="<script>alert('Invalid email or password');window.location.href='/user_login/';</script>"
            return HttpResponse(alert)
        except Exception as e:
            alert="<script>alert('Error while login user');window.location.href='/user_login/';</script>"
            return HttpResponse(alert)
    return render(request, 'user_login.html')

def viewProfile(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        try:
            user = UserReg.objects.get(id=user_id)
        except:
            return redirect('user_login')
        return render(request, 'view_profile.html', {'user': user})
    else:
        return redirect('user_login')
    
    
def editProfile(request, user_id):
    if 'user_id' in request.session:
        try:
            user = UserReg.objects.get(id=user_id)
        except UserReg.DoesNotExist:
            return redirect('user_login')
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            if UserReg.objects.filter(email=email).exclude(id=user_id).exists():
                alert = "Email already exists for another user."
                return render(request, 'edit_profile.html', {'alert': alert, 'user': user})
            if UserReg.objects.filter(name=name).exclude(id=user_id).exists():
                alert = "Username already exists for another user."
                return render(request, 'edit_profile.html', {'alert': alert, 'user': user})
            user.name = name
            user.email = email
            user.phone_number = phone
            user.save()
            return redirect('view_profile')
        return render(request, 'edit_profile.html', {'user': user})
    else:
        return redirect('user_login')
            
def deleteAccount(request,user_id):
    if 'user_id' in request.session:
        try:
            user = UserReg.objects.get(id=user_id)
        except UserReg.DoesNotExist:
            return redirect('user_login')
        user.delete()
        del request.session['user_id']
        return redirect('user_login')
    else:
        return redirect('user_login')
    
def createPost(request):
    user_id=request.session['user_id']
    if user_id:
        user_dtls=UserReg.objects.get(id=user_id)
        if request.method == "POST":
            post_pic= request.FILES.get('post_pic')
            description = request.POST.get('description')
            try:
                chk= predict([description])
                print("Success",chk)
                if chk==1:
                    blocked_user, created = BlockedUsers.objects.get_or_create(
                        user=user_dtls,
                        defaults={'blocked_status': True}
                    )
                    if not created: 
                        blocked_user.blocked_status = True  
                        blocked_user.save()
                    alert="<script>alert('Abusive language detected. Post will not be saved.and you got banned temporarly');window.location.href='/home/';</script>"
                    return HttpResponse(alert)
            except :
                pass
            like_count=0
            PostModel(user=user_dtls,post_pic=post_pic,description=description,likes_count=like_count).save()
            return redirect('home')
        else:
            return render(request,'addpost.html')
    else:
        return redirect('user_login')
    
def displayPosts(request):
    posts = PostModel.objects.all()
    try:
        user_id = request.session['user_id']
    except:
        return redirect('user_login')
    
    if user_id:
        user = UserReg.objects.get(id=user_id)
        liked_posts = user.liked_posts.all()
        post_comments = {}
        for post in posts:
            comments = CommentSectionModel.objects.filter(post=post)  
            post.comment_count = comments.count()
    else:
        liked_posts = []
    
    return render(request, 'viewallposts.html', {'posts': posts, 'liked_posts': liked_posts,'us': user})

def likePost(request, post_id):
    post = PostModel.objects.get(id=post_id)
    user_id = request.session.get('user_id')
    user = UserReg.objects.get(id=user_id)

    if post.liked_users.filter(id=user_id).exists():
        post.liked_users.remove(user)
        post.likes_count = max(0, post.likes_count - 1)
    else:
        post.liked_users.add(user)
        post.likes_count += 1

    post.save()
    return redirect('display_posts')

def addComment(request, post_id):
    if request.method == 'POST':
        try:
            post = PostModel.objects.get(id=post_id)
            comment_text = request.POST.get('comment')
            user_id = request.session.get('user_id')
            user = UserReg.objects.get(id=user_id)
            try:
                st=predict([comment_text])
                if st==1:
                    blocked_user, created = BlockedUsers.objects.get_or_create(
                        user=user,
                        defaults={'blocked_status': True}
                    )
                    if not created: 
                        blocked_user.blocked_status = True  
                        blocked_user.save()
                    alert="<script>alert('This comment contains offensive language. You have been temporarily banned.');window.location.href='/index/';</script>"
                    return HttpResponse(alert)
            except Exception as e:
                print(e)
                pass
                
        except Exception as e:
            print(e)
            alert="<script>alert('unexpected error occured'); window.location.href='/display_posts/';</script>"
            return HttpResponse(alert)
        
        if comment_text:
            CommentSectionModel.objects.create(
                user=user, 
                post=post, 
                comment=comment_text
            )
    return redirect('display_posts')

def commentsDelete(request, cmt_id):
    try:
        comment = CommentSectionModel.objects.get(id=cmt_id)
        user_id= request.session['user_id']
        user=UserReg.objects.get(id=user_id)
        print(user)
    except Exception as e:
        print(e)
        alert="<script>alert('unexpected error occured'); window.location.href='/display_posts/';</script>"
        return HttpResponse(alert)
    if user == comment.user:
        comment.delete()
        return redirect('display_posts')
    else:
        return HttpResponse("You are not allowed to delete this comment.")
    
def check_insta_captions(request):
    if request.method == "POST":
        login_username = request.POST.get('username')  # Instagram login username
        password = request.POST.get('password')
        target_username = request.POST.get('target_username', login_username)  # Profile to fetch; defaults to login username
        try:
            # Initialize Instaloader
            loader = instaloader.Instaloader()
            loader.login(login_username, password)

            # Fetch the profile of the specified user
            profile = instaloader.Profile.from_username(loader.context, target_username)
            captions = []
            abusive_captions = []
            abuse_scores = []

            # Fetch the most recent posts and analyze captions
            for post in profile.get_posts():
                if post.caption:
                    captions.append(post.caption)

                    # Analyze the caption for abuse
                    abuse_score = predict_prob([post.caption])[0]
                    abuse_scores.append(abuse_score)
                    if predict([post.caption])[0] == 1:
                        abusive_captions.append(post.caption)

            # Prepare the context for the template
            context = {
                'captions': zip(captions, abuse_scores),
                'abusive_captions': abusive_captions,
                'username': target_username,
            }
            return render(request, 'insta_captions.html', context)

        except instaloader.exceptions.LoginRequiredException:
            return HttpResponse(
                "<script>alert('Login required. Please check your credentials.');"
                "window.history.back();</script>"
            )
        except instaloader.exceptions.ProfileNotExistsException:
            return HttpResponse(
                "<script>alert('Profile not found. Please enter a valid username.');"
                "window.history.back();</script>"
            )
        except Exception as e:
            print(f"Error: {e}")  # Debugging: Log error to console
            return HttpResponse(
                f"<script>alert('An unexpected error occurred: {e}');"
                "window.history.back();</script>"
            )

    return render(request, 'insta_captions.html')

def adminLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        uname= 'admin'
        passwd= 'admin'
        if username == uname and password == passwd:
            request.session['admin'] = uname
            
            return redirect('admin_dashboard')
        else:
            alert="<script>alert('Invalid username or password'); window.location.href='/admin_login/';</script>"
            return HttpResponse(alert)
    return render(request, 'admin_login.html')

def admDashboard(request):
    if 'admin' not in request.session:
        return redirect('admin_login')
    return render(request, 'admin_dashboard.html')

def adviewUsers(request):
    if 'admin' in request.session:
        us=UserReg.objects.all()
        return render(request, 'adminuserlist.html', {'users': us})
    return redirect('admin_login')
        
def adeditUsers(request,id):
    if 'admin' in request.session:
        try:
            user = UserReg.objects.get(id=id)
        except UserReg.DoesNotExist:
            return redirect('admin_login')
        
        if request.method == 'POST':
            user.name = request.POST.get('username')
            user.email = request.POST.get('email')
            user.phone_number = request.POST.get('phone_number')
            pro_pic = request.FILES.get('pro_pic')
            if pro_pic:
                user.pro_pic = pro_pic
            user.save()
            return redirect('adviewUsers')
        else:
            return render(request, 'adminuseredit.html', {'user': user})
    return redirect('admin_login')

def addeleteUsers(request,id):
    if 'admin' in request.session:
        try:
            user=UserReg.objects.get(id=id)
        except:
            return redirect('admin_login')
        
        user.delete()
    return redirect('admin_login')

def adviewbannedUsers(request):
    if 'admin' in request.session:
        user=BlockedUsers.objects.filter(blocked_status=True)
        return render(request,'adviewbannedusers.html',{'user':user})
    else:
        return redirect('admin_login')
        
    