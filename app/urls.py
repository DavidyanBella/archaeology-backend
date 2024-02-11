from django.urls import path

from .views import *

urlpatterns = [
    # Набор методов для услуг
    path('api/places/search/', search_place),  # GET
    path('api/places/<int:place_id>/', get_place_by_id),  # GET
    path('api/places/<int:place_id>/update/', update_place),  # PUT
    path('api/places/<int:place_id>/delete/', delete_place),  # DELETE
    path('api/places/create/', create_place),  # POST
    path('api/places/<int:place_id>/add_to_find/', add_place_to_find),  # POST
    path('api/places/<int:place_id>/image/', get_place_image),  # GET
    path('api/places/<int:place_id>/update_image/', update_place_image),  # PUT

    # Набор методов для заявок
    path('api/finds/', get_finds),  # GET
    path('api/finds/<int:find_id>/', get_find_by_id),  # GET
    path('api/finds/<int:find_id>/update/', update_find),  # PUT
    path('api/finds/<int:find_id>/update_status_user/', update_status_user),  # PUT
    path('api/finds/<int:find_id>/update_status_admin/', update_status_admin),  # PUT
    path('api/finds/<int:find_id>/delete/', delete_find),  # DELETE
    path('api/finds/<int:find_id>/delete_place/<int:place_id>/', delete_place_from_find),  # DELETE
]