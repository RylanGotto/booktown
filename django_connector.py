import os
import sys
sys.path.append('/home/rylan/library/book_search')
sys.path.append('/home/rylan/library')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import get

def list_accounts():
	print get.get_account(1)


