# -*- coding: utf-8 -*-

'''
Created on 10 juin 2014

@author: etienne
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import os

from processing.core.Processing import Processing
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from processing.parameters.ParameterString import ParameterString
from processing.outputs.OutputNumber import OutputNumber
from QuickOSM.CoreQuickOSM.API.Nominatim import Nominatim
from os.path import dirname,abspath


class NominatimQueryGeoAlgorithm(GeoAlgorithm):

    SERVER = 'SERVER'
    NOMINATIM_STRING = 'NOMINATIM_STRING'
    OSM_ID = 'OSM_ID'

    def defineCharacteristics(self):
        self.name = "Query nominatim API with a string"
        self.group = "API"

        self.addParameter(ParameterString(self.SERVER, 'Nominatim server', 'http://nominatim.openstreetmap.org/search?format=json', False, False))
        self.addParameter(ParameterString(self.NOMINATIM_STRING, 'Search','Montpellier', False, False))
        self.addOutput(OutputNumber(self.OSM_ID,'OSM id'))


    def help(self):
        return True, 'Help soon'
    
    '''def getIcon(self):
        return QIcon(dirname(dirname(dirname(abspath(__file__))))+"/icon.png")'''

    def processAlgorithm(self, progress):
        
        server = self.getParameterValue(self.SERVER)
        query = self.getParameterValue(self.NOMINATIM_STRING)
        
        nominatim = Nominatim(url = server)
        try:
            osmID = nominatim.getFirstPolygonFromQuery(query)
            progress.setInfo("Getting first OSM relation ID from Nominatim :",osmID)
        except:
            raise
        self.setOutputValue("OSM_ID",osmID)