import numpy as np
import scisuit.plot as plt

#Helper function to find the average between two data points
def FindAvg(vec):
	return [(vec[i] + vec[i-1])/2.0 for i in range(1, len(vec))]


#Performs the computation for a single temperature array
def Compute(t:np.ndarray, T:np.ndarray, Dval_time:float, Dval_T:float, zvalue:float, Ref_T:float):
	assert len(t) == len(T), "Length of time and temperature data must be equal."
	
	DValue = Dval_time*10.0**((Dval_T-T)/zvalue) 
	LethRt = 10.0**((T-Ref_T)/zvalue) #Lethal rate
	
	#Although this is fairly slow, for this application it is fast enough. 
	FValue = [float(np.trapezoid(x=t[0:i], y=LethRt[0:i])) for i in range(1, len(t)+1)]
	
	dt = np.diff(t)
	avg_T = np.asarray(FindAvg(T), dtype=np.float64)
	DVal_avg = Dval_time*10.0**((Dval_T-avg_T)/zvalue)
	LogRed = dt/DVal_avg
	
	TotalLogRed = np.cumsum(LogRed)
	TotalLogRed = np.insert(TotalLogRed, 0, 0.0) # at time=0 TotalLogRed(1)=0

	return {"Lethality":LethRt.tolist(), "Dvalue":DValue.tolist(), "TotalLogRed":TotalLogRed.tolist(), "Fvalue":FValue}


#Inputs
time = [0,1,2,3,4,5,6]
temperatures = [ 
[75,105,125,140,135,120,100], 
]

zvalue = 11
Dvalue_Temp = 121
Dvalue_Time = 1.1
RefTemp = 121


#Collect the output(s) (can be more than one temperature array)
Results:list[dict] = []

#compute the time-temperature effect for each temperature array
for _T in temperatures:				
	T = np.asarray(_T, dtype=np.float64) 
	result = Compute(time, T, Dvalue_Time, Dvalue_Temp, zvalue, RefTemp) 			
	Results.append(result)

#print the first entry (if multiple use a simple for loop)
print(Results[0])

#Visualize computed values 
plt.scatter(x=time, y=Results[0].get("Fvalue"))
plt.show()