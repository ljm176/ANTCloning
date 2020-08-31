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


def run(protocol):
    
    #Load Tips
    tips20= [protocol.load_labware('opentrons_96_tiprack_300ul', '1')]
    tips200 = [protocol.load_labware('opentrons_96_tiprack_300ul', '2')]

    #Load Pipettes
    p20Single = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=tips20)
    p300Single = protocol.load_instrument('p300_single', 'left', tip_racks=tips200)
    
    #load labware
    
    transformation = protocol.load_labware('usascientific_96_wellplate_2.4ml_deep', '4')
    dilution = protocol.load_labware('usascientific_96_wellplate_2.4ml_deep', '5')
    agar = protocol.load_labware("corning_24_wellplate_3.4ml_flat", "6")
    lb_rack = protocol.load_labware("opentrons_6_tuberack_falcon_50ml_conical", "7")
    lb = lb_rack.wells_by_name()["A1"]

    def spot(well, spot_vol=10):
        """Takes a diluted transformed culture and spots 50 microlitres onto agar 
        in a Nunc omnitray"""
        
        dil = dilution.wells()[well]
        dest = agar.wells()[well]

        SAFE_HEIGHT = 15  # height avoids collision with agar tray.
        spotting_dispense_rate=0.025 
        
        p300Single.aspirate(spot_vol, dil)
        p300Single.move_to(dest.top(SAFE_HEIGHT))
        p300Single.move_to(dest.top(2))
        p300Single.dispense(volume=spot_vol, rate=spotting_dispense_rate)
        p300Single.move_to(dest.top(1))


    def dilute(well):
        p300Single.consolidate([135, 15], [lb, transformation.wells()[well]], 
                               dilution.wells()[well], mix_after=(3, 150),
                               new_tip="never")
        
    
    def dilute_then_spot(well):
        p300Single.pick_up_tip()
        dilute(well)
        spot(well)
        p300Single.drop_tip()
        
    for w in list(range(5)):
        dilute_then_spot(w)
           
        
        
    
