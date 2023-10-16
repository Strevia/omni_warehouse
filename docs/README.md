# Warehouse Creator Extension
The Warehouse Creator is an Extension for Omniverse Create that allows you to quickly get started with building Warehouse Digital Twins in an automated way. It supports procedurally generating full warehouse scenes, as well as customized generation based on layouts and assets that you want in the scene.

The extension works by spawning USD (Universal Scene Description) assets from Nucleus based on predefined asset-based rules.

The pre-defined asset placement rules control the sample-space of the various positions, rotations, and scaling of the asset to be spawned. Based on user-defined parameters, assets are randomly chosen from Nucleus and placed in random positions from the sample space of positions defined by the placement rules. Occupied positions are recorded, and new assets are spawned in the unoccupied positions of the sample space.

You can modify the assets and their paths to several types and locations based on preference – this allows you to use the extension to generate scenes with your own custom assets from their defined locations.

# Getting Started

## Enable Extension via Extensions Manager
The Extension can be enabled by:

1. Navigating to Window > Extensions Manager from the top-level menu

2. Searching for Warehouse Creator in the text field of the Extension Manager window, to reveal up the omni.warehouse_creator result.

3. Clicking the toggle to enable the Extension

# Navigating the User Interface

## Warehouse Creator - User Interface

The extension UI (User Interface) contains a vertically scrollable window that hosts several quick recipes to get started with building your warehouse scenes. The different recipes and descriptions are elucidated below:

### Option 1: Quick Generation
Quick Generation module allows you to quickly generate your warehouse scene without any parameters. It contains two different options:

### Option 2: Customized Generation
The Customized Generation option allows you to control different parameters for scene generation to generate scenes attuned to your need.

### Option 3: Smart Import
Smart Import module allows you to instantly import your own assets - the smart way! Simply select the asset type you are importing from the drop-down, copy and paste the URL of the asset from the content navigator into the box below. Your asset will be imported in-place. Import assets that fall under the following asset categories:

1. Filled Racks
2. Empty Racks
3. Piles
4. Railings
5. Forklift
6. Robot

Note:
1. URL paths containing the keyword "isaac" will be scaled by (100,100,100) as Isaac Sim assets are in meters versus the default OV units of centimeters.
2. Empty spaces are reserved for the Smart Import feature during initial generation of warehouse. When used, Smart Import will randomly choose a location from a list of reserved spaces to place an imported asset.

### Clear Stage
Quickly clear the scene. Users can select this button to delete all existing assets from their scene. This function is also called each time you generate a scene with Option 1 or 2.

# Customize
Modify the current extension with your own customizations!

## Develop with VS Code
### Pre-requisites
1. Microsoft VS Code (free)
2. Omniverse Create (Omniverse Code also works)
3. Enabled Warehouse Creator Extension
4. Enabled Kit VS Code Debug Extension

### Configuring Omniverse
1. In Create, navigate to Extensions
2. Search for Warehouse Creator
3. Select Warehouse Creator Extension from list of available extensions
4. Select Open with VSCode

Similarly, you will need to follow steps 1-3 to enable the "Kit Debug VSCode" Extension

### Configuring VS Code
1. In VS Code, you will need to create a session to connect and link the debugger to your Create's VS Code Debugger Extension
2. Navigate to Run -> Add Configuration
3. Select Python
4. Click on "Remote Attach". Once you've selected, enter the IP address and Port Number specified in the VS Code Debugger extension
5. Once configured, hit the "F5" on your keyboard or navigate to Run -> Start debugging to start a debugging session
6. Once connected, the Kit VS Code window in Create should show the debugger has attached
7. You should now be able to navigate to the source code, modify it, hit Ctrl + S to save, and see the changes take effect in the extension!
8. Source code files can be found in the following directory: "omni\warehouse_creator\python\scripts\"
Note that if the code is not executable due to a syntax error, the extension will disappear from Omniverse until the code has been fixed and saved once again.
