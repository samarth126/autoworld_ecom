from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

# from django.forms import 
# from .models import User

class RForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields= ['email', 'phone_no']