# from warnings import catch_warnings
import omni.kit.test
import omni.kit.app
import carb
import carb.events
import carb.dictionary

from omni.warehouse_creator import *
from ..scripts.warehouse_window_base import *
from ..scripts.warehouse_helpers import *

class TestWarehouseCreator(omni.kit.test.AsyncTestCaseFailOnLogError):
    print("<tests_warehouse_creator.py>: Starting test script...")
    async def setUp(self):
        print("<TestWarehouseCreator::setUp>: WarehouseCreator starting...")
        self.wh_creator = WarehouseCreatorWindow()
        print("UI Window Created... Building Content...")
        self.wh_creator._build_content(True)
        print("<TestWarehouseCreator::setUp>: WarehouseCreator started.")

    async def tearDown(self):
        print("<TestWarehouseCreator::tearDown>: WarehouseCreator stopping...")
        self.wh_creator.destroy()
        print("<TestWarehouseCreator::tearDown>: WarehouseCreator shutdown.")
