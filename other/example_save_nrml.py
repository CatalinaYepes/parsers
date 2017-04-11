# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 23:27:33 2015

@author: catalinayepes
"""

import xml.etree.ElementTree as ET
import lxml.etree as etree

def child_funtion(vul_model):
    '''vul_model is a class containing: 
    taxo as string and 
    imls,loss_ratio and covs as lists of values'''
    function = ET.SubElement(vul_model, 'vulnerabilityFunction', dist="LN", id=vul_model.taxo)
    imls = ET.SubElement(function, 'imls', imt=vul_model.IMT)
    imls.text = ' '.join(map(str,vul_model.imls))
    lrs = ET.SubElement(function, 'meanLRs')
    lrs.text = ' '.join(map(str,vul_model.loss_ratio))
    covs = ET.SubElement(function, 'covLRs')
    covs.text = ' '.join(map(str,vul_model.covs))


root = ET.Element('nrml', xmlns='http://openquake.org/xmlns/nrml/0.5')
tree = ET.ElementTree(root)

vul_model = ET.SubElement(root, 'vulnerabilityModel', id="funtions_SARA", assetCategory="buildings", lossCategory="economic" )
description = ET.SubElement(vul_model, 'description')
description.text = 'result of SARA project'

taxo = "MUR/H:1"
IMT = "PGA"
values = [0, 10, 13]


function = ET.SubElement(vul_model, 'vulnerabilityFunction', dist="LN", id=taxo)
imls = ET.SubElement(function, 'imls', imt=IMT)
imls.text = ' '.join(map(str,values))
lrs = ET.SubElement(function, 'meanLRs')
covs = ET.SubElement(function, 'covLRs')


# To save is enough with tree.write('file_name'), to pretty print
save_as = 'test.xml'
tree.write(save_as)
x = etree.parse(save_as)

print etree.tostring(x, pretty_print = True)

output_file = open( save_as, 'w' )
output_file.write( '<?xml version="1.0" encoding="UTF-8"?>' )
output_file.write( etree.tostring(x, pretty_print = True) )
output_file.close()

