# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 14:42:36 2020

@author: lajamu
"""

metadata = {
    'protocolName': 'Gibson, Transformation and Plating',
    'author': 'Lachlan <lajamu@biosustain.dtu.dk',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.2'
}

def run(protocol): 
    """
    Sets up and incubates a Gibson Reaction
    """
    #Load Tips
    tips20= [protocol.load_labware('opentrons_96_tiprack_300ul', '1')]
    tips200 = [protocol.load_labware('opentrons_96_tiprack_300ul', '2')]
    
    #Load temperature module

     temperature_module = protocol.load_module('temperature module', 3)
     temperaure_module.load_labware("opentrons_24_aluminumblock_nest_1.5ml_snapcap")
     
     temperature_module.set_temp(50)
     
     