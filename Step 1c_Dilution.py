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

nReactions = 5
def run(protocol): 
    """
    Adds master mix and primers to PCR wells
    """
    #Load Tips
    tips20= [protocol.load_labware('opentrons_96_tiprack_300ul', '1')]
    tips200 = [protocol.load_labware('opentrons_96_tiprack_300ul', '2')]
    
    

    #Load Pipettes
    p20Single = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=tips20)
    p300Single = protocol.load_instrument('p300_single', 'left', tip_racks=tips200)
    
    temp_mod = protocol.load_module("tempdeck", "7")
    dilutionPlate = temp_mod.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')
    
    temp_mod.set_temperature(37)
    
    #load Labware
    pcrPlate = protocol.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', '3')
    
    
    rack= protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '5')
    water = rack.wells_by_name()["A1"]
    dpn1 = rack.wells_by_name()["B1"]
    
    p300Single.distribute(21, water, dilutionPlate.wells()[0:nReactions])
    p20Single.distribute(1, dpn1, dilutionPlate.wells()[0:nReactions])
    
    for w in list(range(0, 5)):
        p20Single.transfer(15, pcrPlate.wells()[w], dilutionPlate.wells()[w],
                           new_tip = "always", mix_after = (3, 20))
        
    protocol.delay(minutes=15)
    temp_mod.set_temperature(4)