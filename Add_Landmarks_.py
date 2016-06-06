from ij import IJ
from  ij.process import ImageProcessor
from ij.io import OpenDialog, SaveDialog
from ij.gui import GenericDialog
import os
import csv
		
def ChooseLandmarkFile():
	od = OpenDialog("Choose Landmark file", None)	
	file_name = od.getFileName()
	dir_name = od.getDirectory()
	print("Reading "+file_name)
	print("in directory "+dir_name)	
	return dir_name, file_name

def ChooseImageFile(image_type):
	od = OpenDialog("Choose %s image"%image_type, None)
	file_name = od.getFileName()
	dir_name = od.getDirectory()
	full_path = os.path.join(dir_name,file_name)
	print("Opening %s"%full_path)
	imp = IJ.openImage(full_path)
	return imp

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

def DrawLandmarks(imp, pos, img_type):
	cal = imp.getCalibration()
	pixel_width  = cal.pixelWidth
	pixel_height = cal.pixelHeight
	pixel_depth  = cal.pixelDepth
	bit_depth = imp.getBitDepth()
	(width,height,n_channels,n_slices,n_frames) = imp.getDimensions()

	radius = 1 #width / 300

	on_val = 2**bit_depth - 1
	imp_landmarks = IJ.createImage("Landmarks",width,height,n_slices,bit_depth)
	imp_landmarks.setCalibration(cal)
	stack = imp_landmarks.getImageStack()

	for landmark in range(len(pos)):
		# Get x,y,z in pixels
		pX = int(round(pos[landmark][0]/pixel_width))
		pY = int(round(pos[landmark][1]/pixel_height))
		pZ = int(round(pos[landmark][2]/pixel_depth))

		print(pX,pY,pZ)
		ip = stack.getProcessor(pZ+1)
		for x in range(pX-radius,pX+radius):
			for y in range(pY-radius,pY+radius):
#				print("Putting %d at (%d,%d,%d)"%(on_val,x,y,pZ))
				if (((x-pX)**2 + (y-pY)**2) <= radius**2):
					ip.putPixel(x,y,on_val)
	imp_landmarks.setTitle(img_type)
	imp_landmarks.updateAndDraw()
	imp_landmarks.show()
	return imp_landmarks

def main():
#	IJ.open()
	imp_target = ChooseImageFile("Target")
	imp_moving = ChooseImageFile("Moving")
	imp_target.show()
	imp_moving.show()
	dir_name,file_name = ChooseLandmarkFile()
	moving_pos, target_pos = ParseLandmarkFile(dir_name,file_name)
	imp_target_landmarks = DrawLandmarks(imp_target,target_pos,"Target landmarks")
	imp_moving_landmarks = DrawLandmarks(imp_moving,moving_pos,"Moving landmarks")

#	imp_target_landmarks.show()
#	imp_target_landmarks.updateAndDraw()

if __name__ == "__main__":
	main()

	