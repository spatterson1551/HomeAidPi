import urllib, pycurl, os, requests, sys, subprocess

#functions
def downloadFile(url, fileName):
    subprocess.call(["wget", "-U", "Mozilla", url, "-O", "tts.mp3"])

def getGoogleSpeechURL(phrase):
    googleTranslateURL = "http://translate.google.com/translate_tts?tl=en&"
    parameters = {'q': phrase}
    data = urllib.urlencode(parameters)
    googleTranslateURL = "%s%s" % (googleTranslateURL, data)
    return googleTranslateURL

def speakSpeechFromText(phrase):
    googleSpeechURL = getGoogleSpeechURL(phrase)
    downloadFile(googleSpeechURL, "tts.mp3")
    #os.system("mplayer tts.mp3 -af extrastereo=0 &")
    subprocess.call(["mpg321", "tts.mp3"])#, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#end functions