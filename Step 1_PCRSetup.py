# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 10:46:16 2020

@author: lajamu
"""

metadata = {
    'protocolName': 'PCR Setup',
    'author': 'Lachlan <lajamu@biosustain.dtu.dk',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.2'
}


#This protocol sets up the PCR reaction

#Function to split primers into list of primer pairs
def chunks(lst):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), 2):
        yield lst[i:i + 2]
        
#Number of Primer Pairs
nPrimerPairs = 10
#Define if sinlge or multiple templates will be used
singleTemplate = False

def run(protocol): 
    """
    Adds master mix, primers and template to PCR wells
    """
    #Load Tips
    tips20= [protocol.load_labware('opentrons_96_tiprack_20ul', '1')]
    #tips200 = [protocol.load_labware('opentrons_96_tiprack_300ul', '2')]

    #Load Pipettes
    p20Single = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=tips20)
    #p300Single = protocol.load_instrument('p300_single', 'left', tip_racks=tips200)
    
    #load Labware
    pcrPlate = protocol.load_labware('opentrons_96_aluminumblock_generic_pcr_strip_200ul', '3')
    masterMixRack = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '4')
    primerRack = protocol.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', '5')
    templateRack = protocol.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', '6')
    
    #Define Location of master mix and water
    masterMix = masterMixRack.wells_by_name()["A1"]

    
    #Define location of primerp pairs and generate a list of pairs
    primers=primerRack.wells()[0:2*nPrimerPairs]
    primerPairs = list(chunks(primers))

    #Add template location to list
    for x in range(nPrimerPairs):
        if singleTemplate:
            primerPairs[x].insert(0, templateRack.wells()[0])
        else:
            primerPairs[x].insert(0, templateRack.wells()[x])
    
    

    #Distribute master mix to wells required for reaction
    p20Single.distribute(10, masterMix, pcrPlate.wells()[0:nPrimerPairs])
    

    
    def makePCRMix(primers, dest):
        """
        Adds template and primers to a well then mixes 3 x 20 uL
        """
        p20Single.consolidate([2, 4, 4], primers, dest, mix_after = (3, 20))
        #Add primer pairs and template to reaction wells
   
    w = 0
    for p in primerPairs:
        makePCRMix(p, pcrPlate.wells()[w])
        w+=1
    
    
    

    
    
    
    
    