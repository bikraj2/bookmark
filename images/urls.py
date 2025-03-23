from django.urls import path

from .views import create_image, image_detail,image_like, image_list, image_ranking
app_name ='images'
urlpatterns = [
    path('create/',view=create_image,name='create'),
    path('detail/<int:id>/<slug:slug>/',
         view = image_detail,
         name = 'detail'
         ),
    path('like/',view=image_like,name='like'),
    path('',view=image_list,name='list'),
    path('ranking/',view=image_ranking,name='ranking'),
]
