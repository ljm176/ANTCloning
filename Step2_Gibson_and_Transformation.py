# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 14:42:36 2020

@author: lajamu
"""

metadata = {
    'protocolName': 'Gibson and Transformation',
    'author': 'Lachlan <lajamu@biosustain.dtu.dk',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.2'
}



def run(protocol): 
    """
    Sets up and incubates a Gibson Reaction, then transforms the gibson product
    into A. Bayli.
    """
    #Load Tips
    tips20= [protocol.load_labware('opentrons_96_tiprack_300ul', '1')]
    tips200 = [protocol.load_labware('opentrons_96_tiprack_300ul', '2')]
    
    #Load Pipettes
    p20Single = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=tips20)
    p300Single = protocol.load_instrument('p300_single', 'left', tip_racks=tips200)
    
    #Load temperature module
    temperature_module = protocol.load_module('temperature module', 3)
    temp_rack = temperature_module.load_labware("opentrons_96_aluminumblock_generic_pcr_strip_200ul")
    temperature_module.set_temperature(50)
    
    
    #Load Labware
    pcrPlate = protocol.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', '5')
    masterMixRack = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '4')
    gibsonMasterMix = masterMixRack.wells_by_name()["A1"]
    water = masterMixRack.wells_by_name()["B1"]
    transformationPlate = protocol.load_labware("usascientific_96_wellplate_2.4ml_deep", "6")
    rack_50mL = protocol.load_labware("opentrons_6_tuberack_falcon_50ml_conical", "9")
    abayli = rack_50mL.wells_by_name()["A1"]
    
    
    #Fragment setups need to be hardcoded. Each nested list should describe the location of 
    #fragments that will generate a construct
    
    #Can write a function to make this setup easier (call PCR plate.wells from
    #a number)
    fragments = [[pcrPlate.wells()[0], pcrPlate.wells()[1]], 
                 [pcrPlate.wells()[2], pcrPlate.wells()[3]]
                 ]
    
    nConstructs = len(fragments)
    
    def make_gibson(frags, dest):
        """
        Makes a 20 uL gibson reaction with 2 fragments and water or 3 fragments.
        """
        
        for f in frags:
            p20Single.transfer(3.3, f, dest, new_tip="always")
        if len(frags) == 2:
            p20Single.transfer(3.3, water, dest, new_tip="always")
        p20Single.transfer(10, gibsonMasterMix, dest, new_tip="always", mix_after=(3, 20))

    w=0
    for x in fragments:
        make_gibson(x, temp_rack.wells()[w])
        
    #Incubation
    protocol.delay(minutes = 120)
    ##Decide if want to switch to the p1000 and do a distribute for the LB
    
    protocol.comment("Add overnight culture to A1 on rack at position 9,\
                     and deep well plate preloaded with 450uL LB to position 6")
    #Add overnight culture to prefilled LB.
    p300Single.distribute(50, abayli, transformationPlate.wells()[0:nConstructs])
    
    #Trasnfer 
    for i in list(range(0,nConstructs)):
        p20Single.transfer(2, temp_rack.wells()[i], transformationPlate.wells()[i])
    
    
    
    protocol.comment("Transformation placed in 30 degrees overnight")
    
    
    
    
    
    