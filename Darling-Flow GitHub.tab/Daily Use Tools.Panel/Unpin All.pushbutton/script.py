# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

import clr
import System
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('DSCoreNodes')
from DSCore.List import Flatten

 
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument
 
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

viewsToKeep = ["Splash Screen", "Project View", "System Browser"]
sheets = []

CollectorLevels = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
CollectorGrids = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Grids).WhereElementIsNotElementType().ToElements()
CollectorRVTlinks = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RvtLinks
).WhereElementIsNotElementType().ToElements()
CollectorProjectBase = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_ProjectBasePoint
).WhereElementIsNotElementType().ToElements()
CollectorImportInstances = FilteredElementCollector(doc).OfClass(ImportInstance
).WhereElementIsNotElementType().ToElements()

ElementsCollector = []

ElementsCollector.append(CollectorLevels)
ElementsCollector.append(CollectorGrids)
ElementsCollector.append(CollectorRVTlinks)
ElementsCollector.append(CollectorProjectBase)
ElementsCollector.append(CollectorImportInstances)

FlattenList = Flatten(ElementsCollector)

OutList =[]

Transaction1 = Transaction(doc,"Pin all")
Transaction1.Start()

for s in FlattenList:
	Element.Pinned.SetValue(s,False)
	OutList.append(s)

#for v in Collector:
#	if (v.Name in viewsToKeep):
#		Element.Pinned.SetValue(v,True)
			
			
			#v.Element.Pinned.Set
#		sheets.append(v)
			#sheets.Pinned(True)
Transaction1.Commit()
#sheets.Pinned(True)
#for v in FilteredElementCollector(doc).OfClass(View):
#	if (v.IsTemplate == False) and (v.Name in viewsToKeep):
#			viewIds.append(v.Id)



OUT = OutList