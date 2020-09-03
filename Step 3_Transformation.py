     

   
metadata = {
    'protocolName': 'Transformation',
    'author': 'Lachlan <lajamu@biosustain.dtu.dk',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.2'
}

nConstructs = 8    

def run(protocol):
        

    
        #Load Tips
        tips20= [protocol.load_labware('opentrons_96_tiprack_20ul', '1')]
        tips200 = [protocol.load_labware('opentrons_96_tiprack_300ul', '2')]
        
        #Load Pipettes
        p20Single = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=tips20)
        p300Single = protocol.load_instrument('p300_single', 'left', tip_racks=tips200)
        
        gibson_rack = protocol.load_labware('opentrons_96_aluminumblock_generic_pcr_strip_200ul', "5")
        transformationPlate = protocol.load_labware("usascientific_96_wellplate_2.4ml_deep", "4")
        rack_50mL = protocol.load_labware("opentrons_6_tuberack_falcon_50ml_conical", "7")
        abayli = rack_50mL.wells_by_name()["A1"]

        
        for i in range(0, nConstructs):
            
            p300Single.transfer(500, abayli.bottom(5), transformationPlate.wells()[i].bottom(5))


        
        #Trasnfer 
        for i in list(range(0,nConstructs)):
            p20Single.transfer(2, gibson_rack.wells()[i], transformationPlate.wells()[i].bottom(5))
        
        
        
        protocol.comment("Transformation placed in 30 degrees overnight")