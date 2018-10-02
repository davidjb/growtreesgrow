About this project
==================

This project has a very simple goal: to use the Raspberry Pi camera, take a
photo, and upload it to several different social media services (Twitter and
Flickr).  It is to be run periodically to eventually produce a timelapse after
being run for months or years, and probably catch some interesting activity
in the meantime.

In particular, this is being used to power http://twitter.com/growtreesgrow,
and https://www.flickr.com/photos/growtreesgrow, accounts dedicated to
watching trees grow in Australia.

This is powered by Python and designed exclusively for use on a Raspberry Pi.
It adjusts camera settings based upon whether it's night or day (based on
dawn/dusk times) so as the camera can keep functioning through the night.

The photo metadata is currently hard-coded into the script for simplicity, 
but I'm happy to refactor and genercise the code if anyone's interested.
Feel free to extend/fork/hack as you will otherwise!

Install
=======

::

    git clone https://github.com/davidjb/growtreesgrow.git
    cd growtreesgrow
    virtualenv . -p /usr/bin/python
    source ./bin/active
    pip install .

Now, you'll have an ``upload-pi-photo`` script available in your path (``bin/upload-pi-photo``).

This is compatible with Python 2.7 for now.  Python 3 support would have been possible except
the current Raspian release has only version 3.2, whilst most Python libraries are
3.3+ compatible.

Getting started
===============

* Create a Twitter account, enable geolocation in your account's settings

* Create a Twitter app, and follow the OAuth procedure below in an interactive
  Python session::

      APP_KEY='xxxxxxxxxxxxxxxxxxxxxxxxx'
      APP_SECRET='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
      twitter = Twython(APP_KEY, APP_SECRET)
      auth = twitter.get_authentication_tokens()
      OAUTH_TOKEN = auth['oauth_token']
      OAUTH_TOKEN_SECRET = auth['oauth_token_secret']
      print(auth['auth_url'])

  Now go to the URL that was printed, authenticate, get the code and set it as
  ``oauth_verifier``::

      oauth_verifier='1234567'
      twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
      final_step = twitter.get_authorized_tokens(oauth_verifier)
      OAUTH_TOKEN = final_step['oauth_token']
      OAUTH_TOKEN_SECRET = final_step['oauth_token_secret']

  Save the values of ``OAUTH_TOKEN`` and ``OAUTH_TOKEN_SECRET`` somewhere so they
  can be used again.  These credentials will grant your application access to your
  user account for posting tweets or performing other actions.

* Tweets should be posted like so, with this specific location and Place ID::

      twitter.update_status(status="Test", lat=-19.3189578, long=146.7376072,
                            display_coordinates=True,  place_id='0013cae44d65aff9')
References
==========

* EXIF GPS data: http://www.opanda.com/en/pe/help/gps.html#GPSLatitude

TODO
====

* Begins has a problem whereby it doesn't read environment variables 
  either for positional args or for args with defaults.  Why?

* Begins: ``env_prefix`` is required -- need to document this
