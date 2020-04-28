import gettext
import os
import shutil
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from os import listdir
from os.path import isfile, join
from tkinter import ttk
from datetime import date
from pathlib import Path
import locale
import ctypes
import subprocess as sp

#find machine's language
language = locale.windows_locale[ctypes.windll.kernel32.GetUserDefaultUILanguage()]

#localize to machine
if language == 'es_MX':
	es = gettext.translation('es_MX', localedir='il8n/locale/', languages=['es_MX'])
	es.install()
elif language == 'fr_CA':
	fr = gettext.translation('fr_CA', localedir='il8n/locale/', languages=['fr_CA'])
	fr.install()
elif language == 'en_US':
	_ = gettext.gettext
else:
	_ = gettext.gettext

#initialize main window (named root)
root = Tk()
root.title("FileSorter")
root.geometry("+%d+%d" % (root.winfo_screenwidth()/8, root.winfo_screenheight()/8))
root.resizable(False, False)

#Variable Declaration
folderPath = StringVar()
folderDefaultList = ["", _("Images"), _("Videos"), _("Music"), _("Executables"), _("Documents"), _("Custom Value")]

#Default Criteria
listImageType = [".bmp", ".jpg", ".jpeg", ".tiff", ".gif", ".tif", ".png",".jpe", ".jif", ".jfif", ".jfi", ".jp2", ".ppm",".pgm",".pbm", ".webp"]
listVideoType = [	
				".webm", 
				".mkv",
				".flv",
				".vob", 
				".ogv",
				".ogg",
				".drc",
				"gifv",
				".mng",
				".avi",
				".mov",
				".qt",
				".mts",
				".m2ts",
				".ts",
				".wmv",
				".rmvb",
				".asf",
				".amv",
				".mp4",
				".m4p",
				".m4v",
				".mpg",
				".mp2",
				".mpeg",
				".mpe",
				".mpv",
				".mpg",
				".mpeg",
				".m2v",
				".svi",
				".3gp",
				".3g2",
				".nsv",
				".f4v",
				".f4p",
				".f4a",
				".f4b"
				]
listMusicType = [
				".3gp",
				".aa",
				".aac",
				".aax",
				".act",
				".aiff",
				".alac",
				".amr",
				".ape",
				".au",
				".awb",
				".dct",
				".dss",
				".dvf",
				".flac",
				".gsm", 
				".iklax", 
				".ivs",
				".m4a", 
				".m4b", 
				".m4p", 
				".mmf",
				".mp3", 
				".mpc", 
				".msv",
				".nmf",
				".nsf",
				".ogg",
				".oga",
				".mogg",
				".opus",
				".ra",
				".rm",
				".raw",
				".sln",
				".tta",
				".voc",
				".vox",
				".wav",
				".wma", 
				".wv",
				".8svx"
				]
listExecutableType = [".msi", ".exe", ".app", ".vb", ".scr",".cmd"]
listDocumentType = [".doc",".pdf",".docx", ".odt", ".wpd",".wp",".wp7",".rtf", ".swx", ".txt"]
listFileType = [listImageType, listVideoType, listMusicType, listExecutableType, listDocumentType]

ind = 0

#Function Def'n
def selectFolder():
	global folderPath
	folderPath = askdirectory(title="Select Folder")
	
	#Check if folder is not current directory
	if folderPath.replace("/", "\\") == os.path.dirname(os.path.abspath( __file__ )):
		folderPath = ""
		msgboxInvalidDir = Toplevel()
		msgboxInvalidDir.grab_set()
		msgboxInvalidDir.title(_("Cannot Sort!"))
		labelMsg = Label(msgboxInvalidDir, text=_("FileSorter is in this directory. It cannot sort itself! Please select another directory")).pack(padx=10, pady=10)
		buttonOkay = Button(msgboxInvalidDir, text=_("Okay"), padx=10, command=msgboxInvalidDir.destroy).pack(pady= 10)
		
		
	
	labelFilePath.config(text=folderPath)
	
	if folderPath:
		buttonSortDefault.config(state=NORMAL)
		buttonSortCustom.config(state=NORMAL)
	else: 
		buttonSortDefault.config(state=DISABLED)
		buttonSortCustom.config(state=DISABLED)

def createFolders(folderListDefault, type, folderListCustom):
	global folderPath
		
	if type == _('Default'):
	#create directories if they do not exist
		for i in range(1, len(folderListDefault)-1):
			if not os.path.exists(folderPath+"/"+folderListDefault[i]):
				Path(folderPath+"/"+folderListDefault[i]).mkdir(parents=True)
			
	if type == _('Custom'):
	#create directories if they do not exist
		for each in folderListCustom:
			if not os.path.exists(each):
				Path(each).mkdir(parents=True)
				
def sortDefault(DefaultList, logPath, root):
	
	createFolders(DefaultList, _('Default'), [''])
		
	#populate global variable filesList with file names & extensions
	filesList = [f for f in listdir(folderPath) if isfile(join(folderPath,f))]
	
	#create log address as string
	logAddress = logPath+"\FileSorter"+_("Log")+".log"
	#open log file & prepare for writing
	fileLog = open(logAddress.replace("/","\\"),'a')
	dateString = date.today().strftime('%b-%d-%Y')
	fileLog.write("FileSorter "+_("Log Sort Date: ") + dateString + _("\nSort Type for ") + dateString + _(": Default\n"))
		
	#check each file
	for files in range(len(filesList)):
		#sort by list
		for i in range(len(listFileType)):
			#sort by types
			for types in range(len(listFileType[i])):
				if listFileType[i][types].upper() in filesList[files][len(filesList[files])-5:len(filesList[files])].upper() and not os.path.exists(folderPath+"/"+folderDefaultList[i+1]+"/"+filesList[files]):
					shutil.move(folderPath+'/'+filesList[files], folderPath+'/'+folderDefaultList[i+1]+'/'+filesList[files])
					fileLog.write(folderPath+'/'+filesList[files]+' moved to '+folderPath+'/'+folderDefaultList[i+1]+'/'+filesList[files]+'\n')			
	fileLog.write("\n")
	fileLog.close()		
	msgDone(root)

def createCustom(logPath):
	custScreen = Toplevel()
	custScreen.title(_("Custom Sort"))
	custScreen.config(width=750, height=185)
	custScreen.geometry('+%d+%d' % (root.winfo_screenwidth()/7, root.winfo_screenheight()/6))
	custScreen.resizable(height = False, width = False)
	
	#Frames
	labelFrame = Frame(custScreen)
	labelFrame.grid(row=0,
					padx=30,
					pady=(20,0),
					sticky=W)
	
	custBottomFrame = Frame(custScreen)
	custBottomFrame.grid(row = 5, sticky=W)
	
	#instruction Labels
	labelInstructionFileType = Label(labelFrame, text=_("File Type - \tDefault options for file types is available. Blank(example: No search) as default line.\n\t\tCustom Value allows you to search for specific file extensions. Use comma's (\",\") for multiple file types."), justify=LEFT).grid(row=0, pady=(10,0), sticky=W)
	labelInstructionFolderName = Label(labelFrame, text=_("Folder Name - \tSelect the new or existing folder name of where you want the item to be sorted.")).grid(row=1, pady=(10,5), sticky=W)
	labelColumnHeaders = Label(labelFrame, text=_("File Type\t\t  Custom Value\t\tFile Path")).grid(row=2, pady=(5,0), sticky=W)
	
	formFields = createCanvasForm(custScreen)
		
	#bottom frame content
	custScButtonSort = Button(custBottomFrame, text=_("Sort"), padx=10, command=lambda: sortCustom(formFields, logPath, custScreen))
	custScButtonSort.grid(	row=0,
							column=0,
							padx=30,
							pady=(20,20),
							sticky=W)
		
	custScButtonQuit = Button(custBottomFrame, text=_("Quit"), padx=10, command=lambda: exitCustomScreen(custScreen))
	custScButtonQuit.grid(	row=0,
							column=1,
							padx=(570,30),
							pady=(20,20),
							sticky=E)

	custScreen.grab_set()
			
	custScreen.mainloop()

def exitCustomScreen(custScreen):
	global ind
	custScreen.destroy()
	ind = 0
	

def createCanvasForm(custScreen):
	
	#Create frame for Canvas
	custEntryFrame =Frame(custScreen)
	#Add Canvas to the frame
	custScreen.update()
	entryCanvas = Canvas(custEntryFrame, width=653, height = custScreen.winfo_height()+13)
	#add Scrollbar to Canvas
	vsb = Scrollbar(custEntryFrame, orient='vertical', command=entryCanvas.yview)
	
	custEntryFrame.grid(row=1, column=0, pady=(1,0), padx=(30,0), sticky=NW)
	entryCanvas.grid(row=0, column=0, padx=(1,0), sticky='news')
	vsb.grid(row=0, column=1, sticky='nes')
	
	#create frame for data entry line
	frame_CriteriaEntry = Frame(entryCanvas)
	entryCanvas.create_window((0,0), window = frame_CriteriaEntry, anchor=W)
	
	#Add form lists
	comboFileType=list()
	textFileExtEntry=list()
	textPathEntry=list()
	buttonSearchFolder=list()
	formFields = [comboFileType, textFileExtEntry, textPathEntry, buttonSearchFolder]

	global ind
	createFormRecord(formFields, frame_CriteriaEntry, ind, entryCanvas, vsb)
			
	#Update frames from idle tasks & calculate entry size
	frame_CriteriaEntry.update_idletasks()
	
	#resize canvas
	formWidth = comboFileType[0].winfo_width()+textFileExtEntry[0].winfo_width()+textPathEntry[0].winfo_width()+buttonSearchFolder[0].winfo_width()
	custEntryFrame.config(	width=formWidth,
							height= comboFileType[0].winfo_height())
	
	#Set Canvas scrolling region
	entryCanvas.config(scrollregion=entryCanvas.bbox('all'),yscrollcommand=vsb.set)
	entryCanvas.yview_moveto(0)
	
	return formFields

def createFormRecord(formFields, frame, ind, entryCanvas, vsb):
	#create combobox entry
	formFields[0].append(ttk.Combobox(frame, values = folderDefaultList, state='readonly', width=13))
	#create text entry (extension)
	formFields[1].append(Entry(frame,width=22, state=DISABLED))
	#initialize file path as blank
	v = StringVar()
	#create path entry (path)
	formFields[2].append(Entry(frame, width=65, textvariable=v))
	#create [...] button
	formFields[3].append(Button(frame, text="...", command=lambda:askDir(v)))
	#place entry items on canvas
	formFields[0][ind].grid(row=ind, column=0, sticky='news', padx=(0,2))
	formFields[1][ind].grid(row=ind, column=1, sticky='news', padx=(0,2))
	formFields[2][ind].grid(row=ind, column=2, sticky='news', padx=(0,2))
	formFields[3][ind].grid(row=ind, column=3, sticky='news')
	formFields[0][ind].bind('<<ComboboxSelected>>', lambda typeSelected:comboboxSelected(formFields, ind))
	v.trace('w' , lambda name, index, mode, v=v:entryChanged(v, formFields, frame, ind, entryCanvas, vsb))
	
def comboboxSelected(formFields,ind):
	if formFields[0][ind].get() == _("Custom Value"):
		formFields[1][ind].config(state=NORMAL)
	else:
		formFields[1][ind].config(state=DISABLED)
		contents = StringVar()
		formFields[1][ind].config(textvariable=contents)
		contents.set("")
	
def askDir(v):
	filePath = askdirectory(title=_("Select Folder"))
	v.set(filePath)
	
def sortCustom(passForm, logPath, screen): 
	global folderPath
	global listFileType
	global folderDefaultList
	
	#cleaning data
	dataForm = pullData(passForm)
	dataClean = cleanData(dataForm)
	
	createFolders( [''], _('Custom'), dataClean[2])

	folderDefaultPathList=[]
	
	#reverse
	for eachList in dataClean:
		eachList.reverse()
	
	#create temporary list of file types
	fileTypeToPath = [[],[], dataClean[0]]
	
	#create instructions
	for record in range(len(dataClean[1])):
		fileTypeToPath[0].append([dataClean[1][record]])
		fileTypeToPath[1].append(dataClean[2][record])
	
	#replace defaults with Default Criteria
	for line in range(len(fileTypeToPath[0])):
		for i in range(len(listFileType)):
			if fileTypeToPath[2][line]==folderDefaultList[i+1]:
				fileTypeToPath[0][line] = listFileType[i]
	
	filesList = [f for f in listdir(folderPath) if isfile(join(folderPath,f))]
	
	#open log file & prepare for writing
	logAddress = logPath+"\FileSorter"+_("Log")+".log"
	fileLog = open(logAddress.replace("/","\\"),'a')
	dateString = date.today().strftime('%b-%d-%Y')
	fileLog.write("FileSorter "+_("Log Sort Date: ") + dateString + _("\nSort Type for ") + dateString + _(": Custom\n"))
	
	#for each file
	for file in range(len(filesList)):
		#for each extension list
		for ext in range(len(fileTypeToPath[0])):
			#for each extension in extension list				
			for each in range(len(fileTypeToPath[0][ext])):	
				if fileTypeToPath[0][ext][each] and fileTypeToPath[0][ext][each].upper() in filesList[file][len(filesList[file])-5:len(filesList[file])].upper() and not os.path.exists(fileTypeToPath[1][ext][each]+'/'+filesList[file]):
					try:
						shutil.move(folderPath+'/'+filesList[file], fileTypeToPath[1][ext]+'/'+filesList[file])
						fileLog.write(folderPath+'/'+filesList[file]+_(' moved to ')+ fileTypeToPath[1][ext]+'/'+filesList[file]+'\n')
					except FileNotFoundError:
						pass			
	fileLog.write('\n')
	fileLog.close
	screen.grab_release()
	msgDone(screen)

def pullData(field):
	dataGot = [[] for i in range(len(field)-1)]
	for dataField in range(len(field)-1):
		for record in range(len(field[0])):
			dataGot[dataField].append(field[dataField][record].get())
	return dataGot	
	
def cleanData(dataForm):

	dataMod=[[] for i in range(len(dataForm))]
			
	#eliminate null path
	for records in range(len(dataForm[2])):
		checkRecord = dataForm[2].pop()
		if not checkRecord: 
			for i in range(len(dataForm)-1):
				dataForm[i].pop()
		if checkRecord:	
			dataMod[2].append(checkRecord)
			for i in range(len(dataForm)-1):
				dataMod[i].append(dataForm[i].pop())
		
	clearIndex = list()
	#identify custom value selected record
	for records in range(len(dataMod[2])):
		if dataMod[0][records] == _("Custom Value"):
			clearIndex.append(records)

	#duplicate "Custom Value" & append entries for each extension entered
	for records in range(len(clearIndex)):	
		valueSplit = dataMod[1][clearIndex[records]].replace('.', '').rstrip().rstrip(',').rstrip().split(',')
		valueSplit = [x.strip(' ') for x in valueSplit]
		valueSplit = list(dict.fromkeys(valueSplit))
		for i in range(len(valueSplit)):
			dataMod[0].append(dataMod[0][clearIndex[records]])
			dataMod[1].append(valueSplit[i].lower())
			dataMod[2].append(dataMod[2][clearIndex[records]])
				
	#clear out form entries  that have "Custom Value" & multiple extensions listed
	for ele in sorted(clearIndex, reverse = True):
		for i in range(len(dataMod)):
			del dataMod[i][ele]
	
	return dataMod
	
def msgDone(previous): #opted for self made message box for interaction control
	#Tell User Done
	msgboxDone = Toplevel()
	msgboxDone.title(_('Done'))
	width= 200
	height = 100
	msgboxDone.geometry("%dx%d+%d+%d" % (width, height, msgboxDone.winfo_screenwidth()/2-width/2, msgboxDone.winfo_screenheight()/2-height/2))
	msgboxDone.grab_set()
	labelMessage = Label(msgboxDone, text = _("Sort Done!"), padx=10, pady=10).place(relx=0.5, rely= 0.5, anchor= S)
	buttonOkay = Button(msgboxDone, text=_("Okay"),padx=10, command=lambda: msgboxControl(msgboxDone, previous)).place(relx=0.5, rely=0.8, anchor= S)
	
def msgboxControl(previous, secondprevious):
	previous.grab_release()
	previous.destroy()
	secondprevious.grab_set()
	
def entryChanged(v, formFields, frame, current, entryCanvas, vsb):
	global ind
	checkList =[]
	for each in range(len(formFields[2])):
		checkList.append(formFields[2][each].get())
	checkList[current] = v.get()
	if not '' in checkList:
		ind += 1		
		createFormRecord(formFields, frame, ind, entryCanvas, vsb)
	#update scroll bar & canvas
	frame.update_idletasks()
	entryCanvas.config(scrollregion=entryCanvas.bbox('all'),yscrollcommand=vsb.set)
	entryCanvas.yview_moveto(1)

def viewLog(sp, address):
	try: #log should have been created in line 461-465; just in case log was deleted manually while program running
		sp.Popen(["notepad.exe", address])
	except: 
		messagebox.showinfo("File not Found", "No log found!")

#Start Logging
basePath = os.path.dirname(os.path.abspath( __file__ ))
address = basePath+"\FileSorter"+_("Log")+".log"
file = open(address, 'a+')
file.close()

#Frames
topFrame = Frame(root)
topFrame.grid(row=0, padx=30, pady=(20,0), sticky=W)
midFrame=Frame(root)
midFrame.grid(row=1, sticky=W)
sortFrame = Frame(root)
sortFrame.grid(row=2, sticky=W, padx=30, pady= 10)
bottomFrame = Frame(root)
bottomFrame.grid(row=3, sticky=W, padx=30, pady=(0,30))

#top frame content
labelInstructionMain = Label(topFrame, text=_("Thank you for choosing to use FileSorter. Language is automatically determined and changed to your local language.\nClick \"Browse for Folder\" button and browse to the folder you want to sort"), justify=LEFT)
#mid frame content
buttonBrowseFolder = Button(midFrame, text=_("Browse for Folder"), command=selectFolder)
labelFilePath = Label(midFrame)
#sort frame content
buttonSortDefault = Button(sortFrame, text=_("Default Sort"), state=DISABLED, command=lambda: sortDefault(folderDefaultList, basePath, root))
buttonSortCustom = Button(sortFrame, text=_("Custom Sort"), state=DISABLED,  command=lambda: createCustom(basePath))
#bottom frame content
buttonReview = Button(bottomFrame, text=_("Review your last sort"), command=lambda: viewLog(sp, address)) 
buttonQuit = Button(bottomFrame, text=_("Quit"), padx=10, command=root.destroy)

#packing UI
labelInstructionMain.grid(	row=0,
							sticky=E)
buttonBrowseFolder.grid(row=0,
						sticky=E,
						padx=(30,5),
						pady=(30,5))
labelFilePath.grid(	row=0,
					column=1,
					sticky=E,
					pady= (30,5))
buttonSortDefault.grid(	row=0,
						column=0,
						sticky=E,
						pady=20)
buttonSortCustom.grid(	row=0,
						column=1,
						sticky=E,
						padx=20,
						pady=20)
buttonReview.grid(	row=0,
					sticky=E)
buttonQuit.grid(row=0,
				column=1,
				sticky=W,
				padx=(450,0))

root.mainloop()