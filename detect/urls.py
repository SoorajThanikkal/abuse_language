from django.urls import path
from .views import *

urlpatterns=[
    path('',index,name='index'),
    path('index/',index,name='index'),
    path('home/',home,name='home'),
    path('user_reg/',userReg,name='user_reg'),
    path('user_login/',userLogin,name='user_login'),
    path('view_profile/',viewProfile,name='view_profile'),
    path('edit_profile/<int:user_id>/',editProfile,name='edit_profile'),
    path('delete_account/<int:user_id>/',deleteAccount,name='delete_profile'),
    
    path('create_post/',createPost,name='create_post'),
    path('display_posts/',displayPosts,name='display_posts'),
    path('like_post/<int:post_id>/',likePost,name='like_post'),
    path('add_comment/<int:post_id>/',addComment,name='add_comment'),
    path('comments_delete/<int:cmt_id>/',commentsDelete,name='comments_delete'),
    path('checkInsta/',check_insta_captions,name='checkinsta'),
    
    path('admin_login/',adminLogin,name='admin_login'),
    path('adm_dashboard/',admDashboard,name='admin_dashboard'),
    path('ad_viewusers/',adviewUsers,name='ad_viewusers'),
    path('adedit_user/<id>/',adeditUsers,name='adedit_user'),
    path('addelete_user/<id>/',addeleteUsers,name='addelete_user'),
    path('adbanned_user/',adviewbannedUsers,name='adbanned_user'),
]