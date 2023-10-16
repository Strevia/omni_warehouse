# Import necessary libraries
import omni.ext
from .warehouse_window_base import *

# Main Class
class WarehouseCreator(omni.ext.IExt):
    def on_startup(self, ext_id):
        self.wh_creator = WarehouseCreatorWindow()
        self.wh_creator._build_content()
        print("[omni.warehouse] WarehouseCreator started")

    def on_shutdown(self):
        self.wh_creator.destroy()
        print("[omni.warehouse] WarehouseCreator shutdown")
