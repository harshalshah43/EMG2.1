from django.urls import path
from .import views

urlpatterns=[
    path('quotation-create/<int:id>/',views.create_quote,name = 'quotation-create'),
    path('quotation-table/',views.quotation_table,name = 'quotation-table'),
    path('quotation-delete/<int:id>/',views.delete_quote,name = 'delete-quote'),
    path('quotation-to-enquiry/<int:id>/',views.quotation_to_enquiry,name = 'quote-to-enquiry'),
    path('quotation-for-item/<int:id>/',views.quotes_for_item,name = 'quote-for-item'),
    path('quotation-for-party/<int:id>/',views.quotes_for_party,name = 'quote-for-party'),
    # path('quotation-search-result/',views.quotation_search,name = 'quotation-search'),
]