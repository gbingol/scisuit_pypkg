"""
Food Process Engineering library (FPE)
"""


""" Food is the base class"""
from .foodmaterial import \
	Food, \
	Beverage, Juice, Cereal, Legume, Nut, Dairy, Fruit, Vegetable, Meat, Sweet, \
	Cp


"""Different methods to compute water activity"""
from .wateractivity import Aw