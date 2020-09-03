# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 14:42:36 2020

@author: lajamu
"""

metadata = {
    'protocolName': 'Gibson',
    'author': 'Lachlan <lajamu@biosustain.dtu.dk',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.2'
}

#Fragment setups need to be hardcoded. Each nested list should describe the location of 
#fragments that will generate a construct
fragments = [
                [0, 3],
                [0, 1, 2], 
                [0, 4], 
                [0, 5], 
                [9, 6],
                [9, 7, 8]
                    ]
               



def run(protocol): 
    """
    Sets up and incubates a Gibson Reaction, then transforms the gibson product
    into A. Bayli.
    """
    #Load Tips
    tips20= [protocol.load_labware('opentrons_96_tiprack_20ul', '1')]
    tips200 = [protocol.load_labware('opentrons_96_tiprack_300ul', '2')]
    
    #Load Pipettes
    p20Single = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=tips20)
    p300Single = protocol.load_instrument('p300_single', 'left', tip_racks=tips200)
    

    
    
    #Load Labware
    pcrPlate = protocol.load_labware('opentrons_96_aluminumblock_generic_pcr_strip_200ul', '5')
    masterMixRack = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '4')
    gibsonMasterMix = masterMixRack.wells_by_name()["A1"]
    water = masterMixRack.wells_by_name()["B1"]
    gibson_rack = protocol.load_labware('opentrons_96_aluminumblock_generic_pcr_strip_200ul', "6")
    

    
    def make_gibson(frags, dest):
        """
        Makes a 20 uL gibson reaction with 2 fragments and water or 3 fragments.
        """
        
        for f in frags:
            p20Single.transfer(3.3, pcrPlate.wells()[f], dest, new_tip="always", touch_tip=True)
        if len(frags) == 2:
            p20Single.transfer(3.3, water, dest, new_tip="always", touch_tip=True)
        p20Single.transfer(10, gibsonMasterMix, dest, new_tip="always", mix_after=(1, 20))

    w=0
    for x in fragments:
        make_gibson(x, gibson_rack.wells()[w])
        w+=1
        

    
    
    
    