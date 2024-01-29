import dataclasses as _dc


class Color:
	""" Colors with corresponding RGB values"""
	AQUA="0 255 255"
	BLACK="0 0 0"
	BLUE="0 0 255"
	BLUE_MEDIUM="0 0 205"
	BLUE_ROYAL="65 105 225"
	BLUE_MIDNIGHT="25 25 112"
	BROWN="165 42 42"
	BROWN_SADDLE="139 69 19"
	CHOCOLATE="210 105 30" 
	CRIMSON="220 20 60"
	FUCHSIA="255 0 255"
	GRAY="128 128 128"
	WHITE="255 255 255"
	RED="255 0 0"
	RED_DARK="139 0 0"
	LIME="0 255 0"
	YELLOW="255 255 0"
	SILVER="192 192 192"
	MAROON="128 0 0"
	OLIVE="128 128 0"
	GREEN="0 128 0"
	PURPLE="128 0 128"
	TEAL="0 128 128"
	NAVY="0 0 128" 
	SALMON_DARK="233 150 122"
	SALMON="250 128 114" 
	SALMON_LIGHT="255 160 122"
	ORANGE_RED="255 69 0"
	ORANGE_DARK="255 140 0"
	ORANGE="255 165 0"
	TAN="210 180 140"
	WHEAT="245 222 179"
	ORCHID="218 112 214"
	INDIGO="75 0 130"


@_dc.dataclass
class Pen:
	color:Color = None
	width:int = 1
	style:int= 100 #solid pen


@_dc.dataclass
class Brush:
	color:Color = None
	style:int = 100 #solid brush