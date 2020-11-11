from django.urls import path


from courseapp import views

app_name = 'courseapp'

urlpatterns = [
    path('home/',views.home,name='home'),
    path('home1/',views.home1,name='home1'),
    path('course_add/',views.course_add,name='course_add'),
    path('course_add1/',views.course_add1,name='course_add1'),
    path('course_add_title/',views.course_add_title,name='course_add_title'),
    path('addAritcle/',views.addAritcle,name='addAritcle'),
    path('addAritcle_btn/',views.addAritcle_btn,name='addAritcle_btn'),
    path('delete/',views.delete,name='delete'),
    path('update/',views.update,name='update'),
    path('updata_title/',views.updata_title,name='updata_title'),
    path('read_sort/',views.read_sort,name='read_sort'),
    # path('home9/',views.home9,name='home9'),

]