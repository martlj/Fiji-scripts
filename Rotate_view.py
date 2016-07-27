import ij3d
from ij import IJ

univ = ij3d.Image3DUniverse.universes.get(0)

ij3d.UniverseSettings.showScalebar()

#nSteps = 20
#for step in range(nSteps):
#	file_name = "/Users/jones58/Documents/Scratch/CellMovie/V2/Images/Cell"+str(step)+".tiff"
#	univ.rotateY(2* 3.141592 / nSteps)
#	imp = univ.takeSnapshot(1440, 870)
#	IJ.save(imp,file_name)