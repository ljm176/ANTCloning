# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 09:34:10 2020

@author: lajamu
"""

metadata = {
    'protocolName': 'Plating of Natural Transformation',
    'author': 'Lachlan <lajamu@biosustain.dtu.dk',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.2'
}

nConstructs = 32

def run(protocol):
    """
    Plates a transformed A. Baylyi culture onto LB Agar. 
    """
    #Load Tips

    tips200 = [protocol.load_labware('opentrons_96_tiprack_300ul', '2')]

    #Load Pipettes
    #p20Single = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=tips20)
    p300Single = protocol.load_instrument('p300_single', 'left', tip_racks=tips200)
    
    #load labware
    #Transformation wellplates
    transformation = protocol.load_labware('usascientific_96_wellplate_2.4ml_deep', '7')

    
    #Agar plates
    
    agar1 = protocol.load_labware("corning_12_wellplate_6.9ml_flat", "4")
    agar2 = protocol.load_labware("corning_12_wellplate_6.9ml_flat", "5")
    agar3 = protocol.load_labware("corning_12_wellplate_6.9ml_flat", "6")

    spots = agar1.wells() + agar2.wells() + agar3.wells()
    

    def spot(dest, spot_vol):
        """Takes a diluted transformed culture and spots the defined volume onto agar 
        in a Nunc omnitray"""


        SAFE_HEIGHT = 15  
        spotting_dispense_rate=0.025 

        p300Single.move_to(dest.top(SAFE_HEIGHT))
        protocol.max_speeds["Z"] = 50
        p300Single.move_to(dest.top(2))
        p300Single.dispense(volume=spot_vol, rate=spotting_dispense_rate)
        p300Single.move_to(dest.top(0))
        del protocol.max_speeds["Z"]
        

    spotVol = 30
    for i in range(nConstructs):
    	p300Single.pick_up_tip()
    	p300Single.mix(3, 200, transformation.wells()[i])
    	p300Single.aspirate(spotVol, transformation.wells()[i])
    	p300Single.touch_tip()
    	spot(spots[i], spotVol)
    	p300Single.drop_tip()

   
