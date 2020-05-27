from django.urls import path

from .views import *

urlpatterns = [
    path('', SurveyList.as_view(), name='surveys_list_url'),
    path('result/<int:id>', SurveyResult.as_view(), name='survey_result_url'),
    path('create/', SurveyCreate.as_view(), name='survey_create_url'),
    path('add/<int:id>', SurveyAdd.as_view(), name='survey_add_url'),
    path('update/<int:id>', SurveyUpdate.as_view(), name='survey_update_url'),
    path('delete/<int:id>', SurveyDelete.as_view(), name='survey_delete_url'),
]