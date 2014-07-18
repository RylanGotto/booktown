def search_genre(genre):
	gen = BookGenre.objects.filter(genre__icontains=genre)
	book_genre = []
	for index, genre in enumerate(gen):
		book_genre.append((genre.book_id, genre.genre))
		print book_genre[index][0]
		print book_genre[index][1]


