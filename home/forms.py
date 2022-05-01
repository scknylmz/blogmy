from django.conf import settings
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=50, 
                            required=True, 
                            widget=forms.TextInput(attrs={
                                'hx-get' : reverse_lazy('check-name'), 
                                'hx-target' : '#id-name-error',
                                'hx-trigger' : 'keyup changed delay:1s',
                                'hx-include': '[name="email"], [name="subject"], [name="message"]'
                            }))
    email = forms.EmailField(required=True,
                            widget=forms.TextInput(attrs={
                                'hx-get' : reverse_lazy('check-email'), 
                                'hx-target' : '#id-email-error',
                                'hx-trigger' : 'keyup changed delay:1s',
                                'hx-include': '[name="name"], [name="subject"], [name="message"]'
                            }))
    subject = forms.CharField(max_length=100, 
                                required=True,
                                widget=forms.TextInput(attrs={
                                'hx-get' : reverse_lazy('check-subject'), 
                                'hx-target' : '#id-subject-error',
                                'hx-trigger' : 'keyup changed delay:1s',
                                'hx-include': '[name="name"], [name="email"], [name="message"]'
                            }))
    message = forms.CharField(required=False,widget=forms.Textarea())
    
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Name'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['subject'].widget.attrs['class'] = 'form-control'
        self.fields['subject'].widget.attrs['placeholder'] = 'Subject'
        self.fields['message'].widget.attrs['class'] = 'form-control'
        self.fields['message'].widget.attrs['placeholder'] = 'Message'

    def clean_name(self):
        name = self.cleaned_data['name']
        for i in name:
            if i.isnumeric():
                raise forms.ValidationError('Your Name Can Not Contain Number')
        if len(name) < 3:
            raise forms.ValidationError('Your Name Is Too Short')
        return name

    def clean_email(self):
        email = self.cleaned_data['email']
        if email.find('@') <0:
            raise forms.ValidationError('It Should Contains "@')
        elif email.find('.') < 0:
            raise forms.ValidationError('It Should Contains "."')
        return email

    def clean_subject(self):
        subject=self.cleaned_data['subject']
        if len(subject) < 2:
            raise forms.ValidationError('You Must Enter a Subject')

        return subject
    
    def get_info(self):
        cl_data = super().clean()

        name = cl_data.get('name').strip()
        from_email = cl_data.get('email')
        subject = cl_data.get('subject')

        msg = f'{name} with email {from_email} said:'
        msg += f'\n"{subject}"\n\n'
        msg += cl_data.get('message')
        print( msg, subject)
        return subject, msg

    def send(self):
        subject, msg = self.get_info()
        print( msg, subject)
        send_mail(
            subject=subject,
            message=msg,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.RECIPIENT_ADDRESS]
        )