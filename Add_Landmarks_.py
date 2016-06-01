from ij import IJ
import ij.process.ImageProcessor
from ij.io import OpenDialog, SaveDialog
from ij.gui import GenericDialog
import os
import csv

def GetScaleFactor():
	gd = GenericDialog("Input Scale Factor")
	gd.addNumericField("Name",8,2)
	gd.showDialog()
	scale_factor = gd.getNextNumber()
	return scale_factor

#def OpenImage():
#	IJ.open()s


		
def ChooseLandmarkFile():
	od = OpenDialog("Choose Landmark file", None)	
	file_name = od.getFileName()
	dir_name = od.getDirectory()
	print("Reading "+file_name)
	print("in directory "+dir_name)	
	return dir_name, file_name

def ParseLandmarkFile(dir_to_open,file_to_open):
	print("Reading Landmark File")
	f = open(os.path.join(dir_to_open,file_to_open),'r');
	active_landmark_counter = 0
	inactive_landmark_counter = 0
	landmark_counter = 0
	moving_pos_array = []
	target_pos_array = []
	for line in csv.reader(f,quotechar='"',delimiter=',',quoting=csv.QUOTE_ALL, skipinitialspace=True):
#		print(line)
		landmark_counter += 1
		active = str(line[1])		
		moving_pos = [0]*3
		target_pos = [0]*3

#		print(x_target,y_target,z_target)
#		print(active)
		if active == 'true':
			moving_pos[0] = float(line[2])
			moving_pos[1] = float(line[3])
			moving_pos[2] = float(line[4])
	
			target_pos[0] = float(line[5])
			target_pos[1] = float(line[6])
			target_pos[2] = float(line[7])

			moving_pos_array.append(moving_pos)
			target_pos_array.append(target_pos)
			active_landmark_counter += 1
		else:
			inactive_landmark_counter += 1
	print("There are %d active landmarks"%(active_landmark_counter))
	print("and %d inactive landmarks"%(inactive_landmark_counter))

	return moving_pos_array, target_pos_array

def DrawCircles(imp, pos, radius):
	pix = imp.getProcessor()
	cal = imp.getCalibration()
	pixel_width  = cal.pixelWidth
	pixel_height = cal.pixelHeight
	pixel_depth  = cal.pixelDepth

#	landmark = 0
	for landmark in range(len(pos)):
		pX = int(round(pos[landmark][0]/pixel_width))
		pY = int(round(pos[landmark][1]/pixel_height))
		pZ = int(round(pos[landmark][2]/pixel_depth))

		print(pX,pY,pZ)

#	pixel_depth  
#	pixel_depth  = 

def main():
#	IJ.open()
	imp = IJ.getImage()
	dir_name,file_name = ChooseLandmarkFile()
	moving, target = ParseLandmarkFile(dir_name,file_name)
	DrawCircles(imp,target,10)
	

if __name__ == "__main__":
	main()




	