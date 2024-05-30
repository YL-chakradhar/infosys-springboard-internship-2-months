from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet,CakeViewSet,CakeCustomizationViewSet,CartViewSet,OrderViewSet,StoreViewSet,CustomerViewSet_admin,CakeViewSet_admin,CakeCustomizationViewSet_admin,OrderViewSet_admin

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'user', CustomerViewSet, basename='user')
router.register(r'cakes', CakeViewSet)
router.register(r'cakecustimization',CakeCustomizationViewSet)
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'orders',OrderViewSet,basename='orders')
router.register(r'stores', StoreViewSet)
router.register(r'customer',CustomerViewSet_admin,basename='customer')
router.register(r'cakes_admin', CakeViewSet_admin,basename='cakes_admin')
router.register(r'cakecustimization_admin',CakeCustomizationViewSet_admin,basename='cakecustimization_admin')
router.register(r'orders_admin',OrderViewSet_admin,basename='orders_admin')



# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('cakecustimization/customer/<int:pk>/',CakeCustomizationViewSet.as_view({'get':'get_custom'})),
    

]