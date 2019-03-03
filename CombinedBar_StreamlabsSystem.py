#---------------------------
#   Import Libraries
#---------------------------
import os
import codecs
import sys
import json
import csv
sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references


#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "CombinedProgressBar"
Website = "reecon820@gmail.com"
Description = "Progress bar for goals that combines streamlabs donations and cheers."
Creator = "Reecon820"
Version = "0.6.0.0"


#---------------------------
#   Settings Handling
#---------------------------
class CpbSettings:
    def __init__(self, settingsfile=None):
        try:
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
                self.__dict__ = json.load(f, encoding="utf-8")
        except:
            self.Title = ""
            self.Goal = 0
            self.Current = 0
            self.CurrentUpdate = False
            self.addToList = False
            self.cycleTime = 30
            self.handleListDone = "Show Latest Donation or Cheer"
            self.goalRepeat = "Do not repeat"

    def Reload(self, jsondata):
        #Parent.Log(ScriptName, jsondata)
        self.__dict__ = json.loads(jsondata, encoding="utf-8")

    def Save(self, settingsfile):
        try:
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="w+") as f:
                json.dump(self.__dict__, f, encoding="utf-8")
            with codecs.open(settingsfile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
                f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8')))
        except:
            Parent.Log(ScriptName, "Failed to save settings to file.")

#---------------------------
#   Define Global Variables
#---------------------------
global cpbSettingsFile
cpbSettingsFile = ""
global cpbScriptSettings
cpbScriptSettings = CpbSettings()

global cpbBarHtmlPath
cpbBarHtmlPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "Bar.html"))

global cpbBar2HtmlPath
cpbBar2HtmlPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "Bar2.html"))

global cpbBulkImportFilePath
cpbBulkImportFilePath = os.path.abspath(os.path.join(os.path.dirname(__file__), "bulk_goals.csv"))

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():
    #   Create Settings Directory
    directory = os.path.join(os.path.dirname(__file__), "Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #   Load settings
    global cpbSettingsFile
    cpbSettingsFile = os.path.join(os.path.dirname(__file__), "Settings\settings.json")
    global cpbScriptSettings
    cpbScriptSettings = CpbSettings(cpbSettingsFile)
    updateUi()

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
    #Parent.Log(ScriptName, jsonData)
    # Execute json reloading here
    cpbScriptSettings.Reload(jsonData)
    cpbScriptSettings.Save(cpbSettingsFile)
    updateUi()

    currentUpdate = 'true' if cpbScriptSettings.CurrentUpdate else 'false'
    
    addToList = 'true' if cpbScriptSettings.addToList else 'false'

    multiClear = cpbScriptSettings.goalRepeat

    handling = 'show_donor'
    if cpbScriptSettings.handleListDone == "Repeat Last Goal Indefinitely":
        handling = "repeat_goal"
    elif cpbScriptSettings.handleListDone == "Keep Last Goal Open Beyond 100%":
        handling = "keep_open"
    elif cpbScriptSettings.handleListDone == "Make Random Goal":
        handling = "random_goal"

    data = '{{"title": "{0}", "goal": {1}, "current": {2}, "currentUpdate": {3}, "addToList": {4}, "cycleTime": {5}, "listDoneHandling": "{6}", "multiClear": "{7}" }}'.format(cpbScriptSettings.Title, cpbScriptSettings.Goal, cpbScriptSettings.Current, currentUpdate, addToList, cpbScriptSettings.cycleTime, handling, multiClear)
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
    command = "echo " + cpbBarHtmlPath + "| clip"
    os.system(command)
    return

def CopyHtmlPath2():
    command = "echo " + cpbBar2HtmlPath + "| clip"
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

def ClearData():
    pass

def EditBulkFile():
    os.startfile(cpbBulkImportFilePath)

def ImportBulkData():
    try:
        with codecs.open(cpbBulkImportFilePath, encoding="utf-8-sig", mode="r") as f:
            # read semicolon separated CSV with format title;current;goal
            readCSV = csv.reader(f, delimiter=';')
            bulkJson = []
            for row in readCSV:
                goal = {'title': row[0], 'current': float(row[1]), 'goal': float(row[2])}
                bulkJson.append(goal)
                
            Parent.BroadcastWsEvent("EVENT_BULK_GOALS", json.dumps(bulkJson))
    except Exception as err:
        Parent.Log(ScriptName, "Error reading bulk file: {0}".format(err))

def updateUi():
    ui = {}
    UiFilePath = os.path.join(os.path.dirname(__file__), "UI_Config.json")
    try:
        with codecs.open(UiFilePath, encoding="utf-8-sig", mode="r") as f:
            ui = json.load(f, encoding="utf-8")
    except Exception as err:
        Parent.Log(ScriptName, "Error reading UI file: {0}".format(err))

    # update ui with loaded settings
    ui['Title']['value'] = cpbScriptSettings.Title
    ui['Goal']['value'] = cpbScriptSettings.Goal
    ui['Current']['value'] = cpbScriptSettings.Current
    ui['CurrentUpdate']['value'] = cpbScriptSettings.CurrentUpdate
    ui['addToList']['value'] = cpbScriptSettings.addToList
    ui['cycleTime']['value'] = cpbScriptSettings.cycleTime
    ui['handleListDone']['value'] = cpbScriptSettings.handleListDone
    ui['goalRepeat']['value'] = cpbScriptSettings.goalRepeat

    try:
        with codecs.open(UiFilePath, encoding="utf-8-sig", mode="w+") as f:
            json.dump(ui, f, encoding="utf-8", indent=4, sort_keys=True)
    except Exception as err:
        Parent.Log(ScriptName, "Error saving UI file: {0}".format(err))
    
    return