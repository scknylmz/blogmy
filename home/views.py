from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.contrib import messages

from home.models import Contact, Personnel, Blog, Works, WorksCategory
from home.forms import ContactForm

from django.conf import settings
from django.core.mail import send_mail
# Create your views here.

def index(request):
    personnel = Personnel.objects.get(id=1)
    contact = Contact.objects.get(name=personnel.id)
    
    categories = WorksCategory.objects.all()
    works = Works.objects.all().order_by('publish_date')
    blogs = Blog.objects.all()

    paginator_works = Paginator(works, 2)
    page_number_works = request.GET.get('page',1)
    page_obj_works = paginator_works.get_page(page_number_works)

    paginator_blogs = Paginator(blogs, 2)
    page_number_blogs = request.GET.get('page',1)
    page_obj_blogs = paginator_blogs.get_page(page_number_blogs)

    forms = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']

            msg = f'{name} with email {from_email} said:'
            msg += f'\n"{subject}"\n\n'
            msg += form.cleaned_data['message']
            send_mail(
                subject=subject,
                message=msg,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.RECIPIENT_ADDRESS]
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('home:index')
        else:
            messages.warning(request, 'Please correct the error below.')

    if request.session.has_key('_my_data'):
        del request.session['_my_data']
    if request.method=="POST":
        request.session['_my_data'] = request.POST

    context = {
        "personnel" : personnel,
        "contact" : contact,
        "works" : works,
        "blogs" : blogs,
        "categories" : categories,
        "page_obj_blogs" : page_obj_blogs,
        "page_obj_works" : page_obj_works,
        "forms" : forms,
    }
            
    if request.htmx.target == "recent_works_load_more":
        return render(request, 'partials/htmx/recent-works-list.html', context)
    if request.htmx.target == "recent_blogs_load_more":
        return render(request, 'partials/htmx/recent-blog-list.html', context)

    return render(request, 'index.html', context)
    
def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    context = {
        "blog" : blog,
    }
    return render(request,"blog_detail.html", context)

def works_list(request, category):
    
    query_work_list = Works.objects.filter(category_id__category=category).order_by("publish_date")
    paginator = Paginator(query_work_list, 2)
    page_number = request.GET.get('page',2)
    page_obj_works_list = paginator.get_page(page_number)
    context = {
        "page_obj_works_list" : page_obj_works_list,
        "category" : category,
    }
    return render(request, 'partials/htmx/works-list.html', context)

def check_name(request):
    form = ContactForm(request.GET)
    if form.is_valid():
        valid = True
    else:
        valid = False

    try:
        error = form.errors['name']
    except KeyError:
        error = "No Error"
 
    context = {
        'form' : error,
        'valid' : valid
    }
    return render(request, 'partials/field.html', context)

def check_email(request):
    form = ContactForm(request.GET)
    if form.is_valid():
        valid = True
    else:
        valid = False

    try:
        error = form.errors['email']
    except KeyError:
        error = "No Error"
    
    context = {
        'form' : error,
        'valid' : valid
    }
    return render(request, 'partials/field.html', context)

def check_subject(request):
    form = ContactForm(request.GET)
    if form.is_valid():
        valid = True
    else:
        valid = False

    try:
        error = form.errors['subject']
    except KeyError:
        error = "No Error"
    
    context = {
        'form' : error,
        'valid' : valid
    }
    return render(request, 'partials/field.html', context)