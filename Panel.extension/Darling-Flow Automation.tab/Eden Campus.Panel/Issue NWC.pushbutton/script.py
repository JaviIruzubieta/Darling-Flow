import clr
# Import Element wrapper extension methods
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument
uidoc=DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

clr.AddReference('RevitAPIUI')
#import everything from the UI Namespace...
from Autodesk.Revit.UI import *

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)
from datetime import datetime

import System
from System import Array
from System.Collections.Generic import *

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

RunIt = True
#RevDate = IN[2]
uwdoc = UnwrapElement(doc)
sheetList = []
splashscreen = []


if RunIt:
	try:
		errorReport = None
		
		TransactionManager.Instance.EnsureInTransaction(uwdoc)
		
		RevDescription = 'Suitable for Coordination'
		NewRevision = Revision.Create(doc)
		Description = NewRevision.Description = RevDescription;
		
		now = datetime.now()
		str_format = "%d/%b/%y"
		Date = now.strftime(str_format).ToString()
		DateCapital = Date.upper()
		revDate = NewRevision.RevisionDate = DateCapital
		
		revId = NewRevision.GetGeneratingElementIds
		rev = NewRevision.Id
		
		revisions = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Revisions).WhereElementIsNotElementType().ToElements()
		
		#if isinstance(revisions, list):
		#	revs = []
		#	for i in revisions:
		#		revs.append(UnwrapElement(i))
		#else:
		#	revs = [UnwrapElement(revisions)]
		
		sheetscollector = FilteredElementCollector(uwdoc)
		sheetsEl = sheetscollector.OfCategory(BuiltInCategory.OST_Sheets).ToElements()
		
		for splashsheet in sheetsEl:
			if splashsheet.Name == "Splash Screen":
				splashscreen.append(splashsheet)
		
		TransactionManager.Instance.TransactionTaskDone()
		
		for i in splashscreen:
			revisionsOnSheet = i.GetAdditionalRevisionIds()
			for r in revisions:
				if r.Id not in revisionsOnSheet:
					revisionsOnSheet.Add(r.Id)
				else:
					continue
			TransactionManager.Instance.EnsureInTransaction(doc)
			i.SetAdditionalRevisionIds(revisionsOnSheet)
			TransactionManager.Instance.TransactionTaskDone()
			
	except:
		# if error accurs anywhere in the process catch it
		import traceback
		errorReport = traceback.format_exc()
else:
	errorReport = TaskDialog.Show("Darling-Flow","Revision not added. Please ensure Revisions are set to Numeric and Splash Screen exists.")


#Assign your output to the OUT variable
if errorReport == None:
	Message = 'Revision Added to Splash Screen', revDate,RevDescription
	MessageString = Message.ToString()
	OUT = TaskDialog.Show("Darling-Flow",MessageString)
	
	'Revision Added to Splash Screen', revDate, RevDescription
else:
	OUT = errorReport