#---------------------------
#   Import Libraries
#---------------------------
import os
import codecs
import sys
import json
sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references

#   Import your Settings class
from Settings_Module import MySettings
#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "CombinedProgressBar"
Website = "reecon820@gmail.com"
Description = "Progress bar for goals that combines streamlabs donations and cheers."
Creator = "Reecon820"
Version = "0.4.1.0"

#---------------------------
#   Define Global Variables
#---------------------------
global SettingsFile
SettingsFile = ""
global ScriptSettings
ScriptSettings = MySettings()

global BarHtmlPath
BarHtmlPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "Bar.html"))

global Bar2HtmlPath
Bar2HtmlPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "Bar2.html"))

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():
    #   Create Settings Directory
    directory = os.path.join(os.path.dirname(__file__), "Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #   Load settings
    global SettingsFile
    SettingsFile = os.path.join(os.path.dirname(__file__), "Settings\settings.json")
    global ScriptSettings
    ScriptSettings = MySettings(SettingsFile)
    Parent.Log(ScriptName, "{}".format(ScriptSettings.__dict__))
    ui = {}
    UiFilePath = os.path.join(os.path.dirname(__file__), "UI_Config.json")
    try:
        with codecs.open(UiFilePath, encoding="utf-8-sig", mode="r") as f:
            ui = json.load(f, encoding="utf-8")
    except Exception as err:
        Parent.Log(ScriptName, "Error reading UI file: {0}".format(err))

    # update ui with loaded settings
    ui['Title']['value'] = ScriptSettings.Title
    ui['Goal']['value'] = ScriptSettings.Goal
    ui['Current']['value'] = ScriptSettings.Current
    ui['CurrentUpdate']['value'] = ScriptSettings.CurrentUpdate
    ui['addToList']['value'] = ScriptSettings.addToList
    ui['CycleTime']['value'] = ScriptSettings.CycleTime

    try:
        with codecs.open(UiFilePath, encoding="utf-8-sig", mode="w+") as f:
            json.dump(ui, f, encoding="utf-8", indent=4, sort_keys=True)
    except Exception as err:
        Parent.Log(ScriptName, "Error saving UI file: {0}".format(err))

    return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):
    # all logic in overlay
    return

#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
    return

#---------------------------
#   [Optional] Parse method (Allows you to create your own custom $parameters) 
#---------------------------
def Parse(parseString, userid, username, targetid, targetname, message):
    return parseString

#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings(jsonData):
    Parent.Log(ScriptName, jsonData)
    # Execute json reloading here
    ScriptSettings.Reload(jsonData)
    ScriptSettings.Save(SettingsFile)

    currentUpdate = 'true' if ScriptSettings.CurrentUpdate else 'false'
    
    addToList = 'true' if ScriptSettings.addToList else 'false'

    data = '{{"title": "{0}", "goal": {1}, "current": {2}, "currentUpdate": {3}, "addToList": {4}, "cycleTime": {5} }}'.format(ScriptSettings.Title, ScriptSettings.Goal, ScriptSettings.Current, currentUpdate, addToList, ScriptSettings.CycleTime)
    Parent.BroadcastWsEvent("EVENT_BAR_UPDATE", data)

    return

#---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
#---------------------------
def Unload():
    return

#---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
#---------------------------
def ScriptToggled(state):
    return

def CopyHtmlPath1():
    command = "echo " + BarHtmlPath + "| clip"
    os.system(command)
    return

def CopyHtmlPath2():
    command = "echo " + Bar2HtmlPath + "| clip"
    os.system(command)
    return

def TestBits():
    data = '{"name": "test", "display_name": "Test", "bits": 1337, "total_bits": 4711, "message": "cheer1337" }'
    Parent.BroadcastWsEvent("EVENT_CHEER", data)
    return

def TestDonation():
    data = '{"userId": "1234567", "name": "tester", "display_name": "Tester", "amount": "69.69", "currency": "USD", "message": "giggity" }'
    Parent.BroadcastWsEvent("EVENT_DONATION", data)
    return
