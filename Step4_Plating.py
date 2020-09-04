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

nConstructs = 8

def run(protocol):
    
    #Load Tips
    #tips20= [protocol.load_labware('opentrons_96_tiprack_300ul', '1')]
    tips200 = [protocol.load_labware('opentrons_96_tiprack_300ul', '2')]

    #Load Pipettes
    #p20Single = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=tips20)
    p300Single = protocol.load_instrument('p300_single', 'left', tip_racks=tips200)
    
    #load labware
    #Transformation wellplates
    transformation = protocol.load_labware('usascientific_96_wellplate_2.4ml_deep', '7')
    dilution1 = protocol.load_labware('usascientific_96_wellplate_2.4ml_deep', '8')
    dilution2 = protocol.load_labware('usascientific_96_wellplate_2.4ml_deep', '9')
    
    #Agar plates
    
    agar1 = protocol.load_labware("corning_24_wellplate_3.4ml_flat", "4")
    agar2 = protocol.load_labware("corning_24_wellplate_3.4ml_flat", "5")
    agar3 = protocol.load_labware("corning_24_wellplate_3.4ml_flat", "6")
    
    
    lb_rack = protocol.load_labware("opentrons_6_tuberack_falcon_50ml_conical", "10")
    lb = lb_rack.wells_by_name()["A1"]
    

    def spot(dest, spot_vol):
        """Takes a diluted transformed culture and spots 50 microlitres onto agar 
        in a Nunc omnitray"""


        SAFE_HEIGHT = 15  # height avoids collision with agar tray.
        spotting_dispense_rate=0.025 

        p300Single.move_to(dest.top(SAFE_HEIGHT))
        protocol.max_speeds["Z"] = 50
        p300Single.move_to(dest.top(2))
        p300Single.dispense(volume=spot_vol, rate=spotting_dispense_rate)
        p300Single.move_to(dest.top(0))
        del protocol.max_speeds["Z"]
        
    
    
    #Load LB into neccesary wells
    p300Single.pick_up_tip()
    p300Single.transfer(180, lb, [dilution1.wells()[0:nConstructs], dilution2.wells()[0:nConstructs]], new_tip="never")
    p300Single.drop_tip()
    
    def dispense_and_mix(vol, dest):
        p300Single.dispense(vol, dest)
        p300Single.mix(4, 200, dest)
    
    def dilute_and_spot(well, spot_vol):
        p300Single.pick_up_tip()
        p300Single.aspirate(20 + spot_vol, transformation.wells()[well])
        spot(agar1.wells()[well], spot_vol)
        dispense_and_mix(20, dilution1.wells()[well])
        p300Single.aspirate(20 + spot_vol, dilution1.wells()[well])
        spot(agar2.wells()[well], spot_vol)
        dispense_and_mix(20, dilution2.wells()[well])
        p300Single.aspirate(20 + spot_vol, dilution2.wells()[well])
        spot(agar3.wells()[well], spot_vol)
        p300Single.drop_tip()
        
    for w in list(range(nConstructs)):
        dilute_and_spot(w, 25)
        
    
