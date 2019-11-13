#!/usr/bin/env python

import datetime
import json
import os
import webapp2
import jinja2

import config

import sys
import ee


from google.appengine.api import memcache

#handles almost every request from the webpage
class MainHandler(webapp2.RequestHandler):
    """A servlet to handle requests to load the main web page."""
    def get(self, path=''): # if '/' then return HTML, if '/?fmt=json' return json
        if self.request.get('fmt') == 'json':
            date = self.request.get('date')
            date_range = self.request.get('date_range')
            landsat = self.request.get('mapLayer')
            #if landsat == 'l7' or landsat == 'l8':
            mapid = GetMapId(landsat, date, date_range)
            data = {'mapLayer': landsat,
                    'eeMapId': mapid['mapid'],
                    'eeToken': mapid['token']}; #testing python response to javascript
            self.response.out.headers['Content-Type'] = 'text/json'
            self.response.out.write(json.dumps(data))
            return

        template_values = {
            'mapKey': 'key=GoogleMapsKey',
##            'eeToken': mapid['token'],
        }
        template = JINJA2_ENVIRONMENT.get_template('index.html')
        self.response.out.write(template.render(template_values))


#doesn't do anything atm
class DetailsHandler(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(content)


# Define webapp2 routing from URL paths to web request handlers. See:
# http://webapp-improved.appspot.com/tutorials/quickstart.html
app = webapp2.WSGIApplication([
    ('/details', DetailsHandler),
    ('/', MainHandler),
])


###############################################################################
#                                   Helpers.                                  #
###############################################################################



def GetMapId(landsat, date, date_range):
    """Returns the MapID for Landsat."""
    
    def maskClouds(img):
        scored = ee.Algorithms.Landsat.simpleCloudScore(img);
        return img.updateMask(scored.select(['cloud']).lt(20));

    def CreateTimeBand(img):
        return maskClouds(img).byte().addBands(img.metadata('system:time_start'))

    if landsat == 'l7':
        collection = ee.ImageCollection(IMAGE_COLLECTION_ID_L7)
        l7 = collection.filter(ee.Filter.lte('CLOUD_COVER', 25)).filterDate(date_range, date).map(CreateTimeBand);
        l7Composite = l7.qualityMosaic('system:time_start');

        #vizParams = {bands: ['B4', 'B3', 'B2'], min: 0, max: 0.4};

        return l7Composite.getMapId({
            'min': '0,0,0',
            'max': '255,255,255',
            'bands': 'B4,B3,B2',
            })
    if landsat == 'l8':
        collection = ee.ImageCollection(IMAGE_COLLECTION_ID_L8)
        l8 = collection.filter(ee.Filter.lte('CLOUD_COVER', 25)).filterDate(date_range, date).map(CreateTimeBand);
        l8Composite = l8.qualityMosaic('system:time_start');

        #vizParams = {bands: ['B4', 'B3', 'B2'], min: 0, max: 0.4};

        return l8Composite.getMapId({
            'min': '0',
            'max': '0.4',
            'bands': 'B4,B3,B2',
            })

##params (ImageVisualizationParameters):
##The visualization parameters as a (client-side) JavaScript object. For Images and ImageCollections:
##- image (JSON string) The image to render.
##- version (number) Version number of image (or latest).
##- bands (comma-seprated strings) Comma-delimited list of band names to be mapped to RGB.
##- min (comma-separated numbers) Value (or one per band) to map onto 00.
##- max (comma-separated numbers) Value (or one per band) to map onto FF.
##- gain (comma-separated numbers) Gain (or one per band) to map onto 00-FF.
##- bias (comma-separated numbers) Offset (or one per band) to map onto 00-FF.
##- gamma (comma-separated numbers) Gamma correction factor (or one per band)
##- palette (comma-separated strings) List of CSS-style color strings (single-band previews only).
##- opacity (number) a number between 0 and 1 for opacity.
##- format (string) Either "jpg" or "png".

###############################################################################
#                                   Constants.                                #
###############################################################################


# Memcache is used to avoid exceeding our EE quota. Entries in the cache expire
# 24 hours after they are added. See:
# https://cloud.google.com/appengine/docs/python/memcache/
MEMCACHE_EXPIRATION = 60 * 60 * 24

# The ImageCollection of Landsat 7 TOA dataset. See:
# https://earthengine.google.org
IMAGE_COLLECTION_ID_L7 = 'LANDSAT/LE07/C01/T1_TOA'
IMAGE_COLLECTION_ID_L8 = 'LANDSAT/LC08/C01/T1_TOA'

# The scale at which to reduce the polygons for the brightness time series.
#REDUCTION_SCALE_METERS = 20000

# The Wikipedia URL prefix.
#WIKI_URL = 'http://en.wikipedia.org/wiki/'


###############################################################################
#                               Initialization.                               #
###############################################################################


# Use our App Engine service account's credentials.
EE_CREDENTIALS = ee.ServiceAccountCredentials(
    config.EE_ACCOUNT, config.EE_PRIVATE_KEY_FILE)

### Read the polygon IDs from the file system.
##POLYGON_IDS = [name.replace('.json', '') for name in os.listdir(POLYGON_PATH)]

# Create the Jinja templating system we use to dynamically generate HTML. See:
# http://jinja.pocoo.org/docs/dev/
JINJA2_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    autoescape=True,
    extensions=['jinja2.ext.autoescape'])

# Initialize the EE API.
ee.Initialize(EE_CREDENTIALS)
