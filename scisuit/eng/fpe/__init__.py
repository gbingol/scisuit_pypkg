""" Food Process Engineering library (FPE) """


""" Food is the base class"""
from .foodmaterial import Food, Beverage, Juice, Cereal, Legume, Nut, Dairy, Fruit, Vegetable, Meat, Sweet


"""Different methods to compute water activity and specific heat capacity"""
from ._foodproperty import Aw, Cp