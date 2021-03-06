#!/usr/bin/python
import csv
import sys
import MySQLdb

db = MySQLdb.connect(host="localhost", user="root", passwd="5*Hotel", db=sys.argv[2])
cur = db.cursor()


def insert_book(bk_title, fic_type):
	cur.execute("INSERT INTO book_search_book (title, is_fiction) VALUES (\"%s\", %s);" % (bk_title, fic_type))
	db.commit()

def insert_author(af_n, al_n, afull_name, pseudonym):
	cur.execute("INSERT INTO book_search_author (af_name, al_name, afull_name, pseudonym) VALUES (\"%s\", \"%s\", \"%s\", \"%s\");" % (af_n, al_n, afull_name, pseudonym))
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


def insert_editor(bk_title, editor_name):
	cur.execute("INSERT INTO book_search_editor (isbn, editor_name) VALUES ((SELECT isbn FROM book_search_edition JOIN book_search_book USING (book_id) WHERE book_search_book.title = \"%s\"), \"%s\");" % (bk_title, editor_name))
	db.commit()


def getcur():
	return cur



def loaddb(csvfile):
	with open(csvfile, 'rb') as csvfile:
		dialect = csv.Sniffer().sniff(csvfile.read(), delimiters='|')
		csvfile.seek(0)
		reader = csv.reader(csvfile, dialect)
		for row in reader:
			if len(row) == 12:
				bk_title = row[0].lstrip()
				fic_type = row[1].lstrip()
				al_n = row[2].lstrip()
				af_n = row[3].lstrip()
				afull_name = row[4].lstrip()
				sudo = row[5].lstrip()
				isbn_num = row[6].lstrip()
				pub_date = row[7].lstrip()
				pub_n = row[8].lstrip()
				lang = row[9].lstrip()
				gen = row[10].lstrip()
				editor_name = row[11].lstrip()
				insert_book(bk_title, fic_type)
				insert_author(af_n, al_n, afull_name, sudo)
				insert_book_author(bk_title, al_n)
				insert_edition(bk_title, isbn_num, pub_date, pub_n, lang)
				insert_editor(bk_title, editor_name)
				insert_genre(bk_title, gen)
				print "The following entry has been made to the database: \n"
				print row, "\n"
			else:
				print "***********************************************\nThe following line had to many items needed 12 was %s" % len(row)
				print row

if __name__ == '__main__':
	loaddb(sys.argv[1])