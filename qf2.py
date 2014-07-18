from book_search.models	import Book, Author, BookGenre, Editor, Edition, Pseudonym, Author

def search_genre(genre):
	gen = BookGenre.objects.filter(genre__icontains=genre)
	book_genre = []
	book = []
	for index, genre in enumerate(gen):
		book.append({'book_id':str(genre.book_id), 'genre':genre.genre})
		book_genre.append((genre.book_id, genre.genre))

	for b in book:
		book_result = Book.objects.get(book_id=str(b['book_id']))
		b.update({'title':book_result.title, 'is_fiction':book_result.is_fiction,   'authorid':123})


def search_gen(genre):
	gen = BookGenre.objects.filter(genre__icontains=genre)
	results = []
	books = []
	for i in gen:
		results.append(i)
	for i in results:
		print i.author_id.afull_name




	
		
	



