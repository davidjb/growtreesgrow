# coding: utf-8
from __future__ import unicode_literals
import datetime
import logging
import time
import os
import random

import begin
from dateutil.tz import tzlocal
from fractions import Fraction
import flickrapi
import picamera
import yaml
from twython import Twython
from astral import Location


LATITUDE = -19.319002
LATITUDE_DMS = '19/1,19/1,84072/10000'
LATITUDE_REF = 'S'
LONGITUDE = 146.737610
LONGITUDE_DMS = '146/1,44/1,153960/10000'
LONGITUDE_REF = 'E'
ELEVATION = 32  # Metres above sea-level

LOCATION = Location(info=(
    'Townsville',
    'Australia',
    LATITUDE,
    LONGITUDE,
    'Australia/Brisbane',
    ELEVATION))


def update_twitter_status(twitter, status, media):
    response = twitter.upload_media(media=media)
    twitter.update_status(
        status=status,
        lat=LATITUDE,
        long=LONGITUDE,
        display_coordinates=True,
        place_id='0013cae44d65aff9',  # Townsville
        media_ids=[response['media_id']])


def capture_photo(filename, rotation=90, mode="auto", quality=15):
    """ Quality does not represent 'standard' JPEG quality.
    The resulting file will have 100 quality according to ImageMagick.
    """
    with picamera.PiCamera() as camera:

        camera.rotation = rotation
        camera.resolution = camera.MAX_RESOLUTION
        camera.exif_tags['GPS.GPSLatitude'] = LATITUDE_DMS
        camera.exif_tags['GPS.GPSLatitudeRef'] = LATITUDE_REF
        camera.exif_tags['GPS.GPSLongitude'] = LONGITUDE_DMS
        camera.exif_tags['GPS.GPSLongitudeRef'] = LONGITUDE_REF

        if mode == "auto":
            # Auto
            camera.shutter_speed = 0
            camera.exposure_mode = 'auto'
            camera.iso = 0
        elif mode == "day":
            # Daytime (for consistency)
            camera.brightness = 44
            camera.contrast = 20
            camera.shutter_speed = 0
            camera.exposure_mode = 'auto'
            camera.awb_mode = 'auto'
            camera.iso = 100
        elif mode == "night":
            # Nighttime
            camera.framerate = Fraction(1, 10)
            camera.shutter_speed = 1000000
            camera.exposure_mode = 'verylong'
            camera.awb_mode = 'fluorescent'
            camera.iso = 400

        time.sleep(5)
        camera.capture(filename, format='jpeg', quality=quality)


@begin.start(env_prefix='GTG_')
@begin.logging
def main(twitter_app_key, #: 'Twitter App Key',
         twitter_app_secret, #: 'Twitter App Secret',
         twitter_oauth_token, #: 'Twitter OAuth Token',
         twitter_oauth_token_secret, #: 'Twitter OAuth Token Secret',
         flickr_app_key, #: 'Flickr App Key',
         flickr_app_secret, #: 'Flickr App Secret',
         flickr_oauth_token, #: 'Flickr OAuth Token',
         flickr_oauth_token_secret, #: 'Flickr OAuth Token Secret',
         flickr_oauth_token_access_level, #: 'Flickr OAuth Token Access Level'='delete',
         image_path='.', #: 'Path to save images'='.',
         comments_path='./comments.yaml', #: 'Comments YAML file'='./comments.yaml',
         rotation=0, #: 'Camera rotation in degrees'=0,
         quality=15, #: 'Quality setting for GPU image processor'=15,
         test=False): #: 'Test photo capture only, no social media'=False):

    with open(comments_path, 'rb') as comments_file:
        comments = yaml.safe_load(comments_file)

    now = datetime.datetime.now(tz=tzlocal())
    
    if now >= LOCATION.dawn() and now <= LOCATION.dusk():
        camera_mode = 'day'
    else:
        camera_mode = 'night'

    if now.hour == 6:
        comment_mode = 'morning'
    elif now.hour >= 7 and now.hour <= 17:
        comment_mode = 'day'
    elif now.hour >= 18 and now.hour <= 20:
        comment_mode = 'evening'
    elif now.hour >= 21 or now.hour <= 5:
        comment_mode = 'night'

    logging.info('Starting photo capture')
    try:
        filename = os.path.join(
             image_path,
             '{timestamp:%Y-%m-%d-%H-%M}.jpg'.format(timestamp=now))
        capture_photo(filename,
                      mode=camera_mode,
                      rotation=rotation,
                      quality=int(quality))
    except Exception as e:
        logging.exception(e)
        exit(1)
    logging.info('Captured photo at ' + filename)

    if not test:
        logging.info('Starting photo sharing')
        try:
            random_status = random.choice(comments[comment_mode])
            twitter = Twython(
                twitter_app_key,
                twitter_app_secret,
                twitter_oauth_token,
                twitter_oauth_token_secret
            )
            with open(filename, 'rb') as photo:
                update_twitter_status(twitter=twitter, status=random_status, media=photo)
                logging.info('Tweeted the photo')
        except Exception as e:
            logging.exception(e)
    
        try:
            flickr_token = flickrapi.auth.FlickrAccessToken(
                unicode(flickr_oauth_token),
    	    unicode(flickr_oauth_token_secret),
    	    unicode(flickr_oauth_token_access_level))
            flickr = flickrapi.FlickrAPI(
                unicode(flickr_app_key),
                unicode(flickr_app_secret),
                token=flickr_token)
    
    
            response = flickr.upload(
                unicode(filename),
                title=now.isoformat(),
                tags='trees time-lapse raspberry-pi',
                is_public=1,
                content_type=1
            )
            logging.info('Uploaded photo to Flickr as photo ID %s' % response.find('photoid').text)
        except Exception as e:
            logging.exception(e)

    logging.info('All finished. See you soon!')
