import MySQLdb

db = MySQLdb.connect(host="localhost", user="root",passwd="5*Hotel", db="library")
cur = db.cursor()


def insert_book(bk_title, fic_type):
	cur.execute("INSERT INTO book_search_book (title, is_fiction) VALUES (\"%s\", %s);" % (bk_title, fic_type))
	db.commit()

def insert_author(af_n, al_n):
	cur.execute("INSERT INTO book_search_author (af_name, al_name) VALUES (\"%s\", \"%s\");" % (af_n, al_n) )
	db.commit()

def insert_book_author(bk_title, al_n):
	cur.execute("INSERT INTO book_search_bookauthor (book_id, author_id) VALUES ((select book_id FROM book_search_book WHERE title = \"%s\"),(SELECT author_id FROM book_search_author WHERE al_name = \"%s\" ));" % (bk_title, al_n))
	db.commit()

def insert_edition(bk_title, isbn_num, pub_date, pub_n, lang):
	cur.execute("INSERT INTO book_search_edition (book_id, isbn, pub_date, publisher, language) VALUES ((SELECT book_id FROM book_search_book WHERE title = \"%s\"),\"%s\",\"%s\",\"%s\",\"%s\");" % (bk_title, isbn_num, pub_date, pub_n, lang))
	db.commit()

def insert_genre(bk_title, gen):
	cur.execute("SELECT book_id FROM book_search_book WHERE title=\"%s\";" % bk_title)
	cur.execute("INSERT INTO book_search_bookgenre (book_id, genre) VALUES ( \"%s\",\"%s\");" % (cur.fetchall()[0][0], gen))
	db.commit()

def insert_pseudonym(al_n, sudo):
	cur.execute("INSERT INTO book_search_pseudonym (author_id, pseudonym) VALUES ((SELECT author_id FROM book_search_author WHERE al_name=\"%s\"),\"%s\");" % (al_n, sudo))
	db.commit()

def getcur():
	return cur