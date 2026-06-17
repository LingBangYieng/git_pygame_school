import json


class Settings:

    def __init__(self, settingDictOverride=None):
        if settingDictOverride is None:
            with open("settings.json", "r") as f:
                settings = json.load(f)
        else:
            settings = settingDictOverride
        
        user_settings = settings["User"]
        engine_settings = settings["Engine"]
    
        self.MAX_FPS = user_settings["MAX_FPS"]
        self.SFX_VOLUME = user_settings["SFX_VOLUME"]
        self.RESOLUTION = user_settings["RESOLUTION"]
        self.FULLSCREEN = user_settings["FULLSCREEN"]

        self.fov_degr = engine_settings["fov_degr"]
        self.CellSize = engine_settings["CellSize"]
        self.GameScale = engine_settings["GameScale"]




        self.__savedSettings = {}
        # self.saveSettings()

    @property
    def WIDTH(self):
        return int(self.RESOLUTION.split("x")[0]  )  
        
    @property
    def HEIGHT(self):
        return int(self.RESOLUTION.split("x")[1])



    def saveSettings(self):
        user_saveSettings = {}
        engine_saveSettings = {}

        self.__savedSettings["User"] = user_saveSettings
        self.__savedSettings["Engine"] = engine_saveSettings
    
        user_saveSettings["MAX_FPS"] = self.MAX_FPS    
        user_saveSettings["SFX_VOLUME"] = self.SFX_VOLUME 
        user_saveSettings["RESOLUTION"] = self.RESOLUTION 
        user_saveSettings["FULLSCREEN"] = self.FULLSCREEN 

        engine_saveSettings["fov_degr"] = self.fov_degr   
        engine_saveSettings["CellSize"] = self.CellSize   
        engine_saveSettings["GameScale"] = self.GameScale

    def discardSettings(self):
        self.__init__(self.__savedSettings)


    def __updateClass(self):
        self.__init__()
    

    def applySettings(self):
        print(self.RESOLUTION)
        self.saveSettings()
        print(self.saveSettings)
        with open("settings.json", "w") as f:
            json.dump(self.__savedSettings, f, indent=4)
        self.__updateClass()





