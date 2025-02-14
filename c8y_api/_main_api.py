# Copyright (c) 2020 Software AG,
# Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA,
# and/or its subsidiaries and/or its affiliates and/or their licensors.
# Use, reproduction, transfer, publication or disclosure is prohibited except
# as specifically provided for in your License Agreement with Software AG.

from requests.auth import AuthBase

from c8y_api._base_api import CumulocityRestApi

from c8y_api.model.administration import Users, GlobalRoles, InventoryRoles
from c8y_api.model.alarms import Alarms
from c8y_api.model.applications import Applications
from c8y_api.model.events import Events
from c8y_api.model.identity import Identity
from c8y_api.model.binaries import Binaries
from c8y_api.model.inventory import Inventory, DeviceInventory, DeviceGroupInventory
from c8y_api.model.measurements import Measurements
from c8y_api.model.operations import Operations


class CumulocityApi(CumulocityRestApi):
    """Main Cumulocity API.

    Provides usage centric access to a Cumulocity instance.
    """

    def __init__(self, base_url: str, tenant_id: str, username: str = None, password: str = None,
                 tfa_token: str = None, auth: AuthBase = None, application_key: str = None):
        super().__init__(base_url, tenant_id, username=username, password=password, tfa_token=tfa_token,
                         auth=auth, application_key=application_key)
        self.__measurements = Measurements(self)
        self.__inventory = Inventory(self)
        self.__binaries = Binaries(self)
        self.__group_inventory = DeviceGroupInventory(self)
        self.__device_inventory = DeviceInventory(self)
        self.__identity = Identity(self)
        self.__users = Users(self)
        self.__global_roles = GlobalRoles(self)
        self.__inventory_roles = InventoryRoles(self)
        self.__applications = Applications(self)
        self.__events = Events(self)
        self.__alarms = Alarms(self)
        self.__operations = Operations(self)

    @property
    def measurements(self) -> Measurements:
        """Provide access to the Measurements API."""
        return self.__measurements

    @property
    def inventory(self) -> Inventory:
        """Provide access to the Inventory API."""
        return self.__inventory

    @property
    def group_inventory(self) -> DeviceGroupInventory:
        """Provide access to the Device Group Inventory API."""
        return self.__group_inventory

    @property
    def devicegroups(self) -> DeviceGroupInventory:
        """Provide access to the Device Group Inventory API."""
        return self.__group_inventory

    @property
    def binaries(self):
        """Provide access to the Binary API."""
        return self.__binaries

    @property
    def device_inventory(self) -> DeviceInventory:
        """Provide access to the Device Inventory API."""
        return self.__device_inventory

    @property
    def identity(self) -> Identity:
        """Provide access to the Identity API."""
        return self.__identity

    @property
    def users(self) -> Users:
        """Provide access to the Users API."""
        return self.__users

    @property
    def global_roles(self) -> GlobalRoles:
        """Provide access to the Global Roles API."""
        return self.__global_roles

    @property
    def inventory_roles(self) -> InventoryRoles:
        """Provide access to the Inventory Roles API."""
        return self.__inventory_roles

    @property
    def applications(self) -> Applications:
        """Provide access to the Applications API."""
        return self.__applications

    @property
    def events(self) -> Events:
        """Provide access to the Events API."""
        return self.__events

    @property
    def alarms(self) -> Alarms:
        """Provide access to the Alarm API."""
        return self.__alarms

    @property
    def operations(self) -> Operations:
        """Provide access to the Operation API."""
        return self.__operations
