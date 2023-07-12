import wx

from ..util import parent_path as _parent_path
from ..wxpy import NumTextCtrl, makeicon
from ..eng.fluids_dbase import Refrigerant, SaturatedRefrigerant, SuperHeatedRefrigerant, ThermoPhysical


class pnlRefrigerantSaturated ( wx.Panel ):

	def __init__( self, parent):
		wx.Panel.__init__ ( self, parent )

		self.m_txtBGChanged  = None
		self.m_FluidType = None
		self.m_SelectedProperty = None
		self.m_Parent = parent.GetParent()

		self.m_stFluidType = wx.StaticText( self, wx.ID_ANY, u"Type: ")
		self.m_stFluidType.Wrap( -1 )

		self.m_choiceFluidType = wx.Choice( self, choices = [])
		self.m_choiceFluidType.SetSelection( 0 )

		self.m_radioT = wx.RadioButton( self, label = u"T (°C)")
		self.m_txtT = NumTextCtrl( self)
		self.m_radioP = wx.RadioButton( self, label = u"P (kPa)")
		self.m_txtP = NumTextCtrl( self)
		self.m_radioVf = wx.RadioButton( self, label = u"vf (m\u00B3/kg)")
		self.m_txtVf = NumTextCtrl( self)
		self.m_radioVg = wx.RadioButton( self, label = u"vg (m\u00B3/kg)")
		self.m_txtVg = NumTextCtrl( self)
		self.m_radioHf = wx.RadioButton( self, label = u"hf (kJ/kg)")
		self.m_txtHf = NumTextCtrl( self)
		self.m_radioHg = wx.RadioButton( self, label = u"hg (kJ/kg)")
		self.m_txtHg = NumTextCtrl( self)
		self.m_radioSf = wx.RadioButton( self, label = u"sf (kJ/kg\u00B7K)")
		self.m_txtSf = NumTextCtrl( self)
		self.m_radioSg = wx.RadioButton( self, label = u"sg (kJ/kg\u00B7K)")
		self.m_txtSg = NumTextCtrl( self)

		sizerFluidType = wx.BoxSizer( wx.HORIZONTAL )
		sizerFluidType.Add( self.m_stFluidType, 0, wx.ALL, 5 )
		sizerFluidType.Add( self.m_choiceFluidType, 1, wx.ALL, 5 )

		fgSzr = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSzr.AddGrowableCol( 1 )
		fgSzr.SetFlexibleDirection( wx.BOTH )
		fgSzr.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		fgSzr.Add( self.m_radioT, 0, wx.ALL, 5 )
		fgSzr.Add( self.m_txtT, 0, wx.ALL|wx.EXPAND, 5 )
		fgSzr.Add( self.m_radioP, 0, wx.ALL, 5 )
		fgSzr.Add( self.m_txtP, 0, wx.ALL|wx.EXPAND, 5 )
		fgSzr.Add( self.m_radioVf, 0, wx.ALL, 5 )
		fgSzr.Add( self.m_txtVf, 0, wx.ALL|wx.EXPAND, 5 )
		fgSzr.Add( self.m_radioVg, 0, wx.ALL, 5 )
		fgSzr.Add( self.m_txtVg, 0, wx.ALL|wx.EXPAND, 5 )
		fgSzr.Add( self.m_radioHf, 0, wx.ALL, 5 )
		fgSzr.Add( self.m_txtHf, 0, wx.ALL|wx.EXPAND, 5 )
		fgSzr.Add( self.m_radioHg, 0, wx.ALL, 5 )
		fgSzr.Add( self.m_txtHg, 0, wx.ALL|wx.EXPAND, 5 )
		fgSzr.Add( self.m_radioSf, 0, wx.ALL, 5 )
		fgSzr.Add( self.m_txtSf, 0, wx.ALL|wx.EXPAND, 5 )
		fgSzr.Add( self.m_radioSg, 0, wx.ALL, 5 )
		fgSzr.Add( self.m_txtSg, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_btnCompute = wx.Button( self, wx.ID_ANY, u"Compute")

		mainSizer = wx.BoxSizer( wx.VERTICAL )
		mainSizer.Add( sizerFluidType, 1, wx.EXPAND, 5 )
		mainSizer.Add( ( 0, 10), 1, wx.EXPAND, 5 )
		mainSizer.Add( fgSzr, 0, wx.EXPAND, 5 )
		mainSizer.Add( ( 0, 10), 1, wx.EXPAND, 5 )
		mainSizer.Add( self.m_btnCompute, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.SetSizerAndFit( mainSizer )
		self.Layout()

		self.m_CtrlList = [[self.m_radioT, self.m_txtT, "T"], [self.m_radioP, self.m_txtP, "P"], 
            [self.m_radioVf, self.m_txtVf, "vf"], [self.m_radioVg, self.m_txtVg, "vg"],
            [self.m_radioHf, self.m_txtHf, "hf"], [self.m_radioHg, self.m_txtHg, "hg"],
            [self.m_radioSf, self.m_txtSf, "sf"], [self.m_radioSg, self.m_txtSg, "sg"]]


		self.Bind( wx.EVT_INIT_DIALOG, self.__OnInitDialog )
		self.Bind( wx.EVT_RADIOBUTTON, self.__OnRadioButton )

		self.m_choiceFluidType.Bind( wx.EVT_CHOICE, self.__OnChoice )	
		self.m_btnCompute.Bind( wx.EVT_BUTTON, self.__OnComputeBtn )


	def __del__( self ):
		pass


	def __ChangeBGColor(self, txtCtrl):
		BGColor = wx.Colour(144,238,144)
		if(self.m_txtBGChanged != None):
			self.m_txtBGChanged.SetBackgroundColour(wx.Colour(255, 255, 255)) 
			self.m_txtBGChanged.Refresh()
		
		txtCtrl.SetBackgroundColour(BGColor)
		txtCtrl.Refresh()
		self.m_txtBGChanged = txtCtrl


	def __OnInitDialog( self, event ):
		refrigerant = Refrigerant()
		self.m_FluidList = refrigerant.GetFluidNames()
	
		for entry in self.m_FluidList:
			Name = str(entry[0])
			Alternative = str(entry[1])
			if(len(Alternative)>7):
				Alternative = Alternative[0:int(len(Alternative)/2)] + "..." + Alternative[-int(len(Alternative)/4):]
			
			self.m_choiceFluidType.Append(Name +", "+ Alternative)
		event.Skip()



	def __OnChoice( self, event ):
		sel = event.GetSelection()
		self.m_FluidType = self.m_FluidList[sel][0] #name
		event.Skip()



	def __OnRadioButton( self, event ):
		for lst in self.m_CtrlList:
			if(event.GetEventObject() == lst[0]):
				self.__ChangeBGColor(lst[1])
				self.m_SelectedProperty = lst[2]



	def __OnComputeBtn( self, event ):
		try:
			assert self.m_FluidType != None, "Fluid type must be selected"
			assert self.m_SelectedProperty != None, "A property must be selected"
			assert self.m_txtBGChanged.GetValue() != "", "A value must be entered for " + self.m_SelectedProperty
			
			fl = SaturatedRefrigerant(self.m_FluidType ) 
			result = fl.search(self.m_SelectedProperty, float(self.m_txtBGChanged.GetValue()))	
				
			for lst in self.m_CtrlList:
				if lst[1] == self.m_txtBGChanged: continue

				Value = result.get(lst[2])
				Digits = self.m_Parent.GetDigits() 
				lst[1].SetValue(str(round(Value, Digits)) if Digits!=None else str(Value))
		
		except Exception as e:
			wx.MessageBox(str(e))
	
	


	def Export(self):
		s = str(self.m_SelectedProperty) + "=" + str(self.m_txtBGChanged.GetValue()) + "\n"
		
		for lst in self.m_CtrlList: 
			if lst[1] == self.m_txtBGChanged:
				continue
			s += str(lst[2]) + "=" + str(lst[1].GetValue()) + "\n"
		
		if wx.TheClipboard.Open():
			wx.TheClipboard.SetData(wx.TextDataObject(s))
			wx.TheClipboard.Close()
			wx.TheClipboard.Flush()





class pnlRefrigerantSuperheated ( wx.Panel ):

	def __init__( self, parent):
		wx.Panel.__init__ ( self, parent)
		
		self.m_FluidType = None
		self.m_Parent = parent.GetParent()
		self.m_NCheckedBoxes = 1 # pressure already checked

		self.m_staticFluidType = wx.StaticText( self, wx.ID_ANY, u"Type: ")
		self.m_staticFluidType.Wrap( -1 )
		self.m_choiceFluidType = wx.Choice( self, choices = [] )
		self.m_choiceFluidType.SetSelection( 0 )

		self.m_chkT = wx.CheckBox( self, wx.ID_ANY, u"T (°C)" )
		self.m_txtT = NumTextCtrl( self)
		self.m_chkP = wx.CheckBox( self, wx.ID_ANY, u"P (kPa)")
		self.m_chkP.SetValue(True)
		self.m_chkP.Enable( False )
		self.m_txtP = NumTextCtrl( self)
		self.m_txtP.SetBackgroundColour(wx.Colour(144,238,144))
		self.m_chkV = wx.CheckBox( self, wx.ID_ANY, u"v (m\u00B3/kg)")
		self.m_txtV = NumTextCtrl( self)
		self.m_chkH = wx.CheckBox( self, wx.ID_ANY, u"h (kJ/kg)")
		self.m_txtH = NumTextCtrl( self)
		self.m_chkS = wx.CheckBox( self, wx.ID_ANY, u"s (kJ/kg\u00B7K)")
		self.m_txtS = NumTextCtrl( self)

		sizerFluidType = wx.BoxSizer( wx.HORIZONTAL )
		sizerFluidType.Add( self.m_staticFluidType, 0, wx.ALL, 5 )
		sizerFluidType.Add( self.m_choiceFluidType, 1, wx.ALL, 5 )

		fgSzr= wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSzr.AddGrowableCol( 1 )
		fgSzr.SetFlexibleDirection( wx.BOTH )
		fgSzr.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		fgSzr.Add( self.m_chkT, 0, wx.ALL, 5 )
		fgSzr.Add( self.m_txtT, 0, wx.ALL|wx.EXPAND, 5 )
		fgSzr.Add( self.m_chkP, 0, wx.ALL, 5 )
		fgSzr.Add( self.m_txtP, 0, wx.ALL|wx.EXPAND, 5 )
		fgSzr.Add( self.m_chkV, 0, wx.ALL, 5 )
		fgSzr.Add( self.m_txtV, 0, wx.ALL|wx.EXPAND, 5 )
		fgSzr.Add( self.m_chkH, 0, wx.ALL, 5 )
		fgSzr.Add( self.m_txtH, 0, wx.ALL|wx.EXPAND, 5 )
		fgSzr.Add( self.m_chkS, 0, wx.ALL, 5 )
		fgSzr.Add( self.m_txtS, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_btnCompute = wx.Button( self, wx.ID_ANY, u"Compute" )

		mainSizer = wx.BoxSizer( wx.VERTICAL )
		mainSizer.Add( sizerFluidType, 1, wx.EXPAND, 5 )
		mainSizer.Add( ( 0, 10), 1, wx.EXPAND, 5 )
		mainSizer.Add( fgSzr, 0, wx.EXPAND, 5 )
		mainSizer.Add( ( 0, 10), 1, wx.EXPAND, 5 )
		mainSizer.Add( self.m_btnCompute, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		self.SetSizerAndFit( mainSizer )
		self.Layout()
		
		self.m_CtrlList = [
		[self.m_chkT, self.m_txtT,  "T"], 
		[self.m_chkV, self.m_txtV, "v"],
		[self.m_chkH, self.m_txtH, "h"],
		[self.m_chkS, self.m_txtS, "s"]]

		self.Bind( wx.EVT_INIT_DIALOG, self.__OnInitDialog )
		self.m_choiceFluidType.Bind( wx.EVT_CHOICE, self.FluidType_OnChoice )
		self.m_chkT.Bind( wx.EVT_CHECKBOX, self.chkT_OnCheckBox )
		self.m_chkV.Bind( wx.EVT_CHECKBOX, self.chkV_OnCheckBox )
		self.m_chkH.Bind( wx.EVT_CHECKBOX, self.chkH_OnCheckBox )
		self.m_chkS.Bind( wx.EVT_CHECKBOX, self.chkS_OnCheckBox )
		self.m_btnCompute.Bind( wx.EVT_BUTTON, self.btnCompute_OnButtonClick )

	def __del__( self ):
		pass


	def EnableDisable(self, chkCtrl):
		BGColor = wx.Colour(144,238,144)
		White = wx.Colour(255, 255, 255)
		LRed = wx.Colour(255,204,204) #light red
		self.m_NCheckedBoxes += (1 if chkCtrl.GetValue() else -1)
			
		for Ctrls in self.m_CtrlList:
			cond = self.m_NCheckedBoxes == 2
			if(Ctrls[0] == chkCtrl):
				Ctrls[1].SetBackgroundColour(BGColor if cond else White) 
				Ctrls[1].Refresh()
				continue

			Ctrls[1].SetBackgroundColour(LRed if cond else White) 
			Ctrls[0].Enable(not cond)
			Ctrls[1].Refresh()

	
	def __OnInitDialog( self, event ):
		refrigerant = Refrigerant()
		self.m_FluidList = refrigerant.GetFluidNames()
	
		for entry in self.m_FluidList:
			Name = str(entry[0])
			Alternative = str(entry[1])
			if(len(Alternative)>7):
				Alternative = Alternative[0:int(len(Alternative)/2)] + "..." + Alternative[-int(len(Alternative)/4):]
			
			self.m_choiceFluidType.Append(Name +", "+ Alternative)
		event.Skip()
		

	def FluidType_OnChoice( self, event ):
		sel = event.GetSelection()
		self.m_FluidType = self.m_FluidList[sel][0] #name
		event.Skip()

	def chkT_OnCheckBox( self, event ):
		self.EnableDisable(self.m_chkT)
		event.Skip()

	def chkV_OnCheckBox( self, event ):
		self.EnableDisable(self.m_chkV)
		event.Skip()

	def chkH_OnCheckBox( self, event ):
		self.EnableDisable(self.m_chkH)
		event.Skip()

	def chkS_OnCheckBox( self, event ):
		self.EnableDisable(self.m_chkS)
		event.Skip()

	def btnCompute_OnButtonClick( self, event ):
		if self.m_FluidType == None:
			wx.MessageBox("Fluid type must be selected")
			return
		
		if self.m_NCheckedBoxes ==1:
			wx.MessageBox("Exactly two properties must be selected")
			return
		
		if(self.m_txtP.GetValue() == wx.EmptyString):
			wx.MessageBox("A value must be entered for pressure")
			return
		
		SelectedProp:str = ""
		InputVal = ""
		for lst in self.m_CtrlList:
			if lst[0].GetValue() == True:
				SelectedProp = lst[2].upper()
				InputVal = lst[1].GetValue()
		
		if(InputVal == ""):
			wx.MessageBox("A value must be entered for " + SelectedProp)
			return
				
		fl = SuperHeatedRefrigerant(self.m_FluidType ) 
		
		result = dict()
		try:
			result = fl.search(float(self.m_txtP.GetValue()), SelectedProp, float(InputVal))
		except Exception as e:
			wx.MessageBox(str(e))
			return
		
		
		Digits = self.m_Parent.GetDigits()
		
		for Ctrl in  self.m_CtrlList:
			Value = result.get(Ctrl[2].capitalize())
			if(Value == None):
				continue
				
			if(Digits != None):
				Ctrl[1].SetValue(str(round(Value, Digits )))
			else:
				Ctrl[1].SetValue(str(Value))
		
		event.Skip()
	

	def Export(self):
		s = "P=" + str(self.m_txtP.GetValue()) + "\n"

		for lst in self.m_CtrlList: 
			if lst[0].GetValue():
				s += str(lst[2]) + "=" + str(lst[1].GetValue()) + "\n"
				break
		
		for lst in self.m_CtrlList: 
			if lst[0].GetValue():
				continue
			s += str(lst[2]) + "=" + str(lst[1].GetValue()) + "\n"
		
		if wx.TheClipboard.Open():
			wx.TheClipboard.SetData(wx.TextDataObject(s))
			wx.TheClipboard.Close()
			wx.TheClipboard.Flush()





class pnlThermoPhysical ( wx.Panel ):

	def __init__( self, parent):
		wx.Panel.__init__ ( self, parent)
		
		self.m_txtBGChanged  = None
		self.m_FluidType = None
		self.m_SelectedProperty = None
		self.m_Parent = parent.GetParent()

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		sizerFluidType = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticFluidType = wx.StaticText( self, wx.ID_ANY, u"Type: ")
		self.m_staticFluidType.Wrap( -1 )

		sizerFluidType.Add( self.m_staticFluidType, 0, wx.ALL, 5 )

		m_choiceFluidTypeChoices = []
		self.m_choiceFluidType = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choiceFluidTypeChoices, 0 )
		self.m_choiceFluidType.SetSelection( 0 )
		sizerFluidType.Add( self.m_choiceFluidType, 1, wx.ALL, 5 )


		mainSizer.Add( sizerFluidType, 1, wx.EXPAND, 5 )


		mainSizer.Add( ( 0, 10), 1, wx.EXPAND, 5 )

		fgSizerLeft = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizerLeft.AddGrowableCol( 1 )
		fgSizerLeft.SetFlexibleDirection( wx.BOTH )
		fgSizerLeft.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_radioT = wx.RadioButton( self, wx.ID_ANY, u"T (°C)")
		fgSizerLeft.Add( self.m_radioT, 0, wx.ALL, 5 )

		self.m_txtT = NumTextCtrl( self)
		fgSizerLeft.Add( self.m_txtT, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radioRho = wx.RadioButton( self, wx.ID_ANY, u"Density (kg/m\u00B3)")
		fgSizerLeft.Add( self.m_radioRho, 0, wx.ALL, 5 )

		self.m_txtRho = NumTextCtrl( self)
		fgSizerLeft.Add( self.m_txtRho, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radioCp = wx.RadioButton( self, wx.ID_ANY, u"Cp (kJ/kgK)")
		fgSizerLeft.Add( self.m_radioCp, 0, wx.ALL, 5 )

		self.m_txtCp = NumTextCtrl( self)
		fgSizerLeft.Add( self.m_txtCp, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radioK = wx.RadioButton( self, wx.ID_ANY, u"k (W/mK)")
		fgSizerLeft.Add( self.m_radioK, 0, wx.ALL, 5 )

		self.m_txtK = NumTextCtrl( self)
		fgSizerLeft.Add( self.m_txtK, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radioMu = wx.RadioButton( self, wx.ID_ANY, u"Viscosity (Pa s)")
		fgSizerLeft.Add( self.m_radioMu, 0, wx.ALL, 5 )

		self.m_txtMu = NumTextCtrl( self)
		fgSizerLeft.Add( self.m_txtMu, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_radioPr = wx.RadioButton( self, wx.ID_ANY, u"Pr")
		fgSizerLeft.Add( self.m_radioPr, 0, wx.ALL, 5 )

		self.m_txtPr = NumTextCtrl( self)
		fgSizerLeft.Add( self.m_txtPr, 0, wx.ALL|wx.EXPAND, 5 )


		mainSizer.Add( fgSizerLeft, 0, wx.EXPAND, 5 )
		mainSizer.Add( ( 0, 10), 1, wx.EXPAND, 5 )

		self.m_btnCompute = wx.Button( self, wx.ID_ANY, u"Compute")
		mainSizer.Add( self.m_btnCompute, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		self.SetSizerAndFit( mainSizer )
		self.Layout()
		
		self.m_CtrlList = [[self.m_txtT, "T"], [self.m_txtRho, "rho"], 
            [self.m_txtCp, "cp"], [self.m_txtMu, "mu"],
            [self.m_txtK, "k"], [self.m_txtPr, "Pr"]]

		self.Bind( wx.EVT_INIT_DIALOG, self.OnInitDialog )
		self.m_choiceFluidType.Bind( wx.EVT_CHOICE, self.FluidType_OnChoice )
		self.m_radioT.Bind( wx.EVT_RADIOBUTTON, self.radioT_OnRadioButton )
		self.m_radioRho.Bind( wx.EVT_RADIOBUTTON, self.radioRho_OnRadioButton )
		self.m_radioCp.Bind( wx.EVT_RADIOBUTTON, self.radioCp_OnRadioButton )
		self.m_radioK.Bind( wx.EVT_RADIOBUTTON, self.radioK_OnRadioButton )
		self.m_radioMu.Bind( wx.EVT_RADIOBUTTON, self.radioMu_OnRadioButton )
		self.m_radioPr.Bind( wx.EVT_RADIOBUTTON, self.radioPr_OnRadioButton )
		self.m_btnCompute.Bind( wx.EVT_BUTTON, self.btnCompute_OnButtonClick )

	def __del__( self ):
		pass

	def ChangeBGColor(self, txtCtrl):
		BGColor = wx.Colour(144,238,144)
		if(self.m_txtBGChanged != None):
			self.m_txtBGChanged.SetBackgroundColour(wx.Colour(255, 255, 255)) 
			self.m_txtBGChanged.Refresh()
		
		txtCtrl.SetBackgroundColour(BGColor)
		txtCtrl.Refresh()
		self.m_txtBGChanged = txtCtrl


	def OnInitDialog( self, event ):
		fl = ThermoPhysical("")
		self.m_FluidList = fl.GetFluidNames()
	
		for entry in self.m_FluidList:
			self.m_choiceFluidType.Append(str(entry[0]))
		event.Skip()
	
	
	
	def FluidType_OnChoice( self, event ):
		sel = event.GetSelection()
		self.m_FluidType = self.m_FluidList[sel][0] 
		event.Skip()



	def radioT_OnRadioButton( self, event ):
		self.ChangeBGColor(self.m_txtT)
		self.m_SelectedProperty = "T"
		event.Skip()

	def radioRho_OnRadioButton( self, event ):
		self.ChangeBGColor(self.m_txtRho)
		self.m_SelectedProperty = "rho"
		event.Skip()

	def radioCp_OnRadioButton( self, event ):
		self.ChangeBGColor(self.m_txtCp)
		self.m_SelectedProperty = "cp"
		event.Skip()

	def radioK_OnRadioButton( self, event ):
		self.ChangeBGColor(self.m_txtK)
		self.m_SelectedProperty = "k"
		event.Skip()

	def radioMu_OnRadioButton( self, event ):
		self.ChangeBGColor(self.m_txtMu)
		self.m_SelectedProperty = "mu"
		event.Skip()

	def radioPr_OnRadioButton( self, event ):
		self.ChangeBGColor(self.m_txtPr)
		self.m_SelectedProperty = "pr"
		event.Skip()

	def btnCompute_OnButtonClick( self, event ):
		if self.m_FluidType == None:
			wx.MessageBox("Fluid type must be selected")
			return
		
		if self.m_SelectedProperty == None:
			wx.MessageBox("A property must be selected")
			return
		
		
		if self.m_txtBGChanged.GetValue() == "":
			wx.MessageBox("A value must be entered for " + self.m_SelectedProperty)
			return
		
		fl = ThermoPhysical(self.m_FluidType ) 
		result = dict()
		try:
			result = fl.search(self.m_SelectedProperty, float(self.m_txtBGChanged.GetValue()))
		except Exception as e:
			wx.MessageBox(str(e))
			return
            
		for lst in self.m_CtrlList:
			if lst[0] == self.m_txtBGChanged:
				continue
			Value = result.get(lst[1])
			Digits = self.m_Parent.GetDigits() 
			if(Digits != None):
				lst[0].SetValue(str(round(Value, Digits)))
			else:
				lst[0].SetValue(str(Value)) 

		event.Skip()


	def Export(self):
		s = str(self.m_SelectedProperty) + "=" + str(self.m_txtBGChanged.GetValue()) + "\n"
		
		for lst in self.m_CtrlList: 
			if lst[0] == self.m_txtBGChanged:
				continue
			Name = lst[1]
			Value = lst[0].GetValue()
			s += str(Name) + "=" + str(Value) + "\n"
		
		if wx.TheClipboard.Open():
			wx.TheClipboard.SetData(wx.TextDataObject(s))
			wx.TheClipboard.Close()
			wx.TheClipboard.Flush()



class frmFluidProperties ( wx.Frame ):

	def __init__( self, parent=None, FileMenu = None ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Properties of Fluids" )
		
		self.m_Digits = None
		
		ParentPath = _parent_path(__file__)
		IconPath = ParentPath / "icons" / "fluid.bmp"
		
		self.SetIcon(makeicon(IconPath))

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		self.m_notebook = wx.Notebook( self, wx.ID_ANY)
		self.m_pnlSaturated = pnlRefrigerantSaturated( self.m_notebook )
		self.m_pnlSaturated.InitDialog()
		
		self.m_pnlSuperheated = pnlRefrigerantSuperheated( self.m_notebook)
		self.m_pnlSuperheated.InitDialog()
		
		self.m_pnlThermal = pnlThermoPhysical( self.m_notebook)
		self.m_pnlThermal.InitDialog()
		
		self.m_notebook.AddPage( self.m_pnlSaturated, u"Saturated", True )
		self.m_notebook.AddPage( self.m_pnlSuperheated, u"Superheated", False )
		self.m_notebook.AddPage( self.m_pnlThermal, u"Thermo-physical", False )

		mainSizer.Add( self.m_notebook, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizerAndFit( mainSizer )
		self.Layout()
		
		self.m_menubar = wx.MenuBar( 0 )

		if FileMenu == None:
			self.m_FileMenu = wx.Menu()
			self.m_ItemExport = wx.MenuItem( self.m_FileMenu, wx.ID_ANY, u"Copy to clipboard")
			self.m_FileMenu.Append( self.m_ItemExport )
			self.Bind( wx.EVT_MENU, self.Export_OnMenu, id = self.m_ItemExport.GetId() )
		else:
			self.m_FileMenu = FileMenu

		self.m_menubar.Append( self.m_FileMenu, u"File" )

		self.m_menuDigits = wx.Menu()
		self.m_menuItem2 = wx.MenuItem( self.m_menuDigits, wx.ID_ANY, u"2 Digits", wx.EmptyString, wx.ITEM_RADIO )
		self.m_menuDigits.Append( self.m_menuItem2 )

		self.m_menuItem3 = wx.MenuItem( self.m_menuDigits, wx.ID_ANY, u"3 Digits", wx.EmptyString, wx.ITEM_RADIO )
		self.m_menuDigits.Append( self.m_menuItem3 )

		self.m_menuItem4 = wx.MenuItem( self.m_menuDigits, wx.ID_ANY, u"4 Digits", wx.EmptyString, wx.ITEM_RADIO )
		self.m_menuDigits.Append( self.m_menuItem4 )

		self.m_menuItem_AsIs = wx.MenuItem( self.m_menuDigits, wx.ID_ANY, u"As Is", wx.EmptyString, wx.ITEM_RADIO )
		self.m_menuDigits.Append( self.m_menuItem_AsIs )
		self.m_menuItem_AsIs.Check( True )

		self.m_menubar.Append( self.m_menuDigits, u"Digits" )
		self.SetMenuBar( self.m_menubar )


		self.Centre( wx.BOTH )

		
		self.Bind( wx.EVT_MENU, self.Digit2_OnMenu, id = self.m_menuItem2.GetId() )
		self.Bind( wx.EVT_MENU, self.Digit3_OnMenu, id = self.m_menuItem3.GetId() )
		self.Bind( wx.EVT_MENU, self.Digit4_OnMenu, id = self.m_menuItem4.GetId() )
		self.Bind( wx.EVT_MENU, self.AsIs_OnMenu, id = self.m_menuItem_AsIs.GetId() )

	def __del__( self ):
		pass

	
	def Export_OnMenu( self, event ):
		curPage = self.m_notebook.GetCurrentPage()
		curPage.Export()
		
		event.Skip()
	
	def Digit2_OnMenu( self, event ):
		self.m_Digits = 2
		event.Skip()

	def Digit3_OnMenu( self, event ):
		self.m_Digits = 3
		event.Skip()

	def Digit4_OnMenu( self, event ):
		self.m_Digits = 4
		event.Skip()

	def AsIs_OnMenu( self, event ):
		self.m_Digits = None
		event.Skip()

	def GetDigits(self):
            return self.m_Digits