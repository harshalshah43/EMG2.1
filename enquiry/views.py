from django.shortcuts import render,redirect
from sympy import re
from .models import Enquiry
from quotation.models import Quotation
from .forms import EnquiryCreateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.http import HttpResponseRedirect

@login_required
def enquiry_table(request):
    enquiries = Enquiry.objects.all().order_by('-date_posted')
    # print(type(enquiries.first().date_posted.month))
    page = request.GET.get('page',1)
    paginator = Paginator(enquiries,40)
    try:
        enquiries = paginator.page(page)
    except PageNotAnInteger:
        enquiries = paginator.page(1)
    except EmptyPage:
        enquiries = paginator.page(paginator.num_pages)
    context = {
            'enquiry_list':enquiries
        }
    return render(request,'enquiry/enquiry_table.html',context)


def enquiry_search(request):
    context = {
        }
    if request.method == 'GET':
        query1 = request.GET.get("q1")
        query2 = request.GET.get("q2")
        query3 = request.GET.get("q3")
        # query3 = int(query3)
        qs = Enquiry.objects.all()
        if query1:
            print("breakpoint1")
            qs1 = qs.filter(party__icontains = query1)
            if query2:
                qs2 = qs.filter(item_code__icontains = query2)
                qs1 = qs1.intersection(qs2)
                if query3 and query3.isdigit():
                    qs3 = qs.filter(date_posted__month = query3)
                    qs1 = qs1.intersection(qs3)
            elif query3:
                qs3 = qs.filter(date_posted__month = query3)
                qs1 = qs1.intersection(qs3)
            context = {
                'enquiry_list':qs1,
                'title':'search results for '+query1 + query2
            }
            return render(request,'enquiry/enquirysearch_table.html',context)
        if query2:
            print("breakpoint2")
            qs2 = qs.filter(item_code__icontains = query2)
            if query3 and query3.isdigit():
                qs3 = qs.filter(date_posted__month = query3)
                qs2 = qs2.intersection(qs3)
            print(qs2)
            context = {
                'enquiry_list':qs2,
                'title':'search results for '+query1 + query2
            }
            return render(request,'enquiry/enquirysearch_table.html',context)
        if query3 and query3.isdigit(): 
            qs3 = qs.filter(date_posted__month = query3)
            context = {
                'enquiry_list':qs3,
                'title':'search results for '+query3 
            }
            return render(request,'enquiry/enquirysearch_table.html',context)
        return render(request,'enquiry/enquirysearch_form.html',context)

@login_required
def enquiry_create_form(request):
    if request.method == 'POST':
        c_form = EnquiryCreateForm(request.POST,request.FILES)
        context = {
        'form':c_form
        }
        if c_form.is_valid():
            c_form.save()
            enquiry = Enquiry.objects.last()
            return redirect("quotation-create",id = enquiry.id)
        else:
            messages.success(request,f'Enquiry could not be posted')
            context = {
                    'operation':'Create New ',
                    'form':c_form
                }
            return render (request,'enquiry/enquiry_create_form.html',context)
    c_form = EnquiryCreateForm()
    context = {
        'operation':'Create New ',
        'form':c_form,
    }
    return render (request,'enquiry/enquiry_create_form.html',context)

@login_required
def enquiry_detail(request,id):
    eid =id
    current_enquiry = Enquiry.objects.filter(id=eid).first()
    quotations = Quotation.objects.filter(enquiry = current_enquiry)
    context = {
        'quotations':quotations,
        'enquiry':current_enquiry
    }
    return render (request,'enquiry/enquiry_detail.html',context)
@login_required
def enquiry_to_quotation(request,id):
    eid = id
    current_enquiry = Enquiry.objects.filter(id = eid).first()
    quotations = Quotation.objects.filter(enquiry = id)
    return render(request,'quotation/quotation_table.html',{'quotations':quotations})

def enquiry_delete(request,id):
    eid = id
    current_enquiry = Enquiry.objects.filter(id = eid).first()
    current_party = current_enquiry.party
    Enquiry.objects.filter(id=eid).delete()
    context = {
        'enquiry_list':Enquiry.objects.filter(party = current_party)
    }
    return render(request,'enquiry/enquiry_table.html',context)

@login_required
def enquiry_update(request,id):
    eid = id
    current_enquiry = Enquiry.objects.filter(id = eid).first()
    print(current_enquiry)
    # print(current_enquiry.first())

    if request.method == 'POST':
        u_form = EnquiryCreateForm(request.POST,request.FILES,instance = current_enquiry)
        
        if u_form.is_valid:
            u_form.save()
            quotations = Quotation.objects.filter(enquiry = current_enquiry)
            context = {
                'quotations':quotations,
                'enquiry':current_enquiry
            }
            return render(request,'enquiry/enquiry_detail.html',context)
   
    else:
        u_form = EnquiryCreateForm(instance=current_enquiry)
        context = {
            'operation':'Update ',
            'form':u_form
        }
        return render(request,'enquiry/enquiry_create_form.html',context)

@login_required
def enquiry_by_party(request,id):
    eid =id
    current_enquiry_party = Enquiry.objects.get(id = eid).party
    # print(current_enquiry_party)
    enquiriesfortheparty = Enquiry.objects.filter(party = current_enquiry_party).order_by('-date_posted')
    print(current_enquiry_party)
    context = {
        'title':'for '+current_enquiry_party,
        'enquiry_list':enquiriesfortheparty
    }
    return render(request,'enquiry/enquiry_table.html',context)
    
@login_required
def enquiry_by_item_code(request,id):
    eid =id
    current_enquiry_item_code = Enquiry.objects.get(id = eid).item_code
    # print(current_enquiry_party)
    enquiriesfortheitemcode = Enquiry.objects.filter(item_code = current_enquiry_item_code).order_by('-date_posted')
    context = {
        'enquiry_list':enquiriesfortheitemcode
    }
    return render(request,'enquiry/enquiry_table.html',context)

@login_required
def enquiries_unquoted(request):
    enquiries = Enquiry.objects.filter(status = 'Open').order_by('-date_posted')
    page = request.GET.get('page',1)
    paginator = Paginator(enquiries,40)
    try:
        enquiries = paginator.page(page)
    except PageNotAnInteger:
        enquiries = paginator.page(1)
    except EmptyPage:
        enquiries = paginator.page(paginator.num_pages)
    context = {
        'enquiry_list':enquiries
    }
    return render(request,'enquiry/enquiry_table.html',context)

@login_required
def parties_report(request):
    data = Enquiry.objects.values('party').annotate(count = Count('date_posted')).order_by('-count')
    # data = sorted(data, key = lambda d:d['count'])
    data = list(data)
    data = list(filter(lambda x: x['count'] > 0,data))
    print(data[0])
    return render(request,'enquiry/parties_report.html',{'parties':data})

@login_required
def product_report(request):
    data = Enquiry.objects.values('item_code').annotate(count = Count('date_posted')).order_by('-count')
    # data = sorted(data, key = lambda d:d['count'])
    data = list(data)
    data = list(filter(lambda x: x['count'] > 0,data))
    print(data[0])
    return render(request,'enquiry/product_report.html',{'products':data})

@login_required
def import_data(request):
    import flood as fl
    fl.clean_data('chunk.csv')
    fl.flood("chunk.csv")
    fl.merge("Enquiry_data.csv","chunk.csv")
    recent = Enquiry.objects.all().order_by('-date_posted')[:4]
    context = {
        'enquiry_list':recent
    }
    return render(request,'enquiry/enquiry_table.html',context)


def change_status_all(request):
    enquiries = Enquiry.objects.filter(status = None)
    for enquiry in enquiries:
        enquiry.status = 'Open'
        enquiry.save()
    context = {
        'enquiry_list':enquiries
    }
    return render(request,'enquiry/enquiry_table.html',context)
    

def temp(request):
    return render(request,'enquiry/temp.html',{})
