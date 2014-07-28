from django.contrib.auth.models import User
from models	import Book, Author, BookGenre, Editor, Edition,  BookAuthor
from django import forms
class acc():
	def accounts(self):
		return User.objects.all()

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('email','username','password','first_name','last_name')

class BookForm(forms.ModelForm):
	class Meta:
		model = Book
		fields = ('title','is_fiction')

class BookGForm(forms.ModelForm):
	class Meta :
		model = BookGenre

class EditorForm(forms.ModelForm):
	class Meta:
		model = Editor


class EditionForm(forms.ModelForm):
	pub_date = forms.DateField()
	class Meta:
		model = Edition


class AuthorForm(forms.ModelForm):
	class Meta:
		model = Author
		fields = ('af_name', 'al_name', 'pseudonym')


