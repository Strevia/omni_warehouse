import os, platform
import random
import omni.ext
import omni.ui as ui
from omni.ui.workspace_utils import RIGHT
from pxr import Usd, UsdGeom, UsdLux, Gf
from .recipes import warehouse_recipe as wh_rec


class wh_helpers():
    def __init__(self):
        NUCLEUS_SERVER = "http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/ArchVis/Industrial/"
        isTest = False
        self._system = platform.system()
        self.mode = "procedural"
        self.objects = ["empty_racks", "filled_racks", "piles", "railings", "forklift", "robot"]
        self.objectDict = self.initAssetPositions()
        self.objDictList = list(self.objectDict)
        self.isaacSimScale = Gf.Vec3f(100, 100,100)

        # Shell info is hard-coded for now
        self.shell_path = f"{NUCLEUS_SERVER}Buildings/Warehouse/Warehouse01.usd"
        self.shell_translate = (0, 0, 55.60183)
        self.shell_rotate = (-90.0, 0.0, 0.0)
        self.shell_name = "WarehouseShell"

    def config_environment(self):
        for prim in self._stage.Traverse():
            if '/Environment/' in str(prim):
                prim.SetActive(False)
        self.create_distant_light()

    def create_distant_light(self):
        environmentPath = '/Environment'
        lightPath = environmentPath + '/distantLight'
        prim = self._stage.DefinePrim(environmentPath, 'Xform')
        distLight = UsdLux.DistantLight.Define(self._stage, lightPath)
        distLight.AddRotateXYZOp().Set(Gf.Vec3f(315,0,0))
        distLight.CreateColorTemperatureAttr(6500.0)
        if self._system == "Linux":
            distLight.CreateIntensityAttr(6500.0)
        else:
            distLight.CreateIntensityAttr(3000.0)
        distLight.CreateAngleAttr(1.0)
        lightApi = UsdLux.ShapingAPI.Apply(distLight.GetPrim())
        lightApi.CreateShapingConeAngleAttr(180)

    # Spawning warehouse shell when the button is clicked
    def genShell(self):
        self.clear_stage()
        self.mode = "procedural"
        self.spawn_prim(self.shell_path, self.shell_translate, self.shell_rotate, self.shell_name)

    # Generate Warehouse w/ user-selected assets
    def gen_custom(self, isProcedural, mode, objectButtons):
        self.mode = mode

        # Create shell
        self.spawn_prim(self.shell_path, self.shell_translate, self.shell_rotate, self.shell_name)
        selected_obj = []

        # Spawn all objects (procedural) or user-selected objects
        if isProcedural:
            selected_obj = self.objects
        else:
            for i in range(len(objectButtons)):
                if objectButtons[i].checked == True:
                    identifier = {
                        0: "empty_racks",
                        1: "filled_racks",
                        2: "piles",
                        3: "railings",
                        4: "forklift",
                        5: "robot",
                    }
                    selected_obj.append(identifier.get(i))
        objectUsdPathDict = {"empty_racks": [],
                             "filled_racks":[],
                             "piles":[],
                             "railings":[],
                             "forklift":[],
                             "robot":[]
                            }
        # Reserved spots are dependent on self.mode (i.e. layout)
        numForkLifts = len(wh_rec[self.objects[4] + "_" + self.mode])
        spots2RsrvFL = numForkLifts - 1
        numRobots = len(wh_rec[self.objects[5] + "_" + self.mode])
        spots2RsrvRob = numRobots - 1
        self.objParams = {"empty_racks": [(-90,-180,0), (1,1,1), 5],
                          "filled_racks":[(-90,-180,0), (1,1,1), 5],
                          "piles":[(-90,-90,0), (1,1,1), 5],
                          "railings":[(-90,0,0), (1,1,1), 5],
                          "forklift":[(-90, random.uniform(0, 90), 0), self.isaacSimScale, spots2RsrvFL],
                          "robot":[(-90, random.uniform(0, 90), 0), self.isaacSimScale, spots2RsrvRob]
                        }
        # Reserve spots for Smart Import feature
        for h in range(0,len(selected_obj)):
            for i in range(0, len(self.objDictList)):
                if selected_obj[h] == self.objDictList[i]:
                    for j in wh_rec[selected_obj[h] + "_asset"]:
                        objectUsdPathDict[self.objDictList[i]].append(wh_rec[selected_obj[h]] + j)
                    rotation = self.objParams[self.objDictList[i]][0]
                    scale = self.objParams[self.objDictList[i]][1]
                    spots2Rsrv = self.objParams[self.objDictList[i]][2]
                    self.objectDict[self.objDictList[i]] = self.reservePositions(objectUsdPathDict[self.objDictList[i]], selected_obj[h], rotation, scale, spots2Rsrv)

    # Function to reserve spots/positions for Smart Import feature (after initial generation of assets)
    def reservePositions(self, assets, asset_prefix, rotation = (0,0,0), scale = (1,1,1), spots2reserve = 5):
        if len(assets) > 0:
            rotate = rotation
            scale = scale
            all_translates = wh_rec[asset_prefix + "_" + self.mode]
            #Select all but 5 positions from available positions (reserved for Smart Import functionality)
            if spots2reserve >= len(all_translates) and len(all_translates) > 0:
                spots2reserve = len(all_translates) - 1
            elif len(all_translates) == 0:
                spots2reserve = 0
            reserved_positions = random.sample(all_translates, spots2reserve)
            translates = [t for t in all_translates if t not in reserved_positions]
            positions = reserved_positions
        for i in range(len(translates)):
            name = asset_prefix + str(i)
            path = random.choice(assets)
            translate = translates[i]
            self.spawn_prim(path, translate, rotate, name, scale)
        return positions

    # Smart Import
    def smart_import(self, pathString, importCategory):
        self.get_root()
        # Get chosen index from drop-down
        import_index = importCategory.model.get_item_value_model().get_value_as_int()
        selected = self.objDictList[import_index] #ToDo: should idx dropdown list
        path = pathString.get_value_as_string()
        scale = Gf.Vec3f(1.0, 1.0, 1.0)
        # Scale if contains Isaac Sim Path (these assets are typically in meters vs centimeters)
        if "isaac" in path.lower():
            scale = self.isaacSimScale
        # If positions available, spawn selected asset
        notificationMsg = "No more available positions to spawn new asset"
        for idx in range(0,len(self.objectDict)):
            if selected in self.objDictList[idx]:
                if len(self.objectDict[self.objDictList[idx]]) != 0:
                    translate = self.objectDict[self.objDictList[idx]].pop()
                    break
                else:
                    self.windowNum = self.notification_window("window", "Smart Import", notificationMsg)
                    return
        pathName = os.path.basename(path).split(".")[0]
        if pathName == "transporter":
            pathName = "robot"
        existing_assets = []
        world = self._stage.GetDefaultPrim()
        for i in world.GetChildren():
            existing_assets.append(i.GetPath())
        # If prim exists, add count suffix and spawn
        counter = 0
        assetName = pathName + str(counter)
        while f"/World/{assetName}" in existing_assets:
            assetName = f"{pathName}" + str(counter)
            counter += 1
        pathName = assetName
        rotate = (-90.0, 0.0, 0.0)
        self.spawn_prim(path, translate, rotate, pathName, scale)
        pathString.set_value("")

    # spawn_prim function takes in a path, XYZ position, orientation, a name and spawns the USD asset in path with
    # the input name in the given position and orientation inside the world prim as an XForm
    def spawn_prim(self, path, translate, rotate, name, scale=Gf.Vec3f(1.0, 1.0, 1.0)):
        world = self._stage.GetDefaultPrim()
        # Creating an XForm as a child to the world prim
        asset = UsdGeom.Xform.Define(self._stage, f"{str(world.GetPath())}/{name}")
        # Checking if asset already has a reference and clearing it
        asset.GetPrim().GetReferences().ClearReferences()
        # Adding USD in the path as reference to this XForm
        asset.GetPrim().GetReferences().AddReference(f"{path}")
        # Setting the Translate and Rotate
        UsdGeom.XformCommonAPI(asset).SetTranslate(translate)
        UsdGeom.XformCommonAPI(asset).SetRotate(rotate)
        UsdGeom.XformCommonAPI(asset).SetScale(scale)
        # Returning the Xform if needed
        return asset

    def initAssetPositions(self):
        dictAssetPositions = {
            "empty_racks": wh_rec["empty_racks" + "_" + self.mode],
            "filled_racks": wh_rec["filled_racks" + "_" + self.mode],
            "piles": wh_rec["piles" + "_" + self.mode],
            "railings": wh_rec["railings" + "_" + self.mode],
            "forklift": wh_rec["forklift" + "_" + self.mode],
            "robot": wh_rec["robot" + "_" + self.mode]
        }
        return dictAssetPositions

    # Clear stage function
    def clear_stage(self):
        #Removing all children of world except distant light
        self.get_root()
        world = self._stage.GetDefaultPrim()
        doesLightExist = self._stage.GetPrimAtPath('/Environment/distantLight').IsValid()
        # config environment
        if doesLightExist == False:
            self.config_environment()
        # clear scene
        for i in world.GetChildren():
            if i.GetPath() == '/Environment/distantLight' or i.GetPath() == '/World':
                continue
            else:
                self._stage.RemovePrim(i.GetPath())

    # Notification window
    def notification_window(self,windowNum, textWindow, textField):
        windowNum = ui.Window(textWindow, width=400, height=100)
        with windowNum.frame:
            with ui.VStack():
                ui.Label(textField)
        return windowNum

    # gets stage
    def get_root(self):
        self._stage = omni.usd.get_context().get_stage()