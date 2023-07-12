import time
import wx


import scisuit.eng as eng
from scisuit.util import parent_path
from scisuit.wxpy import makeicon, NumTextCtrl





class frmPsychrometry ( wx.Frame ):

	def __init__( self, parent = None, FileMenu = None ):
		wx.Frame.__init__ ( self, 
                parent,  	
                title = u"Psychrometry", 
                style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.RESIZE_BORDER|wx.TAB_TRAVERSAL )

		self.m_Digits = 3 #show results with 3 decimal points

		IconPath = parent_path(__file__) / "icons" / "psychart.png"
		self.SetIcon(makeicon(IconPath))

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.Colour( 0, 242, 242 ) )

		self.m_chkP = wx.CheckBox( self, wx.ID_ANY, "P")
		self.m_chkP.SetToolTip( u"Pressure" )
		self.m_txtP = NumTextCtrl( self)
		self.m_txtP.SetToolTip( u"Pressure" )
		self.m_lblP = wx.StaticText( self, wx.ID_ANY, "kPa")
		self.m_lblP.Wrap( -1 )

		self.m_stxtPw = wx.StaticText( self, wx.ID_ANY, "Pw")
		self.m_stxtPw.Wrap( -1 )
		self.m_txtPw = wx.TextCtrl( self, style= wx.TE_READONLY )
		self.m_lblPw = wx.StaticText( self, wx.ID_ANY, "kPa")
		self.m_lblPw.Wrap( -1 )

		self.m_stxtPws = wx.StaticText( self, wx.ID_ANY, u"Pws")
		self.m_stxtPws.Wrap( -1 )
		self.m_txtPws = wx.TextCtrl( self, style= wx.TE_READONLY )
		self.m_lblPws = wx.StaticText( self, wx.ID_ANY, "kPa")
		self.m_lblPws.Wrap( -1 )

		self.m_chkTdb = wx.CheckBox( self, wx.ID_ANY, u"Tdb")
		self.m_chkTdb.SetToolTip( u"dry-bulb temperature" )
		self.m_txtTdb = NumTextCtrl( self)
		self.m_lblTdb = wx.StaticText( self, wx.ID_ANY, "°C")
		self.m_lblTdb.Wrap( -1 )

		self.m_chkTwb = wx.CheckBox( self, wx.ID_ANY, u"Twb")
		self.m_chkTwb.SetToolTip( u"wet-bulb temperature" )
		self.m_txtTwb = NumTextCtrl( self)
		self.m_lblTwb = wx.StaticText( self, wx.ID_ANY, "°C")
		self.m_lblTwb.Wrap( -1 )

		self.m_chkTdp = wx.CheckBox( self, wx.ID_ANY, u"Tdp")
		self.m_chkTdp.SetToolTip( u"dew-point temperature" )
		self.m_txtTdp = NumTextCtrl( self)
		self.m_lblTdp = wx.StaticText( self, wx.ID_ANY, "°C")
		self.m_lblTdp.Wrap( -1 )

		self.m_chkW = wx.CheckBox( self, wx.ID_ANY, "W")
		self.m_txtW = NumTextCtrl( self)	
		self.m_lblW = wx.StaticText( self, wx.ID_ANY, "kg/kgda")
		self.m_lblW.Wrap( -1 )

		self.m_stxtWs = wx.StaticText( self, wx.ID_ANY, "Ws")
		self.m_stxtWs.Wrap( -1 )	
		self.m_txtWs = wx.TextCtrl( self,style = wx.TE_READONLY )
		self.m_lblWs = wx.StaticText( self, wx.ID_ANY, "kg/kgda")
		self.m_lblWs.Wrap( -1 )	

		self.m_chkH = wx.CheckBox( self, wx.ID_ANY, "H")
		self.m_txtH =  NumTextCtrl( self)
		self.m_lblH = wx.StaticText( self, wx.ID_ANY, "kJ/kgda")
		self.m_lblH.Wrap( -1 )

		self.m_chkRH = wx.CheckBox( self, wx.ID_ANY, "RH")
		self.m_txtRH = NumTextCtrl( self)
		self.m_lblRH = wx.StaticText( self, wx.ID_ANY, "%")
		self.m_lblRH.Wrap( -1 )

		self.m_chkV = wx.CheckBox( self, wx.ID_ANY, "v")
		self.m_txtV = NumTextCtrl( self)
		self.m_lblV = wx.StaticText( self, wx.ID_ANY, "m3/kg")
		self.m_lblV.Wrap( -1 )

		fgSzr_L = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSzr_L.SetFlexibleDirection( wx.BOTH )
		fgSzr_L.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		fgSzr_L.Add( self.m_chkP, 0, wx.ALL, 5 )
		fgSzr_L.Add( self.m_txtP, 0, wx.ALL, 5 )
		fgSzr_L.Add( self.m_lblP, 0, wx.ALL, 5 )
		fgSzr_L.Add( self.m_stxtPw, 0, wx.ALL, 5 )
		fgSzr_L.Add( self.m_txtPw, 0, wx.ALL, 5 )
		fgSzr_L.Add( self.m_lblPw, 0, wx.ALL, 5 )
		fgSzr_L.Add( self.m_stxtPws, 0, wx.ALL, 5 )
		fgSzr_L.Add( self.m_txtPws, 0, wx.ALL, 5 )
		fgSzr_L.Add( self.m_lblPws, 0, wx.ALL, 5 )
		fgSzr_L.Add( self.m_chkTdb, 0, wx.ALL, 5 )
		fgSzr_L.Add( self.m_txtTdb, 0, wx.ALL, 5 )
		fgSzr_L.Add( self.m_lblTdb, 0, wx.ALL, 5 )
		fgSzr_L.Add( self.m_chkTwb, 0, wx.ALL, 5 )
		fgSzr_L.Add( self.m_txtTwb, 0, wx.ALL, 5 )
		fgSzr_L.Add( self.m_lblTwb, 0, wx.ALL, 5 )
		fgSzr_L.Add( self.m_chkTdp, 0, wx.ALL, 5 )
		fgSzr_L.Add( self.m_txtTdp, 0, wx.ALL, 5 )
		fgSzr_L.Add( self.m_lblTdp, 0, wx.ALL, 5 )

		fgSzr_R = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSzr_R.SetFlexibleDirection( wx.BOTH )
		fgSzr_R.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		fgSzr_R.Add( self.m_chkW, 0, wx.ALL, 5 )
		fgSzr_R.Add( self.m_txtW, 0, wx.ALL, 5 )
		fgSzr_R.Add( self.m_lblW, 0, wx.ALL, 5 )
		fgSzr_R.Add( self.m_stxtWs, 0, wx.ALL, 5 )
		fgSzr_R.Add( self.m_txtWs, 0, wx.ALL, 5 )
		fgSzr_R.Add( self.m_lblWs, 0, wx.ALL, 5 )
		fgSzr_R.Add( self.m_chkH, 0, wx.ALL, 5 )
		fgSzr_R.Add( self.m_txtH, 0, wx.ALL, 5 )
		fgSzr_R.Add( self.m_lblH, 0, wx.ALL, 5 )
		fgSzr_R.Add( self.m_chkRH, 0, wx.ALL, 5 )
		fgSzr_R.Add( self.m_txtRH, 0, wx.ALL, 5 )
		fgSzr_R.Add( self.m_lblRH, 0, wx.ALL, 5 )
		fgSzr_R.Add( self.m_chkV, 0, wx.ALL, 5 )
		fgSzr_R.Add( self.m_txtV, 0, wx.ALL, 5 )
		fgSzr_R.Add( self.m_lblV, 0, wx.ALL, 5 )

		szrLR = wx.BoxSizer( wx.HORIZONTAL )
		szrLR.Add( fgSzr_L, 1, wx.EXPAND, 5 )
		szrLR.Add( fgSzr_R, 1, wx.EXPAND, 5 )

		self.m_btnCalc = wx.Button( self, wx.ID_ANY, "Compute")
		self.m_btnCalc.Enabled=False
		
		mainSizer = wx.BoxSizer( wx.VERTICAL )
		mainSizer.Add( szrLR, 1, wx.EXPAND, 5 )
		mainSizer.Add( ( 0, 20), 0, wx.EXPAND, 5 )
		mainSizer.Add( self.m_btnCalc, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		if(FileMenu == None):
			self.m_menuFile = wx.Menu()
			self.m_menuCopyClipbrd = wx.MenuItem( self.m_menuFile, -1, "Copy to clipboard")
			self.m_menuFile.Append( self.m_menuCopyClipbrd )
			self.Bind( wx.EVT_MENU, self.__OnCopyClipbrd, id = self.m_menuCopyClipbrd.GetId() )
		else:
			assert isinstance(FileMenu, wx.Menu), "FileMenu must be of type wx.Menu"
			self.m_menuFile = FileMenu
		
		self.m_menuDigits = wx.Menu()	
		self.m_menuItem2Digits = wx.MenuItem( self.m_menuDigits, -1, "2 Digits","", wx.ITEM_RADIO)
		self.m_menuDigits.Append( self.m_menuItem2Digits )

		self.m_menuItem3Digits = wx.MenuItem( self.m_menuDigits, -1, "3 Digits", "", wx.ITEM_RADIO )
		self.m_menuDigits.Append( self.m_menuItem3Digits )
		self.m_menuItem3Digits.Check(True)

		self.m_menuItem4Digits = wx.MenuItem( self.m_menuDigits, -1, "4 Digits", "", wx.ITEM_RADIO )
		self.m_menuDigits.Append( self.m_menuItem4Digits )

		self.m_menubar = wx.MenuBar( 0 )
		self.m_menubar.Append( self.m_menuFile, "File" )
		self.m_menubar.Append( self.m_menuDigits, "Digits" )
		self.SetMenuBar( self.m_menubar )


		self.SetSizerAndFit( mainSizer )
		self.Layout()
		self.Centre( wx.BOTH )


		self.Bind( wx.EVT_CHECKBOX, self.__OnCheckBox )
		self.m_btnCalc.Bind( wx.EVT_BUTTON, self.__OnBtn )
		
		
		self.Bind( wx.EVT_MENU, self.__OnMenuDigits, id = self.m_menuItem2Digits.GetId() )
		self.Bind( wx.EVT_MENU, self.__OnMenuDigits, id = self.m_menuItem3Digits.GetId() )
		self.Bind( wx.EVT_MENU, self.__OnMenuDigits, id = self.m_menuItem4Digits.GetId() )


		self.m_CheckBoxes=[self.m_chkP, self.m_chkTdb, self.m_chkTwb, self.m_chkTdp, 
				self.m_chkW, self.m_chkH, self.m_chkRH, self.m_chkV]

		
		self.m_Controls=[
			[self.m_chkP, self.m_txtP, "kPa", "P"],
			[self.m_chkTdb, self.m_txtTdb, "°C", "Tdb"],
			[self.m_chkTwb, self.m_txtTwb, "°C", "Twb"],
			[self.m_chkTdp, self.m_txtTdp, "°C", "Tdp"],
			[self.m_chkW, self.m_txtW, "kg/kg da", "W"],
			[self.m_chkH, self.m_txtH, "kJ/kgda", "H"],
			[self.m_chkRH, self.m_txtRH, "%", "RH"],
			[self.m_chkV, self.m_txtV, "m3/kg", "V"],
			[None, self.m_txtPw, "kPa", "Pw"],
			[None, self.m_txtPws, "kPa", "Pws"],
			[None, self.m_txtWs, "kg/kgda", "Ws"]
		]

	
	
	def EnableAllCheckBoxes(self):
		for chkBox in self.m_CheckBoxes:
			chkBox.Enable(True)
    

	def DisableUncheckedBoxes(self):
		for chkBox in self.m_CheckBoxes:
			chkBox.Enabled = chkBox.GetValue()



	def __del__( self ):
		pass

    
	def __OnCheckBox( self, event ):
		NChkedBoxes = 0
	
		for chkBox in self.m_CheckBoxes:
			NChkedBoxes += int(chkBox.GetValue())

		if(NChkedBoxes >= 3):
			self.DisableUncheckedBoxes()
		else:
			self.EnableAllCheckBoxes()
		
		self.m_btnCalc.Enabled = (NChkedBoxes >= 3)
		
	

	def __OnCopyClipbrd( self, event ):
		strInput, strOutput = "", ""
		
		for Entry in self.m_Controls:
			if(Entry[0] and Entry[0].GetValue()):
				strInput += str(Entry[3]) + " = " + str(Entry[1].GetValue()) + " " + str(Entry[2]) + "\n"
			else:
				strOutput += str(Entry[3]) + " = " + str(Entry[1].GetValue()) + " " + str(Entry[2]) + "\n"			

		data = strInput + "\n" + strOutput
		if wx.TheClipboard.Open():
			wx.TheClipboard.SetData(wx.TextDataObject(data))
			wx.TheClipboard.Close()
			wx.TheClipboard.Flush()
		
			
	
	
	def __OnMenuDigits( self, event ): 
		id = event.GetId()
		if(id == self.m_menuItem2Digits.GetId()):
			self.m_Digits=2
		elif(id == self.m_menuItem3Digits.GetId()):
			self.m_Digits=3
		else:
			self.m_Digits=4



	def __OnBtn( self, event ):
		PsyParams = dict()
		try:
			"""
			Collect the check entries and values in a dictionary
			"""
			for Entry in self.m_Controls:
				if(Entry[0] and Entry[0].GetValue()):
					assert Entry[1].GetValue() !="", "A numeric value must be entered for " + Entry[3]  

					#note that we use NumTextCtrl so this will always succeed
					PsyParams[Entry[3]] = float(Entry[1].GetValue()) 
		
		
			result = eng.psychrometry(**PsyParams)

			for Entry in self.m_Controls:
				value = getattr(result, Entry[3])
				value = round(value, self.m_Digits)
				Entry[1].SetValue(str(value))

		except Exception as e:
			wx.MessageBox(str(e))