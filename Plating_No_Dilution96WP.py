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

nConstructs = 96

def run(protocol):
    """
    Plates a transformed A. Baylyi culture onto LB Agar. 
    """
    #Load Tips

    tips20 = [protocol.load_labware('opentrons_96_tiprack_20ul', '1')]

    #Load Pipettes
    #p20Single = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=tips20)
    p20Multi = protocol.load_instrument('p20_multi_gen2', 'right', tip_racks=tips20)
    
    #load labware
    #Transformation wellplates
    transformation = protocol.load_labware("corning_96_wellplate_360ul_flat", '2')

    
    #Agar plates
    
    agar1 = protocol.load_labware("biorad_96_wellplate_200ul_pcr", "4")
    agar2 = protocol.load_labware("biorad_96_wellplate_200ul_pcr", "5")


    def spot(dest, spot_vol):
        """Takes a diluted transformed culture and spots the defined volume onto agar 
        in a Nunc omnitray"""


        SAFE_HEIGHT = 15  
        spotting_dispense_rate=0.25 

        p20Multi.move_to(dest.top(SAFE_HEIGHT))
        protocol.max_speeds["Z"] = 50
        p20Multi.move_to(dest.top(2))
        p20Multi.dispense(volume=spot_vol, rate=spotting_dispense_rate)
        p20Multi.move_to(dest.top(0))
        del protocol.max_speeds["Z"]
        

    for i in range(1,6):
        w1 = "A" + str(i)
        w2 = "A" + str(i + 6)
        p20Multi.pick_up_tip()
        p20Multi.mix(3, 20, transformation[w])
        p20Multi.aspirate(10, transformation[w])
        spot(agar1[w1], 5)
        spot(agar1[w2], 5)
        p20Multi.drop_tip()




   
