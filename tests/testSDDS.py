#! /usr/bin/env python
import sys
import time
import logging

import context
import pyElegant
import sdds



def sddsDemo1(output):
     sdds.demo(output)
    
def sddsDemo2(output):
     sdds.demo2(output)

def sddsDemo3(input, output):
     x = sdds.SDDS(0)
     x2 = sdds.SDDS(1)
     
     x.load(input)
     x.save(output)
     x2.load(input)
     x2.save(output)

#sddsDemo1('pythonWriteExample.sdds')
#sddsDemo2('pythonWriteExample.sdds')
logging.basicConfig(level=logging.DEBUG)
sddsDemo3('pythonReadExample.sdds', 'pythonWriteExample.sdds')
