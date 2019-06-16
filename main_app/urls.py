from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('about/', views.about, name='about'),
	path('cars/', views.cars_index, name='index'),
	path('cars/<int:car_id>/', views.cars_detail, name='detail'),
	path('cars/<int:car_id>/add_service/', views.add_service, name='add_service'),
	path('cars/<int:car_id>/add_photo/', views.add_photo, name='add_photo'),
	path('cars/<int:car_id>/assoc_accessory/<int:accessory_id>/', views.assoc_accessory, name='assoc_accessory'),
	path('cars/<int:car_id>/remove_accessory/<int:accessory_id>/', views.remove_accessory, name='remove_accessory'),
	path('cars/create/', views.CarCreate.as_view(), name='cars_create'),
	path('cars/<int:pk>/update/', views.CarUpdate.as_view(), name='cars_update'),
	path('cars/<int:pk>/delete/', views.CarDelete.as_view(), name='cars_delete'),
	path('accessories/', views.AccessoryList.as_view(), name='accessories_index'),
  	path('accessories/<int:pk>/', views.AccessoryDetail.as_view(), name='accessories_detail'),
  	path('accessories/create/', views.AccessoryCreate.as_view(), name='accessories_create'),
 	path('accessories/<int:pk>/update/', views.AccessoryUpdate.as_view(), name='accessories_update'),
  	path('accessories/<int:pk>/delete/', views.AccessoryDelete.as_view(), name='accessories_delete'),
  	path('accounts/', include('django.contrib.auth.urls')),
  	path('accounts/signup', views.signup, name='signup'),
]

# Do NOT need to factor in route parameter conflict
# NOTE: Changing 'name' attribute will impact rest of code
# CBVs require int:pk route parameter
# Do NOT need to import django.contrib
# If desired, can put 'accounts/' in outermost urls.py