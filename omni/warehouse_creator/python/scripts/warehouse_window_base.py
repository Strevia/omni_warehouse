import os, platform
import omni.ext
import omni.ui as ui
from omni.ui.workspace_utils import RIGHT
from .warehouse_helpers import *
import carb
WINDOW_TITLE = "Warehouse Creator"

class WarehouseCreatorWindow():

    def __init__(self):
        # Render Setting; Enable ambient lighting
        self._system = platform.system()
        carb.settings.get_settings().set("/rtx/sceneDb/ambientLightIntensity", 1.5)
        if self._system == "Linux":
            carb.settings.get_settings().set("/rtx/indirectDiffuse/scalingFactor", 10.0)

        from os.path import dirname, abspath
        path =  dirname(dirname(dirname(dirname(dirname(__file__)))))
        path = path + "/data/UI/"
        self.UI_IMAGE_SERVER = path
        self._usd_context = omni.usd.get_context()
        self._wh_helper = wh_helpers()

        # Main extension window (Width is 0 to fit the window to UI elements)
        self._window = ui.Window(WINDOW_TITLE, width=0, height=800)
        self._window.deferred_dock_in("Stage", ui.DockPolicy.CURRENT_WINDOW_IS_ACTIVE)


    def destroy(self):
        # Render Setting; Disable ambient lighting (default)
        carb.settings.get_settings().set("/rtx/sceneDb/ambientLightIntensity", 0.0)
        carb.settings.get_settings().set("/rtx/indirectDiffuse/scalingFactor", 1.0)
        self._window = None

    # U S E R       I N T E R F A C E
    def _build_content(self, runTestScript = False):
        # Elements within the window frame
        with self._window.frame:

            # General UI Styling
            style1 = {
                "Button:hovered": {"background_color": 0xFF00B976, "border_color": 0xFFFD761D},
                "Button": {},
                "Button.Label": {"color": 0xFF00B976},
                "Button.Label:hovered": {"color": 0xFFFFFFFF},
            }

            # UI elements in a main VStack
            with ui.VStack(style=style1):

                # Main title label
                titleLabel = ui.Label(
                    "Warehouse Creator",
                    style={"color": 0xFF00B976, "font_size": 35},
                    alignment=ui.Alignment.CENTER,
                    height=0,
                )
                titleDescriptionLabel = ui.Label(
                    "\nWelcome to the Warehouse Creator Extension! Quickly get started with building your\nwarehouse scenes with a click of a button. For more detailed guide on quickly getting\nstarted with building scenes, checkout our official documentation here: \n\n",
                    width=500,
                    alignment=ui.Alignment.CENTER,
                )

                # Quick Generation label
                quickgenLabel = ui.Label(
                    "Option 1. Quick Generation",
                    alignment=ui.Alignment.CENTER,
                    width=500,
                    style={"color": 0xFF00B976, "font_size": 25},
                )
                quickgenDescriptionLabel1 = ui.Label(
                    "\nQuick Generation module allows you to quickly generate your warehouse scene w/o\nany parameters. You can choose to begin with a standalone warehouse shell, to bring\n in your own assets to populate your scene!\n\n",
                    width=500,
                    alignment=ui.Alignment.CENTER,
                )

                # G E N E R A T E       W A R E H O U S E       S H E L L
                with ui.VStack():
                    shellImage = ui.Image(
                        f"{self.UI_IMAGE_SERVER}shell.JPG",
                        width=500,
                        height=150,
                    )
                    shellImage.fill_policy = shellImage.fill_policy.PRESERVE_ASPECT_CROP

                    # Spawning warehouse shell when the button is clicked
                    def generateShell():
                        self.layoutButton1.checked = False
                        self.layoutButton2.checked = False
                        self.layoutButton3.checked = False
                        self.objectButton1.checked = False
                        self.objectButton2.checked = False
                        self.objectButton3.checked = False
                        self.objectButton4.checked = False
                        self.objectButton5.checked = False
                        self.objectButton6.checked = False
                        self._wh_helper.genShell()

                    shellButton = ui.Button(
                        "Generate Warehouse Shell",
                        clicked_fn=lambda: generateShell(),
                        width=500,
                        height=40,
                        tooltip="Generates an empty warehouse shell",
                    )

                quickgenDescriptionLabel2 = ui.Label(
                    "\nYou can also quickly create a full, procedurally generated warehouse scene! Just click\non the button below to generate your scene now!\n\n",
                    width=500,
                    alignment=ui.Alignment.CENTER,
                )

                # P R O C E D U R A L       W A R E H O U S E       G E N E R A T I O N
                with ui.VStack():
                    proceduralImage = ui.Image(
                        f"{self.UI_IMAGE_SERVER}warehouse.JPG",
                        width=500,
                        height=150,
                    )
                    proceduralImage.fill_policy = proceduralImage.fill_policy.PRESERVE_ASPECT_CROP
                    def genProcedural():
                        self._wh_helper.clear_stage()
                        self.layoutButton1.checked = False
                        self.layoutButton2.checked = False
                        self.layoutButton3.checked = False
                        self.objectButton1.checked = False
                        self.objectButton2.checked = False
                        self.objectButton3.checked = False
                        self.objectButton4.checked = False
                        self.objectButton5.checked = False
                        self.objectButton6.checked = False

                        # Pass asset buttons
                        self.objectButtons = [
                            self.objectButton1,
                            self.objectButton2,
                            self.objectButton3,
                            self.objectButton4,
                            self.objectButton5,
                            self.objectButton6,
                        ]

                        self.mode = "procedural"
                        self._wh_helper.gen_custom(True, self.mode, self.objectButtons)

                    proceduralButton = ui.Button(
                        "Procedurally Generate Warehouse",
                        clicked_fn=lambda: genProcedural(),
                        width=500,
                        height=40,
                        tooltip="Procedurally Generates a warehouse scene",
                    )
                    clearDescription = ui.Label(
                    "\nYou can clear the current scene and start a fresh stage by clicking the button below!\n\n",
                    width=500,
                    alignment=ui.Alignment.CENTER,
                    )
                    clearButton1 = ui.Button(
                        "Clear Stage",
                        clicked_fn=lambda: self._wh_helper.clear_stage(),
                        width=500,
                        height=40,
                        tooltip="Removes all assets on the stage",
                    )

                # C U S T O M       W A RE H O U S E        G E N E R A T I O N
                customgenLabel = ui.Label(
                    "\nOption 2. Customized Generation",
                    alignment=ui.Alignment.CENTER,
                    width=500,
                    style={"color": 0xFF00B976, "font_size": 25},
                )
                customgenDescriptionLabel1 = ui.Label(
                    "\nCustomized Generation module allows you to set custom parameters to generate your\nwarehouse scene. You can choose what objects the generated scene contains, and the\nlayout you want the scene to be generated with!\n\n",
                    width=500,
                    alignment=ui.Alignment.CENTER,
                )

                # Customized Warehouse Generation - layouts
                layoutLabel = ui.Label(
                    "2.1 Select Preferred Layout",
                    alignment=ui.Alignment.CENTER,
                    width=500,
                    style={"color": 0xFF00B976, "font_size": 20},
                )
                customgenDescriptionLabel2 = ui.Label(
                    "\nTo begin, select the preferred layout from the standard layout options given below.\n\n",
                    width=500,
                    alignment=ui.Alignment.CENTER,
                )

                # Layout selection
                with ui.VStack(width=500):

                    # Layout labels
                    with ui.HStack(width=500):
                        layoutLabel1 = ui.Label(
                            "U-Shaped Layout", alignment=ui.Alignment.CENTER, style={"color": 0xFF00B976}
                        )
                        layoutLabel2 = ui.Label(
                            "I-Shaped Layout", alignment=ui.Alignment.CENTER, style={"color": 0xFF00B976}
                        )
                        layoutLabel3 = ui.Label(
                            "L-Shaped Layout", alignment=ui.Alignment.CENTER, style={"color": 0xFF00B976}
                        )

                    # Layout buttons
                    with ui.HStack(width=500):
                        self.layoutButton1 = ui.Button(
                            width=166,
                            height=150,
                            tooltip="Generates a U-Shaped Layout",
                            style={
                                "Button.Image": {
                                    "image_url": f"{self.UI_IMAGE_SERVER}U-Shaped_Warehouse.png",
                                    "alignment": ui.Alignment.CENTER,
                                }
                            },
                            clicked_fn=lambda: sel_layout(1),
                        )

                        self.layoutButton2 = ui.Button(
                            width=166,
                            height=150,
                            tooltip="Generates an I-Shaped Layout",
                            style={
                                "Button.Image": {
                                    "image_url": f"{self.UI_IMAGE_SERVER}I-Shaped_Warehouse.png",
                                    "alignment": ui.Alignment.CENTER,
                                }
                            },
                            clicked_fn=lambda: sel_layout(2),
                        )
                        self.layoutButton3 = ui.Button(
                            width=166,
                            height=150,
                            tooltip="Generates an L-Shaped Layout",
                            style={
                                "Button.Image": {
                                    "image_url": f"{self.UI_IMAGE_SERVER}L-Shaped_Warehouse.png",
                                    "alignment": ui.Alignment.CENTER,
                                }
                            },
                            clicked_fn=lambda: sel_layout(3),
                        )

                # Customized Warehouse Generation - objects
                objectsLabel = ui.Label(
                    "\n2.2 Select Preferred Objects",
                    alignment=ui.Alignment.CENTER,
                    width=500,
                    style={"color": 0xFF00B976, "font_size": 20},
                )
                customgenDescriptionLabel3 = ui.Label(
                    "\nNow, select the preferred objects you want in your scene from the options given below.\n\n",
                    width=500,
                    alignment=ui.Alignment.CENTER,
                )

                # Objects selection
                with ui.VStack(width=500):

                    # Object labels row 1
                    with ui.HStack(width=500):
                        objectsLabel1 = ui.Label(
                            "Empty Racks", alignment=ui.Alignment.CENTER, style={"color": 0xFF00B976}
                        )
                        objectsLabel2 = ui.Label(
                            "Filled Racks", alignment=ui.Alignment.CENTER, style={"color": 0xFF00B976}
                        )
                        objectsLabel3 = ui.Label("Piles", alignment=ui.Alignment.CENTER, style={"color": 0xFF00B976})

                    # Object buttons row 1
                    with ui.HStack(width=500):
                        self.objectButton1 = ui.Button(
                            width=166,
                            height=150,
                            tooltip="Generates empty racks",
                            style={
                                "Button.Image": {
                                    "image_url": f"{self.UI_IMAGE_SERVER}objects-01.png",
                                    "alignment": ui.Alignment.CENTER,
                                }
                            },
                            clicked_fn=lambda: sel_object(self.objectButton1),
                        )
                        self.objectButton2 = ui.Button(
                            width=166,
                            height=150,
                            tooltip="Generates filled racks",
                            style={
                                "Button.Image": {
                                    "image_url": f"{self.UI_IMAGE_SERVER}objects-02.png",
                                    "alignment": ui.Alignment.CENTER,
                                }
                            },
                            clicked_fn=lambda: sel_object(self.objectButton2),
                        )
                        self.objectButton3 = ui.Button(
                            width=166,
                            height=150,
                            tooltip="Generates random piles of items",
                            style={
                                "Button.Image": {
                                    "image_url": f"{self.UI_IMAGE_SERVER}objects-03.png",
                                    "alignment": ui.Alignment.CENTER,
                                }
                            },
                            clicked_fn=lambda: sel_object(self.objectButton3),
                        )

                    # Object labels row 2
                    with ui.HStack(width=500):
                        objectsLabel4 = ui.Label(
                            "\nRailings", alignment=ui.Alignment.CENTER, style={"color": 0xFF00B976}
                        )
                        objectsLabel5 = ui.Label(
                            "\nForklift", alignment=ui.Alignment.CENTER, style={"color": 0xFF00B976}
                        )
                        objectsLabel6 = ui.Label("\nRobot", alignment=ui.Alignment.CENTER, style={"color": 0xFF00B976})

                    # Object buttons row 2
                    with ui.HStack(width=500):
                        self.objectButton4 = ui.Button(
                            width=166,
                            height=150,
                            tooltip="Generates safety railings",
                            style={
                                "Button.Image": {
                                    "image_url": f"{self.UI_IMAGE_SERVER}objects-04.png",
                                    "alignment": ui.Alignment.CENTER,
                                }
                            },
                            clicked_fn=lambda: sel_object(self.objectButton4),
                        )
                        self.objectButton5 = ui.Button(
                            width=166,
                            height=150,
                            tooltip="Generates forklifts",
                            style={
                                "Button.Image": {
                                    "image_url": f"{self.UI_IMAGE_SERVER}objects-05.png",
                                    "alignment": ui.Alignment.CENTER,
                                }
                            },
                            clicked_fn=lambda: sel_object(self.objectButton5),
                        )
                        self.objectButton6 = ui.Button(
                            width=166,
                            height=150,
                            tooltip="Generates transporter robots",
                            style={
                                "Button.Image": {
                                    "image_url": f"{self.UI_IMAGE_SERVER}objects-06.png",
                                    "alignment": ui.Alignment.CENTER,
                                }
                            },
                            clicked_fn=lambda: sel_object(self.objectButton6),
                        )

                customgenDescriptionLabel4 = ui.Label(
                    "\nNow, click on the button below to generate your own, customized warehouse scene!\n\n",
                    width=500,
                    alignment=ui.Alignment.CENTER,
                )
                def genCustomWarehouse(mode):
                    self.mode = mode
                    self._wh_helper.clear_stage()
                    # Pass asset buttons
                    self.objectButtons = [
                        self.objectButton1,
                        self.objectButton2,
                        self.objectButton3,
                        self.objectButton4,
                        self.objectButton5,
                        self.objectButton6,
                    ]
                    self._wh_helper.gen_custom(False, self.mode, self.objectButtons)

                customizedButton = ui.Button(
                    "Generate Customized Warehouse",
                    clicked_fn=lambda: genCustomWarehouse(self.mode),
                    width=500,
                    height=40,
                    tooltip="Generates a warehouse scene based on custom parameters",
                )
                clearButton2 = ui.Button(
                        "Clear Stage",
                        clicked_fn=lambda: self._wh_helper.clear_stage(),
                        width=500,
                        height=40,
                        tooltip="Removes all assets on the stage",
                    )

                # S M A R T         I M P O R T
                with ui.VStack(height=ui.Fraction(1)):
                    smartImportLabel = ui.Label(
                        "\nOption 3. Smart Import",
                        alignment=ui.Alignment.CENTER,
                        width=500,
                        style={"color": 0xFF00B976, "font_size": 25},
                    )
                    smartImportDescriptionLabel1 = ui.Label(
                        "\nSmart Import module allows you to instantly import your own assets - the smart way!\nSimply, select the asset type you are importing from the drop-down, copy and paste\nthe URL of the asset from the content navigator into the box below. Your asset is\nmagically imported in-place!\n\n",
                        width=500,
                        alignment=ui.Alignment.CENTER,
                    )

                    importImage = ui.Image(
                        f"{self.UI_IMAGE_SERVER}objects.JPG",
                        width=500,
                        height=150,
                        fill_policy=ui.FillPolicy.PRESERVE_ASPECT_CROP,
                        alignment=ui.Alignment.CENTER_TOP,
                    )
                    spacinglabel = ui.Label("")
                    importCategoryDropdown = ui.ComboBox(
                        1, "Empty Rack", "Filled Rack", "Pile", "Railing", "Forklift", "Robot"
                    )
                    spacinglabel = ui.Label("")
                    with ui.HStack():

                        importPathString = ui.StringField(width=250, height=40, tooltip= "Paste URL asset path").model
                        importButton = ui.Button(
                            "Import", clicked_fn=lambda: self._wh_helper.smart_import(importPathString, importCategoryDropdown), width=250, height=40
                        )
                    ui.Spacer(height = 65)

               ##########################          UI Helper Functions       ##############################################

                def sel_layout(n):
                    if n == 1:
                        self.layoutButton1.checked = True
                        self.layoutButton2.checked = False
                        self.layoutButton3.checked = False
                        self.mode = "Umode"
                    if n == 2:
                        self.layoutButton1.checked = False
                        self.layoutButton2.checked = True
                        self.layoutButton3.checked = False
                        self.mode = "Imode"
                    if n == 3:
                        self.layoutButton1.checked = False
                        self.layoutButton2.checked = False
                        self.layoutButton3.checked = True
                        self.mode = "Lmode"

                def sel_object(button):
                    if button.checked == True:
                        button.checked = False
                    else:
                        button.checked = True
        # Generate Procedural Scene if test script flag == True
        if runTestScript == True:
            print("<WarehouseCreatorWindow::runTestScript>: Starting Procedural Generation...")
            genProcedural()
            print("<WarehouseCreatorWindow::runTestScript>: Finished Procedural Generation.")
