# This module's future home should be inside userdata/addon_data/script.cinema.experience/ha_scripts
# to make sure it does not get over written when updating the script

import xbmc, xbmcaddon
import sys, urllib2, os
import decimal
from threading import Thread
from urllib import urlencode
if sys.version_info < (2, 7):
    import simplejson
else:
    import json as simplejson
    
__script__               = sys.modules[ "__main__" ].__script__
__scriptID__             = sys.modules[ "__main__" ].__scriptID__
triggers                 = sys.modules[ "__main__" ].triggers
ha_settings              = sys.modules[ "__main__" ].ha_settings
BASE_RESOURCE_PATH       = sys.modules["__main__"].BASE_RESOURCE_PATH
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
import utils

class Automate:
    def __init__( self ):
        pass
        
    def retrieve_aspect_ratio( self ):
        # returns 
        utils.log( "Retrieving Movie Aspect Ratio", xbmc.LOGNOTICE )
        aspect_ratio = 1.78
        playerid_query = '{"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1}'
        jsonresponse = xbmc.executeJSONRPC( playerid_query )
        data = simplejson.loads( jsonresponse )
        if data.has_key('result'):
            if data['result'].has_key('playerid'):
                playerid = int( data['result']['playerid'] )
                json_query = '{"jsonrpc": "2.0", "method": "Player.GetItem", "params": { "playerid": %d, "properties": [ "streamdetails" ]}, "id": 1}' % playerid
                jsonresponse = xbmc.executeJSONRPC( json_query )
                data = simplejson.loads( jsonresponse )
                if data.has_key('result'):
                    if data['result'].has_key('item'):
                        movie_detail = data['result']['item']
                        try:
                            aspect_ratio = float( movie_detail['streamdetails']['video'][0]['aspect'] )
                        except:
                            utils.log( "Error getting streamdetails:", xbmc.LOGDEBUG )
                            utils.log( movie_detail, xbmc.LOGDEBUG )
            else:
                pass
        # convert the supplied aspect ratio to a value with two decimal places
        movie_aspect = decimal.Decimal(aspect_ratio).quantize(decimal.Decimal('.01'), rounding=decimal.ROUND_DOWN)
        return movie_aspect
    
    def sab_pause(self, mode):
        apikey = ""
        ip = "127.0.0.1" # address 
        port = "5000"
        url = "http://%s:%s/sabnzbd/" % ( ip, port )
        query = {}
        query[ "mode" ] = mode
        query[ "apikey" ] = apikey
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
            utils.broadcastUDP( "<b>CE_Automate<li>script_start</b>" )
        # Trivia Intro
        elif trigger == "Trivia Intro" and ha_settings[ "ha_trivia_intro" ]:
            utils.broadcastUDP( "<b>CE_Automate<li>trivia_intro</b>" )
        # Trivia
        elif trigger == "Trivia" and ha_settings[ "ha_trivia_start" ]: 
            utils.broadcastUDP( "<b>CE_Automate<li>triva_start</b>" )
        # Trivia Outro
        elif trigger == "Trivia Outro" and ha_settings[ "ha_trivia_outro" ]:
            utils.broadcastUDP( "<b>CE_Automate<li>trivia_outro</b>" )
        # Movie Theatre Intro
        elif trigger == "Movie Theater Intro" and ha_settings[ "ha_mte_intro" ]:
            utils.broadcastUDP( "<b>CE_Automate<li>movie_theatre_intro</b>" )
        # Coming Attractions Intro
        elif trigger == "Coming Attractions Intro" and ha_settings[ "ha_cav_intro" ]:
            utils.broadcastUDP( "<b>CE_Automate<li>coming_attractions_intro</b>" )
        # Trailer
        elif trigger == "Movie Trailer" and ha_settings[ "ha_trailer_start" ]:
            utils.broadcastUDP( "<b>CE_Automate<li>trailer</b>" )
        # Coming Attractions Outro
        elif trigger == "Coming Attractions Outro" and ha_settings[ "ha_cav_outro" ]: 
            utils.broadcastUDP( "<b>CE_Automate<li>coming_attractions_outro</b>" )
        # Feature Presentation Intro
        elif trigger == "Feature Presentation Intro" and ha_settings[ "ha_fpv_intro" ]: 
            utils.broadcastUDP( "<b>CE_Automate<li>feature_intro</b>" )
        # MPAA Rating
        elif trigger == "MPAA Rating" and ha_settings[ "ha_mpaa_rating" ]: 
            utils.broadcastUDP( "<b>CE_Automate<li>mpaa_rating</b>" )
        # Countdown
        elif trigger == "Countdown" and ha_settings[ "ha_countdown_video" ]:
            utils.broadcastUDP( "<b>CE_Automate<li>countdown_video</b>" )
        # Audio Format
        elif trigger == "Audio Format" and ha_settings[ "ha_audio_format" ]:
            utils.broadcastUDP( "<b>CE_Automate<li>audio_video</b>" )
        # Movie
        elif trigger == "Movie" and ha_settings[ "ha_movie" ]: 
            utils.broadcastUDP( "<b>CE_Automate<li>movie_start</b>" )
            aspect_ratio = self.retrieve_aspect_ratio
            if aspect_ratio == decimal.Decimal( 1.33 ):
                # really 4x3 hmmm....
            elif aspect_ratio == decimal.Decimal( 1.77 ):
                # now we're talking, 16x9
            elif aspect_ratio == decimal.Decimal( 2.35 ):
                # anamorphic
            elif aspect_ratio == decimal.Decimal( 2.40 ):
                # still anamorphic
            else:
                # nothing matched yet.
        # Feature Presentation Outro
        elif trigger == "Feature Presentation Outro" and ha_settings[ "ha_fpv_outro" ]:
            utils.broadcastUDP( "<b>CE_Automate<li>feature_outro</b>" )
        # Movie Theatre Intro
        elif trigger == "Movie Theatre Outro" and ha_settings[ "ha_mte_outro" ]: 
            utils.broadcastUDP( "<b>CE_Automate<li>movie_theatre_outro</b>" )
        # Intermission
        elif trigger == "Intermission" and ha_settings[ "ha_intermission" ]: 
            utils.broadcastUDP( "<b>CE_Automate<li>intermission</b>" )
        # Script End
        elif trigger == "Script End" and ha_settings[ "ha_script_end" ]: 
            utils.broadcastUDP( "<b>CE_Automate<li>script_end</b>" )
        # Paused
        elif trigger == "Pause" and ha_settings[ "ha_paused" ]: 
            utils.broadcastUDP( "<b>CE_Automate<li>paused</b>" )
        # Resumed
        elif trigger == "Resume" and ha_settings[ "ha_resumed" ]: 
            utils.broadcastUDP( "<b>CE_Automate<li>resumed</b>" )
        else:
            utils.log( " - [ home_automation.py ] - Opps. Something happened", xbmc.LOGNOTICE )
        