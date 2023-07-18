import sqlite3 as _sql

from ...util import parent_path as _parent_path
from ... import linearinterp as _linearinterp


__all__ = ['ThermoPhysical', 'SaturatedRefrigerant', 'SuperHeatedRefrigerant']


"""
This module depends on existence of the two databases: refrigerants.db and thermophysical.db

Properties are searched in the above-mentioned respective database, bracketed and then 
the intended value is computed using linear-interpolation(s).
"""



class Refrigerant():
	"""
	Base class for thermodynamic properties of refrigerants
	"""
	s_DataBasePath = _parent_path(__file__) / "refrigerants.db"
	
	def __init__(self) -> None: 
		self.m_Connection = _sql.connect(self.s_DataBasePath) 

		#-1:Compressed, 0:saturated, 1:superheated
		self.m_FluidState = None

		self.m_DBTable = None

	
	def __del__( self ):
		self.m_Connection.close()
	

	def Init(self, FluidName:str)->None:
		self.m_FluidName = FluidName
		cursor = self.m_Connection.cursor()

		"""
		Check if the parameter FluidName is valid
		Note that the columns in the database is configured as
		COLLATE NOCASE, therefore search is not case-sensitive
		"""
		QueryString = "SELECT * FROM MAINTABLE where NAME=?"
		rows = cursor.execute(QueryString , (FluidName,)).fetchall()

		#a name like "R" or "R1" will match more than 1
		if(len(rows)>1):
			raise ValueError("More than 1 fluid matched the name:" + FluidName)

		DBTableColPos = 2 #saturated, compressed
		if(self.m_FluidState == 1):
			DBTableColPos = 3
		
		if(len(rows) == 0):
			QueryString = "SELECT * FROM MAINTABLE where ALTERNATIVE=?"
			rows = cursor.execute(QueryString , (FluidName,)).fetchall()

			#all options exhausted, raise an error
			if(len(rows)==0):
				raise ValueError(FluidName + " did not match any")
            
			self.m_DBTable = rows[0][DBTableColPos]
        
		#len(rows) ==1
		else:
			self.m_DBTable = rows[0][DBTableColPos]



	def GetFluidNames(self):
		QueryString = "SELECT name, alternative FROM MAINTABLE"
		rowList = self.m_Connection.cursor().execute(QueryString , []).fetchall()
		
		return rowList
    



class SaturatedRefrigerant(Refrigerant):

	def __init__(self, FluidName:str) -> None:
		"""
		FluidName: Name of the fluid
		"""
		super().__init__() 

		self.m_FluidState = 0
		super().Init(FluidName)
		

	def search(self, PropertyName:str, QueryValue:float, Sort = True): 
		return _searchOrderedTable(self.m_Connection, self.m_DBTable, PropertyName, QueryValue, Sort) 



class SuperHeatedRefrigerant(Refrigerant):

	def __init__(self, FluidName:str) -> None:
		"""
		FluidName: Name of the fluid
		"""
		super().__init__() 

		self.m_FluidState = 1 
		super().Init(FluidName)
	

	def _BracketPressure(self, P:float):
		cursor = self.m_Connection.cursor()

		QueryString = "SELECT min(P), max(P) FROM " + self.m_DBTable
		MinMax = cursor.execute(QueryString , []).fetchall()
		Pmin, Pmax = MinMax[0][0], MinMax[0][1]

		if(not (Pmin<P and P<Pmax)):
			raise ValueError("Pressure range: ["+ str(Pmin) + ", " + str(Pmax) + "]" )
		
		#Pressure is within limits, but where?
		strQuery="SELECT DISTINCT P FROM " + self.m_DBTable + " WHERE P<="+str(P) +" ORDER BY P DESC LIMIT 1"
		row = cursor.execute(strQuery , []).fetchall()
		PL =row[0][0]
		
		strQuery="SELECT DISTINCT P FROM " + self.m_DBTable + " WHERE P>="+ str(P) +" LIMIT 1"
		row = cursor.execute(strQuery , []).fetchall()
		PH =row[0][0]
		
		return PL, PH

	
	def _BracketProperty(self, P:float, Name:str , Value:float):
		"""
		given a pressure value, finds lower and upper range of property
		"""

		cursor = self.m_Connection.cursor()
		
		QueryString = "SELECT min("+ Name +"), max(" + Name +") FROM " + self.m_DBTable + " WHERE P=?"
		MinMax = cursor.execute(QueryString , [P]).fetchall()
		PropertyMin, PropertyMax = MinMax[0][0], MinMax[0][1]

		if(not (PropertyMin < Value and Value < PropertyMax)):
			raise ValueError("At P="+ str(P) + " kPa, " + Name + " has range: ["+ str(PropertyMin) + ", " + str(PropertyMax) + "]" )
		
		"""
		Assumption is made that at a given pressure the property values
		are monotonically increasing (which is the case for T, V, H, S)
		"""
 
		strQuery="SELECT "+ Name +" FROM "+ self.m_DBTable + " WHERE P=? AND " + Name + "<=? ORDER BY " + Name + " DESC LIMIT 1"
		row = cursor.execute(strQuery , [P,Value]).fetchall()
		LowerRange =row[0][0]

		strQuery="SELECT " + Name +" FROM "+ self.m_DBTable + " WHERE P=? AND "+ Name +">=? LIMIT 1"
		row = cursor.execute(strQuery , [P, Value]).fetchall()
		UpperRange = row[0][0]

		return LowerRange, UpperRange


	def _FindProperties(self, P: float, Name:str , Value:float):
		"""
		Given a pressure value and a property, i.e. temperature
		the function returns the properties at the given pressure and temperature
		
		Note that the pressure here is the lower or upper value of the bracketed pressure
		and NOT the exact pressure value requested by user
		
		Therefore for any search this function needs to be called twice: at lower and upper ranges of pressure
		"""
		cursor = self.m_Connection.cursor()

		PropLow, PropHigh = self._BracketProperty(P, Name, Value)

		AllFieldNames:list = _GetFieldNames(self.m_Connection, self.m_DBTable)
		AllFieldNames.remove("P") #P is always known
		AllFieldNames.remove(Name.capitalize()) #property is known as well

		#As of this point AllFieldNames contains only the properties' names we are after
		JoinedFieldNames = ",".join(AllFieldNames)

		#Find properties at Pressure and lower range of the property 
		strQuery="SELECT " + JoinedFieldNames +" FROM "+ self.m_DBTable + " WHERE P=? AND "+ Name +"=?"
		
		"""
		Database table contains only fields of P, T, V, H, S
		Therefore once two properties are known, i.e., P and T,
		there remains 3 properties which are named arbitrarily as A, B, C
		"""
		
		row = cursor.execute(strQuery , [P, PropLow]).fetchall()
		Alow, Blow, Clow =row[0][0], row[0][1], row[0][2]

		#Find properties at lPressure and Upper range of the property 
		row = cursor.execute(strQuery , [P, PropHigh]).fetchall()
		Aup, Bup, Cup =row[0][0], row[0][1], row[0][2]

		A = _linearinterp(PropLow, Alow, PropHigh, Aup, Value)
		B = _linearinterp(PropLow, Blow, PropHigh, Bup, Value)
		C = _linearinterp(PropLow, Clow, PropHigh, Cup, Value)

		return A, B, C


	def search_PT(self, P:float, T:float):
		"""
		search for the values at a given pressure (kPa) and temperature (celcius)
		"""
		cursor = self.m_Connection.cursor()

		PL, PH = self._BracketPressure(P)

		Vlow, Hlow, Slow = self._FindProperties(PL, "T", T)
		Vup, Hup, Sup = self._FindProperties(PH, "T", T)

		V = _linearinterp(PL, Vlow, PH, Vup, P)
		H = _linearinterp(PL, Hlow, PH, Hup, P)
		S = _linearinterp(PL, Slow, PH, Sup, P)
		
		

		return {'V':V, 'H':H, 'S': S}
		
		
	def search_PV(self, P:float, V:float):
		"""
		search for the values at a given pressure (kPa) and specific volume (m3/kg)
		"""
		cursor = self.m_Connection.cursor()

		PL, PH = self._BracketPressure(P)

		Tlow, Hlow, Slow = self._FindProperties(PL, "V", V)
		Tup, Hup, Sup = self._FindProperties(PH, "V", V)

		T = _linearinterp(PL, Tlow, PH, Tup, P)
		H = _linearinterp(PL, Hlow, PH, Hup, P)
		S = _linearinterp(PL, Slow, PH, Sup, P)

		return {'T':T, 'H':H, 'S':S}
		
	
	def search_PH(self, P:float, H:float):
		"""
		search for the values at a given pressure (kPa) and enthalpy (kJ/kg)
		"""
		cursor = self.m_Connection.cursor()

		PL, PH = self._BracketPressure(P)

		Tlow, Vlow, Slow = self._FindProperties(PL, "H", H)
		Tup, Vup, Sup = self._FindProperties(PH, "H", H)

		T = _linearinterp(PL, Tlow, PH, Tup, P)
		V = _linearinterp(PL, Vlow, PH,Vup, P)
		S = _linearinterp(PL, Slow, PH, Sup, P)

		return {'T':T, 'V':V, 'S':S}
	
	
	def search_PS(self, P:float, S:float):
		"""
		search for the values at a given pressure (kPa) and entropy (kJ/kgK)
		"""
		cursor = self.m_Connection.cursor()

		PL, PH = self._BracketPressure(P)

		Tlow, Vlow, Hlow = self._FindProperties(PL, "S",S)
		Tup, Vup, Hup = self._FindProperties(PH, "S", S)

		T = _linearinterp(PL, Tlow, PH, Tup, P)
		V = _linearinterp(PL, Vlow, PH,Vup, P)
		H = _linearinterp(PL, Hlow, PH, Hup, P)

		return {'T':T, 'V':V, 'H':H} 
		
	
	def search(self, P:float, name:str, value:float):
		CapName = name.upper()
		if(CapName == "T"):
			return self.search_PT(P, value)
		
		elif (CapName =="V"):
			return self.search_PV(P, value)
		
		elif(CapName == "H"):
			return self.search_PH(P, value)
		
		elif(CapName == "S"):
			return self.search_PS(P, value)
		
		else:
			raise ValueError("name must be T, V, H or S")
		


class ThermoPhysical():  
	"""
	Thermo-physical properties (T, rho, cp, viscosity, k, Pr) of fluids
	"""
	s_DataBasePath = _parent_path(__file__) / "thermophysical.db"
	
	def __init__(self, FluidName:str ) -> None:
		"""
		FluidName: Name of the fluid
		"""

		self.m_Connection = _sql.connect(self.s_DataBasePath) 
		
		if(FluidName ==""):
			return
		
		self.m_FluidName = FluidName
		cursor = self.m_Connection.cursor()

		"""
		Check if the parameter FluidName is valid
		Note that the columns in the database is configured as
		COLLATE NOCASE, therefore search is not case-sensitive
		"""
		QueryString = "SELECT NAME FROM MAINTABLE where NAME=?"
		rows = cursor.execute(QueryString , (FluidName,)).fetchall()

		#more than 1 name matches
		if(len(rows)>1):
			raise ValueError("More than 1 fluid matched the name:" + FluidName)

		self.m_DBTable = rows[0][0]


	def __del__( self ):
		self.m_Connection.close()
	
	
	def GetFluidNames(self):
		QueryString = "SELECT name FROM MAINTABLE"
		FluidNameList = self.m_Connection.cursor().execute(QueryString , []).fetchall()
		
		return FluidNameList


	def search(self, PropertyName:str, QueryValue:float, Sort:bool = True): 
		return _searchOrderedTable(self.m_Connection, self.m_DBTable, PropertyName, QueryValue, Sort) 



def _GetFieldNames(connection, TableName: str)->list:
		"""
		Given a TableName returns all fieldnames (properties) of the table
		"""
		QueryString = "SELECT name FROM PRAGMA_TABLE_INFO(?)"
		rowList = connection.cursor().execute(QueryString , (TableName,)).fetchall()

		if(len(rowList) == 0):
			raise ValueError("Invalid table name:" + TableName)

		retList = []
		for tupleItem in rowList:
			retList.append(tupleItem[0])

		return retList

	



def _searchOrderedTable(connection, TableName:str, PropertyName:str, QueryValue:float, Sort:bool = True)->dict:
	"""
	## Input:
	TableName: Database table name where uniquely named properties are \n
	PropertyName: Name of the property corresponding to fieldname in the table \n
	QueryValue: Value at which properties are sought after \n
	Sort: Sort the table based on the property name in ascending order \n
	(if multiple queries are performed on the same property, set Sort to False for efficiency )\n \n

	--Table must be in the form of, for example \n
	P	T	s	vf \n
	50	20	2	0.2 \n
	70	25	3	0.8 \n
	
	if we are after properties at T=22, then returns a dict with keys P, s corresponding to T=22`
	"""
	cursor = connection.cursor() 
	AllFieldNames = _GetFieldNames(connection, TableName)

	#Index of the property in the columns of the table
	ParamIndex = -1
	try:
		"""
			note that we search in capitalized field names with capitalized PropertyName
			For example, user now can enter Pr, pr ... to find properties for Prandtl
			The table must contain only unique fields
		"""
		CapitalizedFiledNames = [s.capitalize() for s in AllFieldNames]
		ParamIndex = CapitalizedFiledNames.index(PropertyName.capitalize())
	except:
		raise ValueError("Valid property names: " + str(AllFieldNames))
	

	#Check if QueryValue is within the bounds of the property
	strQuery="SELECT min( {} ), max( {} ) FROM " + TableName 
	rows = cursor.execute(strQuery.format(PropertyName, PropertyName)).fetchone()
	MinVal, MaxVal = rows[0],  rows[1]
	if(not (MinVal<QueryValue and QueryValue<MaxVal)):
		raise ValueError(PropertyName + " range: [" + str(rows[0]) + " , " + str(rows[1]) + "]")

	_rows = None

	if(Sort):
		strQuery = "SELECT * FROM " + TableName + " ORDER BY "+ PropertyName
		_rows = cursor.execute(strQuery , []).fetchall()
	

	RowIndex = -1
	for i in range(len(_rows)):
		Value = _rows[i][ParamIndex]
		if(Value>=QueryValue):
			RowIndex = i
			break
	
	
	retDict = dict()
	if(RowIndex == 0):
		TupleIndex = -1
		for propName in AllFieldNames:
			TupleIndex += 1
			if(propName == PropertyName):
				continue

			Value = _rows[0][TupleIndex]
			retDict[propName] = Value

		return retDict
			
		

	PropValHigh = _rows[RowIndex][ParamIndex]
	PropValLow = _rows[RowIndex - 1][ParamIndex] 
	TupleIndex = -1

	for propName in AllFieldNames: 
		TupleIndex += 1
		
		if(propName.capitalize() == PropertyName.capitalize()):
			continue 

		ValueLow = _rows[RowIndex - 1][TupleIndex]
		ValueHigh = _rows[RowIndex][TupleIndex]
		Value = _linearinterp(PropValLow, ValueLow, PropValHigh, ValueHigh, QueryValue)
		retDict[propName] = Value
		
	return retDict
