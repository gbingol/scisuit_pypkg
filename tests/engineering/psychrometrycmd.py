from scisuit.eng import psychrometry
import scisuit.plot as plt
import scisuit.plot.gdi as gdi

psy = psychrometry(P=101, Tdb=20, Twb=15)
print(psy)

P = 101
Tdb = 20
W = 0.008623540951296561

#Instead of using theoretical limits we are using the practical ones
assert 70<P<120, "P [70, 120] kPa expected."
assert 0<W<1, "Absolute humidity (0, 1) expected."
assert -0<Tdb<90, "Tdb [0, 90]"

plt.psychrometry(P=P*1000)
gdi.marker(xy=(Tdb, W), size=5, fc="#000000")
plt.show()