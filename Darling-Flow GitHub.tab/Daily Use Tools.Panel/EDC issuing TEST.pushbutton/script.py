import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
from System.Collections.Generic import *

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

import os
os.chdir("E:\RV-WIP Local")

import System

import math

import time

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
uidoc=DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

FilePATHS = RVTsToIssue = ["C:\Users\jiruzubieta\Desktop\WIP\EDC-DAA-IXX001-ZZ-M3-A-0001_detached.rvt",
"C:\Users\jiruzubieta\Desktop\WIP\EDC-DAA-XX-ZZ-M3-A-0001_detached.rvt"]
if not isinstance(FilePATHS,list):
	FilePATHS = [FilePATHS]

DestinationFolder = "C:\Users\jiruzubieta\Desktop\WIP\Destination21"
RVTIsRequired = True
IFCIsRequired = True
NWCIsRequired = True
ExportViewName = "Export-NWC"
#Opening detach RVT options


detachWorksetConfig = WorksetConfiguration()
#detachWorksetConfig.Close(True)
openDetachOptions = OpenOptions()
openDetachOptions.DetachFromCentralOption = DetachFromCentralOption.DetachAndPreserveWorksets
openDetachOptions.SetOpenWorksetsConfiguration(detachWorksetConfig)

localWorksetConfig = WorksetConfiguration()
#localWorksetConfig.Open()
openLocalOptions = OpenOptions()
openLocalOptions.DetachFromCentralOption = DetachFromCentralOption.DoNotDetach
openLocalOptions.SetOpenWorksetsConfiguration(localWorksetConfig)

worksharingOptions = WorksharingSaveAsOptions()
worksharingOptions.SaveAsCentral = True

transacOption = TransactWithCentralOptions()

syncOption = SynchronizeWithCentralOptions()
syncOption.SetRelinquishOptions(None)

worksharingOptions = WorksharingSaveAsOptions()
worksharingOptions.SaveAsCentral = True
saveAsOptions = SaveAsOptions()
saveAsOptions.SetWorksharingOptions(worksharingOptions)
saveAsOptions.OverwriteExistingFile = True

#SaveOptions = SaveAsOptions()
#SaveOptions.SetWorksharingOptions(worksharingOptions)

tOptions = TransactWithCentralOptions()

rOptions = RelinquishOptions(False)
rOptions.StandardWorksets = True
rOptions.ViewWorksets = True
rOptions.FamilyWorksets = True
rOptions.UserWorksets = True
rOptions.CheckedOutElements = True

sOptions = SynchronizeWithCentralOptions()
sOptions.SetRelinquishOptions(rOptions)
sOptions.Compact = True
sOptions.SaveLocalBefore = False
sOptions.SaveLocalAfter = False

#File Formats and Names Checkers
#File Names lists
#FileNames = []
FileNamesRVTs = []
FileNamesIFCs = []
FileNamesNWCs = []
#lastcharacters = []
#lastnumbers = []
#FileNameNWCs = []
newdoclist = []
ifcExportOption = IFCExportOptions()

nwcExportOptions = NavisworksExportOptions()
nwcExportOptions.ExportScope = NavisworksExportScope.View
#nwcExportOptions.ExportScope = NavisworksExportScope.View
#nwcExportOptions.ExportScope = NavisworksExportScope.Model
nwcExportOptions.ConvertElementProperties = True
nwcExportOptions.ExportRoomGeometry = False

RestOfSheets = []

for file in FilePATHS:
	modelpath = FilePath(file)
	FileName = file.split("\\")[-1]
	FileNameRVT = FileName
	FileNameRVTcleaned = FileName[:-4]
	FileNameIFC = FileNameRVTcleaned.replace("-M3-","-MR-")
	FileNameNWC = FileNameIFC
	#OpeningFiles
	localDoc = app.OpenDocumentFile(modelpath,openLocalOptions)

	Transaction1 = Transaction(localDoc,"Export NWC & IFC files")
	Transaction1.Start()
	
	if IFCIsRequired or NWCIsRequired:
		exportViewId  = None	
		views = FilteredElementCollector(localDoc).OfClass(View3D).WhereElementIsNotElementType()
		for v in views:
			if v.Name == ExportViewName:
				exportViewId  = v.Id
				break

	if IFCIsRequired:
		ifcExportOption.FilterViewId = ElementId.InvalidElementId
		ifcExportOption.FileVersion = IFCVersion.IFC2x3
		localDoc.Export(DestinationFolder,FileNameIFC,ifcExportOption)
	
	Transaction1.Commit()
	
	if NWCIsRequired:
		if exportViewId  != None:		
			nwcExportOptions.ViewId = exportViewId 
			localDoc.Export(DestinationFolder,FileNameNWC,nwcExportOptions)		
		else:
			nwcExportOptions.ExportScope = NavisworksExportScope.Model
			localDoc.Export(DestinationFolder,FileNameNWC,nwcExportOptions)

	
	localDoc.SynchronizeWithCentral(transacOption, syncOption)
	localDoc.Close(False)

	
	if RVTIsRequired:
		newdoc = app.OpenDocumentFile(modelpath,openDetachOptions)
		
		Transaction2 = Transaction(newdoc,"Save archive Revit model")
		Transaction2.Start()
		
		#collector = FilteredElementCollector(newdoc)
		#views = collector.OfClass(View).ToElements()
		viewsToKeep = ["Splash Screen", "Project View", "System Browser"]
		GAviewsToKeep = "GA-Export-"
		viewIds = List[Autodesk.Revit.DB.ElementId]()
		
		for v in FilteredElementCollector(newdoc).OfClass(View):
			ViewNames = v.Name.ToString()
			if (v.IsTemplate == False) and (v.Name not in viewsToKeep) and (ViewNames.startswith(GAviewsToKeep) == False):
				viewIds.Add(v.Id)
		newdoc.Delete(viewIds)

		Transaction2.Commit()

		newdoc.SaveAs(DestinationFolder+"\\"+FileNameRVT,saveAsOptions)
		WorksharingUtils.RelinquishOwnership(newdoc, RelinquishOptions(True), transacOption)	
		#WorksharingUtils.RelinquishOwnership(detachedDoc, RelinquishOptions(True), transacOption)
		#newdoc.SynchronizeWithCentral(tOptions,sOptions)
		newdoc.Close(False)

OUT = 'Good to go'