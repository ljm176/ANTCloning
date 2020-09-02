# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 08:15:02 2020

@author: lajamu
"""

metadata = {
    'protocolName': 'Dilution',
    'author': 'Lachlan <lajamu@biosustain.dtu.dk',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.2'
}

nReactions = 10
def run(protocol): 
    """
    Adds master mix and primers to PCR wells
    """
    #Load Tips
    tips20= [protocol.load_labware('opentrons_96_tiprack_20ul', '1')]
    tips200 = [protocol.load_labware('opentrons_96_tiprack_300ul', '2')]
    
    

    #Load Pipettes
    p20Single = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=tips20)
    p300Single = protocol.load_instrument('p300_single', 'left', tip_racks=tips200)
    
    temp_mod = protocol.load_module("tempdeck", "7")
    dilutionPlate = temp_mod.load_labware('opentrons_96_aluminumblock_generic_pcr_strip_200ul')
    
    temp_mod.set_temperature(37)
    
    #load Labware
    pcrPlate = protocol.load_labware('opentrons_96_aluminumblock_generic_pcr_strip_200ul', '3')
    
    
    rack= protocol.load_labware('opentrons_24_aluminumblock_nest_1.5ml_snapcap', '5')
    water_dpn = rack.wells_by_name()["A1"]

    for i in range(nReactions):
        p300Single.transfer(40, water_dpn, dilutionPlate.wells()[i])

        
    protocol.delay(minutes=15)
    temp_mod.set_temperature(4)
    
