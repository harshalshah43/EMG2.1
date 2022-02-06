from cv2 import log
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from .models import Quotation
from enquiry.models import Enquiry
from .forms import QuotationCreateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def create_quote(request,id):
    eid = id
    current_enq = Enquiry.objects.filter(id = eid).first()
    if request.method == 'POST':
        q_form = QuotationCreateForm(request.POST,request.FILES)
        q_form.instance.enquiry = current_enq
        
        if q_form.is_valid():
            q_form.save()
            current_enq.status = 'Quoted'
            current_enq.save()
            # return redirect('enquiry-by-party',id = eid)
            return redirect('unquoted-enquiries')
        else:
            messages.success(request,f'Quotation could not be posted')

            context = {
                 'q_form':q_form,
                }
            return render (request,'quotation/quotation_create.html',context)
    q_form = QuotationCreateForm()
    context = {
        'q_form':q_form,
        'party':current_enq.party,
        'item':current_enq.item_code,
        'qty':current_enq.qty
    }
    return render(request,'quotation/quotation_create.html',context)

@login_required
def quotation_table(request):
    quotations = Quotation.objects.all().order_by('-date_posted')
    context = {
        'quotations':quotations
    }
    return render(request,'quotation/quotation_table.html',context)

@login_required
def delete_quote(request,id):
    qid = id
    current_quotation = Quotation.objects.filter(id = qid).first()
    eid = current_quotation.enquiry.id
    current_enquiry = Enquiry.objects.filter(id = eid).first()
    Quotation.objects.filter(id = qid).delete()
    quotations = Quotation.objects.all()
    context = {
        'quotations':quotations,
    }
    return render(request,'quotation/quotation_table.html',context)

@login_required
def quotation_to_enquiry(request,id):
    qid = id
    print("quotation id",qid)
    current_quotation = Quotation.objects.filter(id = qid).first()
    print(current_quotation)
    current_enquiry = current_quotation.enquiry
    enquiry_list = Enquiry.objects.filter(id = current_enquiry.id)
    context = {
        'enquiry_list':enquiry_list
    }
    return render(request,'enquiry/enquiry_table.html',context)


@login_required
def quotes_for_item(request,id):
    eid = id # enquiry id recieved
    current_enquiry = Enquiry.objects.get(id=eid)
    selected_item = current_enquiry.item_code
    enquiries = Enquiry.objects.filter(item_code = selected_item)

    quotations = []
    for enquiry in enquiries:
        quote = Quotation.objects.filter(enquiry = enquiry).first()
        quotations.append(quote)
    quotations = [i for i in quotations if i]
    context = {
        'title':'for item '+current_enquiry.item_code,
        'quotations':quotations
    }
    return render(request,'quotation/quotation_table.html',context)

@login_required
def quotes_for_party(request,id):
    eid = id # enquiry id recieved
    print(eid)
    current_enquiry = Enquiry.objects.get(id=eid)
    selected_party = current_enquiry.party
    enquiries = Enquiry.objects.filter(party = selected_party).order_by('-date_posted')
    quotations = []
    for enquiry in enquiries:
        quote = Quotation.objects.filter(enquiry = enquiry).first()
        quotations.append(quote)
    quotations = [i for i in quotations if i]
    context = {
        'quotations':quotations
    }
    return render(request,'quotation/quotation_table.html',context)

@login_required
def quotation_search(request):
    context = {
        }
    if request.method == 'GET':
        query1 = request.GET.get("q1")
        query2 = request.GET.get("q2")
        query3 = request.GET.get("q3")
        # query3 = int(query3)
        qs = Quotation.objects.all()
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
            return render(request,'quotation/quotationsearch_table.html',context)
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
            return render(request,'quotation/quotationsearch_table.html',context)
        if query3 and query3.isdigit(): 
            qs3 = qs.filter(date_posted__month = query3)
            context = {
                'enquiry_list':qs3,
                'title':'search results for '+query3 
            }
            return render(request,'quotation/quotationsearch_table.html',context)
        return render(request,'quotation/quotationsearch_form.html',context)