import sys
sys.path.append('../')
import datetime
from os import listdir
from csv import reader, DictReader
from mongoengine import *
from models import Demographic

# connect to our mongo database
connect("neuro_image_database")
FILE_PATH = "../../../Data_Files/Longitudinal_Network_Demographic.csv"
DIRECTORY_PATH = "../../../Data_Files/Network-Data"
# open file in read mode
with open(FILE_PATH, 'r') as read_obj:
	# pass the file object to reader() to get the reader object
	csv_dict_reader = DictReader(read_obj)
	for row in csv_dict_reader:
		demographic = Demographic()
		demographic.subject = row["subject"]
		demographic.ptid = row["PTID"]
		demographic.examdate = datetime.datetime.strptime(row["EXAMDATE.x"], "%m/%d/%Y").date()
		demographic.viscode = row["VISCODE"]
		demographic.dx_bl = row["DX_bl"]
		demographic.age = float(row["AGE"])
		demographic.ptgender = row["PTGENDER"]
		demographic.pteducat = int(row["PTEDUCAT"])
		demographic.ptethcat = row["PTETHCAT"]
		demographic.ptraccat = row["PTRACCAT"]
		demographic.ptmarry = row["PTMARRY"]
		demographic.cdrsb = float(row["CDRSB"]) if row["CDRSB"] != "NA" else None 
		demographic.mmse = float(row["MMSE"]) if row["MMSE"] != "NA" else None
		demographic.save()

print("Completed importing the Longitudinal_Network_Demographic.csv file.")	
for filename in listdir(DIRECTORY_PATH):
	#print(f"filename: {filename}.")
	with open(DIRECTORY_PATH + "/" + filename) as file:
		content = ""
		for row in file:
			row = row.rstrip("\n").rstrip()
			content += row.replace("  ", ",")
			content += ";"
			
		content = content[0:-1]
		subject = filename.split("_")[0]
		oneRecord = Demographic.objects(subject = subject).update_one(set__content = content, upsert = True)

print("Completed importing all the matrix files in the Network-Data folder.")	