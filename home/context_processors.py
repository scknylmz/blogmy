from turtle import home


from .models import Personnel

def user_info(request):
    personnel = Personnel.objects.get(id=1)
    return {
        "personnel": personnel,
    }