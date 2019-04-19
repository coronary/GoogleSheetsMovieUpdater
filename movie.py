import gspread
#from imdbpie import Imdb
import imdb
from oauth2client.service_account import ServiceAccountCredentials
#Authenticates the app with google

#def spreadAuth():
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('newKey.json', scope)
gs = gspread.authorize(credentials)

<<<<<<< HEAD
def directory():
	sheetName = 'Movie Tracker'
	gsheet = gs.open(sheetName)
=======
imdb = imdb.IMDb()


#print((imdb.get_title(imdb.search_for_title("Suspiria")[0]['imdb_id'])["soundtrack"]))
#print(dir(imdb))
def sheetChoose(gsheet):
>>>>>>> testing
	tempSheets = gsheet.worksheets()
	sheets = []
	for x in tempSheets:
		sheets.append(x.title)
	while True:
		try:
			print (", ".join(sheets))
			sheet = int(input('Choose the index of the sheet you want '))
			if sheet >= len(sheets):
				raise IndexError
			break
		except Exception as c:
			print (c)
			print ('Must be a valid index between 0 and ' + str(len(sheets)))
	return sheets[sheet]

def rowAsk():
	while True:
		try:
			start = int(input('Starting row: '))
			end = int(input('Ending row: '))
			break
		except:
			print ('Must both be integers')
	return (start, end)

def directory():
	sheetName = 'Movie Tracker'
	sheetURL = ("https://docs.google.com/spreadsheets/d/1K9E4SD_xcQ1i_ouxvIJKPpCLG-OQPw4bGBjjJ4IUmK0/edit#gid=0")
	#gs = spreadAuth()
	gsheet = gs.open_by_url(sheetURL)
	sheet = sheetChoose(gsheet)

	choice = int(input('movie update(1), days watching movies(2): '))
	if choice == 2:
		time(gsheet, sheet)
	else:
		start, end = rowAsk()
		readSheet(gsheet, sheet, start, end)

def readSheet(gsheet, sheet, start, end):
	#opens movie spreadsheet
	currentSheet = gsheet.worksheet(sheet)
	columnTitles = currentSheet.row_values(1)
	movieTitle = columnTitles.index('Title') + 1
	tColumn = columnTitles.index('Runtime') + 1
	gColumn = columnTitles.index('Genre') + 1
	rColumn = columnTitles.index('Runtime') + 1
	#Starts on right number, ends one less than stated

	for x in range(start, end + 1):
		currentSheet.update_cell(x, tColumn, 'X')
		#Grabs movie title
		movie = currentSheet.cell(x, movieTitle).value
		try:
			#(imdb.get_movie(mov[0].movieID)["genre"])
			#Searches for the movie on OMDB
<<<<<<< HEAD
			baseInfo = Imdb().search_for_title(movie)
			search = baseInfo[0]['imdb_id']
			genre = Imdb().get_title_genres(search)["genres"]
			runtime = (Imdb().get_title(search))["base"]["runningTimeInMinutes"]
			#Updates cells with genre and runtime
			currentSheet.update_cell(x, gColumn, comma.join(genre))
			currentSheet.update_cell(x, rColumn, str(runtime) + ' min')
=======

			baseInfo = imdb.search_movie(movie)[0].movieID
			search = imdb.get_movie(baseInfo)

			#Updates cells with genre and runtime
			currentSheet.update_cell(x, gColumn, ", ".join(search["genres"]))
			currentSheet.update_cell(x, rColumn, str(int(search["runtimes"][0])) + ' min')
>>>>>>> testing
		except Exception as c:
			print (str(c) + " at row " + str(x))
			#if it fucks up it owns up to it
			currentSheet.update_cell(x, gColumn, 'fucked up')
			currentSheet.update_cell(x, rColumn, '')
		#currentSheet.update_cell(x, tColumn, '')

def time(gsheet, sheet):
	currentSheet = gsheet.worksheet(sheet)
	columnTitles = currentSheet.row_values(1)
	rColumn = (columnTitles.index('Runtime'))
	sum = 0
	row = currentSheet.row_values(1)
	count = 2
	while row[0] != '':
		try:
			print ('current Row: ' + str(count))
			row = currentSheet.row_values(count)
			timeM = row[rColumn]
			if (timeM == '' or timeM == 'N/A'):
				pass
			else:
				sum += float((timeM.split()[0]))
			count += 1
		except Exception as error:
			print (str(error) + ' at row ' + str(count))
	print (str(((sum/60)/24)) + ' days of watching movies')
	quit()

directory()
