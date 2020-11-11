from django.urls import path


from user import views

app_name = 'user'

urlpatterns = [
    path('register/',views.register,name='register'),
    path('regist_verify/',views.regist_verify,name='regist_verify'),
    path('login/',views.login,name='login'),
    path('login_verify/',views.login_verify,name='login_verify'),
    path('pd_name/',views.pd_name,name='pd_name'),
    path('get_captcha/',views.get_captcha,name='get_captcha'),
    path('email/',views.email,name='email'),
    path('active/',views.active,name='active'),
    path('forget/',views.forget,name='forget'),
    path('forget_verify/',views.forget_verify,name='forget_verify'),
    path('reset_pwd/',views.reset_pwd,name='reset_pwd'),
    path('quit/',views.quit,name='quit'),
    path('quite/',views.quit,name='quite'),

]