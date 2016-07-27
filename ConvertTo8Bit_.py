from ij import IJ, ImageStack, ImagePlus
from ij import WindowManager
from ij.measure import Calibration
from ij.process import StackConverter
from ij.plugin import ContrastEnhancer
from ij.gui import WaitForUserDialog, GenericDialog

def AdjustContrast(imp):
# 	percent_saturated = 0.35
# 	CE = ContrastEnhancer()
# 	CE.setNormalize(True)
# 	CE.setUseStackHistogram(True)
# 	CE.setProcessStack(True)
# 	CE.run("")
# 	IJ.run("Enhance Contrast","saturated=0.35")
	IJ.run("Brightness/Contrast...","")
	WaitForUserDialog("Click to continue").show()
	
def Resize(imp):
	gd = GenericDialog("Image size")
	scales = ["1024","2048","4096"]
	gd.addChoice("Choose image size",scales,scales[1])
	gd.showDialog()
	scale_choice = gd.getNextChoice()
	IJ.run(imp,"Scale...", "x=- y=- z=1.0 width="+scale_choice+" height="+scale_choice+" interpolation=Bilinear average process create title=Scaled")
	scaled_imp = WindowManager.getImage("Scaled")
	return scaled_imp

def ConvertTo8bit(imp):
	IJ.run(imp,"8-bit","")


def SaveMovie(imp):
	IJ.run(imp,"AVI... ","")

def MakeStack():
	IJ.run("Bio-Formats","group_files use_virtual_stack")
	imp = WindowManager.getCurrentImage()
	return imp
	
def main():
	print "Starting script"
	imp = WindowManager.getCurrentImage()
	if not imp:
		imp = MakeStack()

	IJ.run(imp,"Properties...","")
	scaled_imp = Resize(imp)
	scaled_imp.show()
# 	WaitForUserDialog("Select an ROI if you want to restrict automatic contrast adjustment").show()
# 	imp.close()
	AdjustContrast(scaled_imp)
	ConvertTo8bit(scaled_imp)
# 	SaveMovie(scaled_imp)
#	imp.show()

if __name__ == "__main__":
	main()
	