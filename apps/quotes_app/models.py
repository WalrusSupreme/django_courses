from django.db import models
import re, bcrypt
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9+-_.]+\.[a-zA-Z]+$')

# Create your models here.

class UserManager(models.Manager):
    def register(self, form_data):
        errors = []

        if len(form_data["name"]) < 1:
            errors.append("Name is required")
        elif len(form_data["name"]) < 2:
            errors.append("First name must be 2 letters or longer")
        
        if len(form_data["alias"]) < 1:
            errors.append("An Alias is required")
        elif len(form_data["alias"]) < 2:
            errors.append("The Alias must be 2 letters or longer")

        if len(form_data["email"]) < 1:
            errors.append("Email is required")
        elif not EMAIL_REGEX.match(form_data["email"]):
            errors.append("Invalid Email")
        else:
            if len(User.objects.filter(email=form_data["email"].lower())) > 0:
                errors.append("Email already in use")

        if len(form_data["password"]) < 1:
            errors.append("Password is required")
        elif len(form_data["password"]) < 8:
            errors.append("Password must be 8 letters or longer")

        if len(form_data["confirm"]) < 1:
            errors.append("Confirm Password is required")
        elif form_data["password"] != form_data["confirm"]:
            errors.append("Confirm Password must match Password")
        if form_data['birthday'] == '':
            errors.append("Enter in a birthday, please")
        if len(errors) == 0:
            hashed_pw = bcrypt.hashpw(form_data["password"].encode(), bcrypt.gensalt())
            print(str(hashed_pw))
            user = User.objects.create(
                name = form_data["name"],
                alias = form_data["alias"],
                email = form_data["email"].lower(),
                birthday = form_data['birthday'],
                password = hashed_pw
            )
            return (True, user)
        else:
            return (False, errors)

    def login(self, form_data):

        errors = []

        if len(form_data["email"]) < 1:
            errors.append("Email is required")
        elif not EMAIL_REGEX.match(form_data["email"]):
            errors.append("Invalid Email")
        else:
            if len(User.objects.filter(email=form_data["email"].lower())) < 1:
                errors.append("Unknown email {}".format(form_data["email"]))

        if len(form_data["password"]) < 1:
            errors.append("Password is required")
        elif len(form_data["password"]) < 8:
            errors.append("Password must be 8 letters or longer")


        # print(hashed_pw)

        if len(errors) > 0:
            return (False, errors)

        user = User.objects.filter(email=form_data["email"].lower())[0]
        hashed_pw = user.password.split("'")[1]

        if bcrypt.checkpw(form_data["password"].encode(), hashed_pw.encode()):
            return (True, user)
        else:
            errors.append("Incorrect Password")
            return (False, errors)

class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    birthday = models.DateField(auto_now=False)

    objects = UserManager()



class QuoteManager(models.Manager):
    def validate_quote(self, quote_text, user_id, author):
        errors = []
        if len(author) < 4:
            errors.append("Please add a real author for this quote.")
        if len(quote_text) < 10:
            errors.append('Is that a quote?  Quotes are usually much longer, try again')
        current_user = User.objects.get(id = user_id)
        if len(errors) < 1:
            self.create(quote_text = quote_text, author = author, created_by = current_user)
            return (True, errors)
        else:
            return (False, errors)

    def add_favorite(self, user_id, quote_id):       
        quote = Quote.objects.get(id = quote_id)
        current_user = User.objects.get(id = user_id)
        quote.favoriting_users.add(current_user)
        return True
    
    def remove_favorite(self, user_id, quote_id):
        quote = Quote.objects.get(id = quote_id)
        current_user = User.objects.get(id = user_id)
        quote.favoriting_users.remove(current_user)


class Quote(models.Model):
    quote_text = models.TextField(max_length=1000)
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    favoriting_users = models.ManyToManyField(User, related_name="favorite_quotes")
    created_by = models.ForeignKey(User, related_name="quotes_posted", on_delete=models.CASCADE)
    objects = QuoteManager()