from cmath import inf
import wx
import string



class NumTextCtrl(wx.TextCtrl):
	"""
	A text ctrl that only allows numeric entries
	Decimal separator used is .
	"""
	def __init__(self, parent, id = wx.ID_ANY, val:str = wx.EmptyString, minval:float = -inf, maxval:float = inf):
		wx.TextCtrl.__init__(self, parent, id)

		self.m_Min = minval
		self.m_Max = maxval
		self.m_InitVal = val

		if(minval>-inf and maxval<inf):
			self.SetToolTip(self.ToRange(minval, maxval))

		if(val != wx.EmptyString):
			try:
				numVal=float(val)
				self.SetValue(val)
			except ValueError as ve:
				pass

		self.Bind(wx.EVT_CHAR, self.OnChar)
		self.Bind(wx.EVT_TEXT, self.OnText)
		self.Bind( wx.EVT_KILL_FOCUS, self.OnKillFocus )
	

	def ToRange(self, minval:float, maxval:float):
		return "Expected range [" + str(minval) + "," + str(maxval)+ "]"

	
	def OnKillFocus(self, event):
		val = self.GetValue()
		if(val != wx.EmptyString):
			try:
				numVal=float(val)
			except ValueError as ve:
				self.SetValue("")
		
		event.Skip()


	def OnText(self, event):
		if self.GetValue() == "":
			event.Skip()
			return
			
		NumVal = float(self.GetValue())
		if(NumVal<self.m_Min or NumVal>self.m_Max):
			wx.MessageBox(self.ToRange(self.m_Min, self.m_Max))

			#reset the value so that user will not be bugged when trying to recover from a mistake
			self.SetValue(self.m_InitVal)
		else:
			event.Skip()


	def OnChar(self, event):
		key = event.GetKeyCode()
		val = self.GetValue()
		if key == wx.WXK_NONE:
			pass 

		elif chr(key) in string.digits:
			event.Skip()

		elif key==wx.WXK_DELETE or key==wx.WXK_BACK or key==wx.WXK_HOME:
			event.Skip()
		
		elif key==wx.WXK_LEFT or key == wx.WXK_RIGHT:
			event.Skip()
		
		#dont allow duplicate separators
		elif chr(key)=='.' and '.' not in val:
			event.Skip()
		
		elif (chr(key) =='E' or chr(key)=='e') and ('E' not in val) and ('e' not in val):
			#if there is no character then E or e not make any sense
			if(val != wx.EmptyString):
				#if first character is minus then we need at least 2 characters and second one must be digit
				if(val[0]=='-'):
					if(len(val)>=2 and val[1] in string.digits):
						event.Skip()
				else:
					#if first character is not minus and E or e not already entered, allow it
					event.Skip()

		
		#only allow minus at the beginning
		elif chr(key)=='-':
			if(val == wx.EmptyString):
				event.Skip()
			else:
				HasE= ('E' in val) or ('e' in val)
				#if there is already minus at the beginning dont allow to add more
				if val[0] == '-' and not HasE:
					self.SetValue(val[0:])
				else:
					if HasE:
						event.Skip()
					else:
						self.SetValue('-' + val)
		
		elif chr(key) == ',':
			wx.MessageBox("Use decimal point (.) as the decimal separator")