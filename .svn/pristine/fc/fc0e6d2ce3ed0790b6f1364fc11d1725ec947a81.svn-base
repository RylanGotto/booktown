from django.db import models


# Create your models here.
class Book(models.Model):
    book_id = models.AutoField(primary_key=True, db_column="book_id")
    title = models.CharField(max_length=140)
    is_fiction = models.BooleanField()

    class Meta:
        ordering = ['-book_id']
    def __str__(self):
        return str(self.book_id)

class Author(models.Model):
    author_id = models.AutoField(primary_key=True, db_column="author_id")
    af_name = models.CharField(max_length=140)
    al_name = models.CharField(max_length=140)
    afull_name = models.CharField(max_length=140)
    pseudonym = models.CharField(max_length=140)
    class Meta:
        ordering = ['-author_id']
    def __str__(self):
        return str(self.author_id)

class BookAuthor(models.Model):
    book_id = models.ForeignKey(Book, db_column="book_id")
    author_id = models.ForeignKey(Author, db_column="author_id")
    class Meta:
        ordering = ['-author_id']
    def __str__(self):
        return str(self.book_id)+"-"+str(self.author_id)

class Edition(models.Model):
    book_id = models.ForeignKey(Book, db_column='book_id')
    isbn = models.CharField(max_length=14, primary_key=True)
    pub_date = models.DateField()
    publisher = models.CharField(max_length=140)
    language = models.CharField(max_length=140)
    class Meta:
        ordering = ['-isbn']
    def __str__(self):
        return str(self.isbn)

class BookGenre(models.Model):
    book_id = models.ForeignKey(Book, db_column='book_id')
    genre = models.CharField(max_length=140)
    class Meta:
        ordering = ['-genre']
    def __str__(self):
        return str(self.genre) + "-" + str(self.book_id)

class Editor(models.Model):
    isbn = models.ForeignKey(Edition, db_column='isbn', primary_key=True)
    editor_name = models.CharField(max_length=250)
    class Meta:
        ordering = ['-editor_name']
    def __str__(self):
        return str(self.el_name)



