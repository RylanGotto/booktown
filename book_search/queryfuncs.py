import MySQLdb
from random import randint
db = MySQLdb.connect(host="localhost", user="root",passwd="5*Hotel", db="library2")
cur = db.cursor()

def search_genre(genre):
	cur.execute('SELECT b.title, b.is_fiction, g.genre, en.isbn, en.pub_date, en.publisher, en.language, er.editor_name, a.afull_name, a.pseudonym FROM book_search_book b LEFT JOIN book_search_bookgenre g on (b.book_id=g.book_id)LEFT JOIN book_search_edition en on (b.book_id=en.book_id) LEFT JOIN book_search_editor er ON (en.isbn = er.isbn) LEFT JOIN book_search_bookauthor ba ON (b.book_id=ba.book_id) join book_search_author a ON (ba.author_id=a.author_id) WHERE g.genre LIKE \"%s\";' % ('%'+genre+'%'))
	result = []
	for i in cur.fetchall():
		row = {"title":i[0],"is_fict":i[1],'genre':i[2],"isbn":i[3],"date":i[4],"publisher":i[5],"language":i[6], "editor":i[7],"author":i[8],"pseudonym":i[9]}
		result.append(row)
	return result

def search_title(title):
	cur.execute('SELECT b.title, b.is_fiction, g.genre, en.isbn, en.pub_date, en.publisher, en.language, er.editor_name, a.afull_name, a.pseudonym FROM book_search_book b LEFT JOIN book_search_bookgenre g on (b.book_id=g.book_id)LEFT JOIN book_search_edition en on (b.book_id=en.book_id) LEFT JOIN book_search_editor er ON (en.isbn = er.isbn) LEFT JOIN book_search_bookauthor ba ON (b.book_id=ba.book_id) join book_search_author a ON (ba.author_id=a.author_id) WHERE b.title LIKE \"%s\";' % ('%'+title+'%'))
	result = []
	for i in cur.fetchall():
		row = {"title":i[0],"is_fict":i[1],'genre':i[2],"isbn":i[3],"date":i[4],"publisher":i[5],"language":i[6], "editor":i[7],"author":i[8],"pseudonym":i[9]}
		result.append(row)
	return result


def search_author(afullname):
	cur.execute('SELECT b.title, b.is_fiction, g.genre, en.isbn, en.pub_date, en.publisher, en.language, er.editor_name, a.afull_name, a.pseudonym FROM book_search_book b LEFT JOIN book_search_bookgenre g on (b.book_id=g.book_id)LEFT JOIN book_search_edition en on (b.book_id=en.book_id) LEFT JOIN book_search_editor er ON (en.isbn = er.isbn) LEFT JOIN book_search_bookauthor ba ON (b.book_id=ba.book_id) join book_search_author a ON (ba.author_id=a.author_id)  WHERE a.afull_name LIKE \"%s\";' % ('%'+afullname+'%'))
	result = []
	for i in cur.fetchall():
		row = {"title":i[0],"is_fict":i[1],'genre':i[2],"isbn":i[3],"date":i[4],"publisher":i[5],"language":i[6], "editor":i[7],"author":i[8],"pseudonym":i[9]}
		result.append(row)
	return result

def search_pub(pubname):
	cur.execute('SELECT b.title, b.is_fiction, g.genre, en.isbn, en.pub_date, en.publisher, en.language, er.editor_name, a.afull_name, a.pseudonym FROM book_search_book b LEFT JOIN book_search_bookgenre g on (b.book_id=g.book_id)LEFT JOIN book_search_edition en on (b.book_id=en.book_id) LEFT JOIN book_search_editor er ON (en.isbn = er.isbn) LEFT JOIN book_search_bookauthor ba ON (b.book_id=ba.book_id) join book_search_author a ON (ba.author_id=a.author_id) WHERE en.publisher LIKE \"%s\";' % ('%'+pubname+'%'))
	result = []
	for i in cur.fetchall():
		row = {"title":i[0],"is_fict":i[1],'genre':i[2],"isbn":i[3],"date":i[4],"publisher":i[5],"language":i[6], "editor":i[7],"author":i[8],"pseudonym":i[9]}
		result.append(row)
	return result

def feeling_lucky():
	cur.execute('SELECT count(*) from book_search_book')
	ran = int(cur.fetchall()[0][0])
	randint(1, ran)
	cur.execute('SELECT b.title, b.is_fiction, g.genre, en.isbn, en.pub_date, en.publisher, en.language, er.editor_name, a.afull_name, a.pseudonym FROM book_search_book b LEFT JOIN book_search_bookgenre g on (b.book_id=g.book_id)LEFT JOIN book_search_edition en on (b.book_id=en.book_id) LEFT JOIN book_search_editor er ON (en.isbn = er.isbn) LEFT JOIN book_search_bookauthor ba ON (b.book_id=ba.book_id) join book_search_author a ON (ba.author_id=a.author_id) WHERE b.book_id LIKE %d;' % randint(1, ran))
	result = []
	for i in cur.fetchall():
		row = {"title":i[0],"is_fict":i[1],'genre':i[2],"isbn":i[3],"date":i[4],"publisher":i[5],"language":i[6], "editor":i[7],"author":i[8],"pseudonym":i[9]}
		result.append(row)
	return result



