import gspread
from imdbpie import Imdb
from oauth2client.service_account import ServiceAccountCredentials
#Authenticates the app with google
scope = "https://spreadsheets.google.com/feeds"
credentials = ServiceAccountCredentials.from_json_keyfile_name('key.json', scope)
gs = gspread.authorize(credentials)

def readSheet(sheet, person, gColumn, rColumn, start, end, Tcolumn):
	#opens movie spreadsheet
	gsheet = gs.open(sheet).worksheet(person)
	#Starts on right number, ends one less than stated
	for x in range(start, end):
		gsheet.update_cell(x, Tcolumn, 'X')
		#Grabs movie title
		movie = gsheet.cell(x, 1).value
		try:
			#Searches for the movie on OMDB
			baseInfo = Imdb().search_for_title(movie)
			search = Imdb().get_title_by_id(baseInfo[0]['imdb_id'])
			#Updates cells with genre and runtime
			comma = ', '
			gsheet.update_cell(x, gColumn, comma.join(search.genres))
			gsheet.update_cell(x, rColumn, str(int(search.runtime/60)) + ' min')
		except Exception as c:
			print (str(c) + " at row " + str(x))
			#if it fucks up it owns up to it
			gsheet.update_cell(x, gColumn, 'fucked up')
		gsheet.update_cell(x, Tcolumn, '')

def directory():
	sheets = ['experiment', 'Movie Tracker']
	cList = ['Collin', 2, 3, 6]
	mList = ['Molly', 4, 5, 6]
	person = input('c or m? ').lower()
	choice = int(input('movie update(1), days watching movies(2): '))
	if choice == 2:
		if person == 'c':
			time(cList[0], sheets[1], cList[2], cList[3])
		if person == 'm':
			time(mList[0], sheets[1], mList[2], mList[3])
	while True:
		try:
			start = int(input('Starting row: '))
			end = int(input('Ending row: '))
			break
		except:
			print ('Try again')
	if person == 'c':
		readSheet(sheets[1],cList[0],cList[1],cList[2],start,end+1,cList[3])
	elif person == 'm':
		readSheet(sheets[1],mList[0],mList[1],mList[2],start,end+1,mList[3])

def time(person, sheet, Rcolumn, Tcolumn):
	gsheet = gs.open(sheet).worksheet(person)
	sum = 0
	count = 0
	row = gsheet.row_values(count)
	#while row[0] != None:
	for x in range(1,2):
		row = gsheet.row_values(x)
		try:
			timeM = row[Rcolumn]
			sum += (timeM.split()[0])*60
			count += 1
			print (sum)
		except Exception as error:
			print (error)
			pass
directory()
