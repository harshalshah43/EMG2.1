from django.urls import path
from .import views

urlpatterns=[
    path('table/',views.enquiry_table,name = 'enquiry-table'),
    path('new-enquiry-create/',views.enquiry_create_form,name ='enquiry-form'),
    path('enquiry-detail/<int:id>/',views.enquiry_detail,name = 'enquiry-detail'),
    path('enquiry-quotation/<int:id>/',views.enquiry_to_quotation,name = 'get-quotation'),
    path('enquiry-update/<int:id>/',views.enquiry_update,name = 'enquiry-update'),
    path('enquiries-by-party/<int:id>/',views.enquiry_by_party,name = 'enquiry-by-party'),
    path('enquiries-by-item-code/<int:id>/',views.enquiry_by_item_code,name = 'enquiry-by-item-code'),
    path('enquiry-delete/<int:id>/',views.enquiry_delete,name = 'enquiry-delete'),
    path('enquiry-search-result/',views.enquiry_search,name = 'enquiry-search'),
    # path('quotation-create/<int:id>/',views.create_quotation,name = 'create-quotation')
    path('parties/',views.parties_report,name = 'parties-report'),
    path('product/',views.product_report,name = 'product-report'),
    path('change-status-all/',views.change_status_all,name = 'change-status-all'),
    path('import/',views.import_data,name = 'import-data'),
    path('unquoted-enquiries/',views.enquiries_unquoted,name = 'unquoted-enquiries'),
    

    path('temp/',views.temp,name = 'temp')
    
]