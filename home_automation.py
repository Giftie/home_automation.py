# This module's future home should be inside userdata/addon_data/script.cinema.experience/ha_scripts
# to make sure it does not get over written when updating the script

import xbmc, xbmcaddon
import sys, urllib2, os, requests
from threading import Thread
from urllib import urlencode
from requests.auth import HTTPBasicAuth


__script__               = sys.modules[ "__main__" ].__script__
__scriptID__             = sys.modules[ "__main__" ].__scriptID__
triggers                 = sys.modules[ "__main__" ].triggers
ha_settings              = sys.modules[ "__main__" ].ha_settings
BASE_RESOURCE_PATH       = sys.modules["__main__"].BASE_RESOURCE_PATH
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
import utils

lights_pause = "02610511FF"
lights_movie = "02610611FF"
lights_start = "02610411FF"
lights_end   = "02610311FF"

class Automate:
    def __init__( self ):
        pass

    def insteon_direct( self, ip = "0.0.0.0", port = "25105", username = "", password = "", command = "" ):
        auth=HTTPBasicAuth( username, password )
        url = u'http://%s:%s/3?%s=I=3' % ( ip, port, command )
        utils.log( url )
        r = requests.post(url=url, auth=auth)
    
    def sab_pause(self, mode):
        apikey = ""
        ip = "127.0.0.1" # address 
        port = "5000"
        url = "http://%s:%s/sabnzbd/" % ( ip, port )
        query = {}
        query[ "mode" ] = mode
        query["apikey"] = apikey
        response = urllib2.urlopen( urllib2.Request( url + "api?", urlencode( query ) ) )
        response_data = response.read()
      
    def activate_ha( self, trigger = None, prev_trigger = None, mode="normal" ):
        if ha_settings[ "ha_enable" ]:
            if ha_settings[ "ha_multi_trigger" ] and prev_trigger == trigger:
                pass
            elif mode != "thread":
                self.activate_on( trigger )
            else:
                thread = Thread( name='ha_trigger', target=self.activate_on, args=( trigger, ) )
                thread.start()
            prev_trigger = trigger
        return prev_trigger

    def activate_on( self, trigger = None ):
        """
            Scripting to trigger almost anything(HA, other scripts, etc...) when videos start.  
            
            Usage:
                activate_on( "Movie" )
                will trigger code that is set under the Movie heading.
                
        """
        if not trigger:
            utils.log( " - [ home_automation.py ] - No Trigger Sent, Returning", xbmc.LOGNOTICE )
            return
        utils.log( " - [ home_automation.py ] - activate_on( %s ) Triggered" % trigger, xbmc.LOGNOTICE )
        if trigger in triggers:
            utils.log( " - [ home_automation.py ] - Trigger %s" % trigger, xbmc.LOGNOTICE )
        # Script Start
        if trigger == "Script Start" and ha_settings[ "ha_script_start" ]: 
            # place code below this line
            self.insteon_direct( ip = "192.168.2.9", port = "25105", username = "admin", password = "gmracing", command = lights_start )
        # Trivia Intro
        elif trigger == "Trivia Intro" and ha_settings[ "ha_trivia_intro" ]: 
            # place code below this line
            pass
        # Trivia
        elif trigger == "Trivia" and ha_settings[ "ha_trivia_start" ]: 
            # place code below this line
            pass
        # Trivia Outro
        elif trigger == "Trivia Outro" and ha_settings[ "ha_trivia_outro" ]:
            # place code below this line
            pass
        # Movie Theatre Intro
        elif trigger == "Movie Theater Intro" and ha_settings[ "ha_mte_intro" ]:
            # place code below this line
            pass
        # Coming Attractions Intro
        elif trigger == "Coming Attractions Intro" and ha_settings[ "ha_cav_intro" ]:
            # place code below this line
            pass
        # Trailer
        elif trigger == "Movie Trailer" and ha_settings[ "ha_trailer_start" ]:
            # place code below this line
            pass
        # Coming Attractions Outro
        elif trigger == "Coming Attractions Outro" and ha_settings[ "ha_cav_outro" ]: 
            # place code below this line
            pass
        # Feature Presentation Intro
        elif trigger == "Feature Presentation Intro" and ha_settings[ "ha_fpv_intro" ]: 
            # place code below this line
            pass
        # MPAA Rating
        elif trigger == "MPAA Rating" and ha_settings[ "ha_mpaa_rating" ]: 
            # place code below this line
            pass
        # Countdown
        elif trigger == "Countdown" and ha_settings[ "ha_countdown_video" ]:
            # place code below this line
            pass
        # Audio Format
        elif trigger == "Audio Format" and ha_settings[ "ha_audio_format" ]:
            # place code below this line
            pass
        # Movie
        elif trigger == "Movie" and ha_settings[ "ha_movie" ]: 
            # place code below this line
            self.insteon_direct( ip = "192.168.2.9", port = "25105", username = "admin", password = "gmracing", command = lights_movie )
        # Feature Presentation Outro
        elif trigger == "Feature Presentation Outro" and ha_settings[ "ha_fpv_outro" ]:
            # place code below this line
            pass
        # Movie Theatre Intro
        elif trigger == "Movie Theatre Outro" and ha_settings[ "ha_mte_outro" ]: 
            # place code below this line
            pass
        # Intermission
        elif trigger == "Intermission" and ha_settings[ "ha_intermission" ]: 
            # place code below this line
            pass
        # Script End
        elif trigger == "Script End" and ha_settings[ "ha_script_end" ]: 
            # place code below this line
            self.insteon_direct( ip = "192.168.2.9", port = "25105", username = "admin", password = "gmracing", command = lights_end )
        # Paused
        elif trigger == "Pause" and ha_settings[ "ha_paused" ]: 
            # place code below this line
            self.insteon_direct( ip = "192.168.2.9", port = "25105", username = "admin", password = "gmracing", command = lights_pause )
        # Resumed
        elif trigger == "Resume" and ha_settings[ "ha_resumed" ]: 
            # place code below this line
            self.insteon_direct( ip = "192.168.2.9", port = "25105", username = "admin", password = "gmracing", command = lights_movie )
        else:
            utils.log( " - [ home_automation.py ] - Opps. Something happened", xbmc.LOGNOTICE )
