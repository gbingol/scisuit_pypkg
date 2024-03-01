from .charts import layout, subplot, figure, legend, show, title, xlabel, ylabel
from .gdi import Pen, Brush
from .charts import bar, barh, boxplot, bubble, dirfield, hist, line, \
			pie, plot, psychrometry, qqnorm, qqplot, quiver, scatter

from .chartelems import Marker, Trendline


"""Trendline styles"""
TRENDLINE_LINEAR = "linear"
TRENDLINE_POLY = "poly"
TRENDLINE_EXP = "exp"
TRENDLINE_LOG = "log"
TRENDLINE_POW = "pow"



"""Pen styles"""
PEN_SOLID = 100
PEN_DOT = 101
PEN_LONGDASH = 102
PEN_SHORTDASH = 103
PEN_DOTDASH = 104
PEN_TRANSPARENT = 106

"""Brush styles"""
BRUSH_SOLID = 100
BRUSH_TRANSPARENT = 106
BRUSH_BDIAGHATCH = 111
BRUSH_CROSSDIAGHATCH = 112
BRUSH_FDIAGHATCH = 113
BRUSH_CROSSHATCH = 114
BRUSH_HORIZHATCH =115
BRUSH_VERTHATCH = 116

""" Colors with corresponding RGB values"""
COLOR_AQUA = "0 255 255"
COLOR_BLACK = "0 0 0"
COLOR_BLUE = "0 0 255"
COLOR_BLUE_MEDIUM = "0 0 205"
COLOR_BLUE_ROYAL="65 105 225"
COLOR_BLUE_MIDNIGHT="25 25 112"
COLOR_BROWN="165 42 42"
COLOR_BROWN_SADDLE="139 69 19"
COLOR_CHOCOLATE="210 105 30" 
COLOR_CRIMSON="220 20 60"
COLOR_FUCHSIA="255 0 255"
COLOR_GRAY="128 128 128"
COLOR_WHITE="255 255 255"
COLOR_RED="255 0 0"
COLOR_RED_DARK="139 0 0"
COLOR_LIME="0 255 0"
COLOR_YELLOW="255 255 0"
COLOR_SILVER="192 192 192"
COLOR_MAROON="128 0 0"
COLOR_OLIVE="128 128 0"
COLOR_GREEN="0 128 0"
COLOR_PURPLE="128 0 128"
COLOR_TEAL="0 128 128"
COLOR_NAVY="0 0 128" 
COLOR_SALMON_DARK="233 150 122"
COLOR_SALMON="250 128 114" 
COLOR_SALMON_LIGHT="255 160 122"
COLOR_ORANGE_RED="255 69 0"
COLOR_ORANGE_DARK="255 140 0"
COLOR_ORANGE="255 165 0"
COLOR_TAN="210 180 140"
COLOR_WHEAT="245 222 179"
COLOR_ORCHID="218 112 214"
COLOR_INDIGO="75 0 130"

""" Marker Styles"""
MARKER_CIRCLE = "c"
MARKER_TRIANGLE = "t"
MARKER_SQUARE = "s"
MARKER_XMARKER = "x"