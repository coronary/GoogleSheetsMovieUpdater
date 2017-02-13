import gspread
from imdbpie import Imdb
from oauth2client.service_account import ServiceAccountCredentials
#Authenticates the app with google
scope = "https://spreadsheets.google.com/feeds"
credentials = ServiceAccountCredentials.from_json_keyfile_name('key.json', scope)
gs = gspread.authorize(credentials)
comma = ', '

def directory():
	sheetName = 'experiment'
	gsheet = gs.open(sheetName)
	#cList = ['Collin', 2, 3, 6]
	#mList = ['Molly', 4, 5, 6]
	tempSheets = gsheet.worksheets()
	sheets = []
	for x in tempSheets:
		sheets.append(x.title)
	while True:
		try:
			print (comma.join(sheets))
			sheet = int(input('Choose the index of the sheet you want '))
			if sheet >= len(sheets):
				raise IndexError
			break
		except Exception as c:
			print (c)
			print ('Must be a valid index between 0 and ' + str(len(sheets)))
	choice = int(input('movie update(1), days watching movies(2): '))
	if choice == 2:
		time(gsheet, sheets[sheet])
	while True:
		try:
			start = int(input('Starting row: '))
			end = int(input('Ending row: '))
			break
		except:
			print ('Must both be integers')
	readSheet(gsheet, sheets[sheet], start, end)

def readSheet(gsheet, sheet, start, end):
	#opens movie spreadsheet
	currentSheet = gsheet.worksheet(sheet)
	columnTitles = currentSheet.row_values(1)
	movieTitle = columnTitles.index('Title') + 1
	Tcolumn = columnTitles.index('') + 1
	gColumn = columnTitles.index('Genre') + 1
	rColumn = columnTitles.index('Runtime') + 1
	#Starts on right number, ends one less than stated
	for x in range(start, end+1):
		currentSheet.update_cell(x, Tcolumn, 'X')
		#Grabs movie title
		movie = currentSheet.cell(x, movieTitle).value
		try:
			#Searches for the movie on OMDB
			baseInfo = Imdb().search_for_title(movie)
			search = Imdb().get_title_by_id(baseInfo[0]['imdb_id'])
			#Updates cells with genre and runtime
			currentSheet.update_cell(x, gColumn, comma.join(search.genres))
			currentSheet.update_cell(x, rColumn, str(int(search.runtime/60)) + ' min')
		except Exception as c:
			print (str(c) + " at row " + str(x))
			#if it fucks up it owns up to it
			currentSheet.update_cell(x, gColumn, 'fucked up')
		currentSheet.update_cell(x, Tcolumn, '')

def time(gsheet, sheet):
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
