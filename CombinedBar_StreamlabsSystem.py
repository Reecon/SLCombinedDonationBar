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
Version = "0.3.1.0"

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

global GoalsPath
GoalsPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "goals.json"))

global goals
goals = {}

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

    LoadGoals()

    ui = {}
    UiFilePath = os.path.join(os.path.dirname(__file__), "UI_Config.json")
    try:
        with codecs.open(UiFilePath, encoding="utf-8-sig", mode="r") as f:
            ui = json.load(f, encoding="utf-8")
    except Exception as err:
        Parent.Log(ScriptName, "Error reading UI file: {0}".format(err))

    if len(goals) > 0:
        ScriptSettings.Title = goals["goals"][0]["title"]
        ScriptSettings.Goal = goals["goals"][0]["goal"]
        ScriptSettings.Current = goals["goals"][0]["current"]
        ScriptSettings.Save(SettingsFile)
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

    jsonObject = json.loads(jsonData)
    if jsonObject['addToList']:
        AddOrUpdateGoal(jsonData)

    # reload goals
    LoadGoals()

    # update overlay
    currentUpdate = "{0}".format(ScriptSettings.CurrentUpdate)
    currentUpdate = currentUpdate.lower() 

    # adding goals to the list takes priority over updating the current goal
    if jsonObject['addToList']:
        currentUpdate = 'false'
    
    newGoals = dict(goals)
    newGoals['currentUpdate'] = currentUpdate
    newGoals['cycleTime'] = jsonObject['CycleTime']
    data = json.dumps(newGoals)
    #data = '{{"title": "{0}", "goal": "{1}", "current": "{2}", "currentUpdate": {3} }}'.format(ScriptSettings.Title, ScriptSettings.Goal, ScriptSettings.Current, currentUpdate)
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

def LoadGoals():
    try:
        with codecs.open(GoalsPath, encoding="utf-8-sig", mode="r") as f:
            global goals
            goals = json.load(f, encoding="utf-8")
    except Exception as err:
        Parent.Log(ScriptName, "Error reading goals file: {0}".format(err))
    return


def AddOrUpdateGoal(jsonString):
    jsonData = json.loads(jsonString)
    newGoal = {"title": jsonData["Title"], "goal": jsonData["Goal"], "current": jsonData["Current"]}
    
    updated = False

    # look if new goal already exists and update if it does
    for goal in goals['goals']:
        if goal['title'] == newGoal['title']:
            goal['goal'] = newGoal['goal']
            goal['current'] = newGoal['current']
            updated = True

    # if goal value is 0 remove this goal. goal in list is same as newGoal if it was updated
    if newGoal['goal'] == 0 and updated:
        goals['goals'].remove(newGoal)

    # if no goal was updated this is a new goal. so append it to the list
    if not updated:
        goals['goals'].append(newGoal)

    SaveGoals()
    return

def SaveGoals():
    try:
        with codecs.open(GoalsPath, encoding="utf-8-sig", mode="w+") as f:
            json.dump(goals, f, encoding="utf-8", indent=4, sort_keys=True)
    except Exception as err:
        Parent.Log(ScriptName, "Error saving goals file: {0}".format(err))
    return

def OpenListFile():
    os.startfile(GoalsPath)
    return