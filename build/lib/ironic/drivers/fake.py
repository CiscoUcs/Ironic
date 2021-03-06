# -*- encoding: utf-8 -*-
#
# Copyright 2013 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""
Fake drivers used in testing.
"""

from oslo_utils import importutils

from ironic.common import exception
from ironic.common.i18n import _
from ironic.drivers import base
from ironic.drivers.modules import agent
from ironic.drivers.modules.amt import management as amt_mgmt
from ironic.drivers.modules.amt import power as amt_power
from ironic.drivers.modules import discoverd
from ironic.drivers.modules.drac import management as drac_mgmt
from ironic.drivers.modules.drac import power as drac_power
from ironic.drivers.modules import fake
from ironic.drivers.modules import iboot
from ironic.drivers.modules.ilo import inspect as ilo_inspect
from ironic.drivers.modules.ilo import management as ilo_management
from ironic.drivers.modules.ilo import power as ilo_power
from ironic.drivers.modules import ipminative
from ironic.drivers.modules import ipmitool
from ironic.drivers.modules.irmc import management as irmc_management
from ironic.drivers.modules.irmc import power as irmc_power
from ironic.drivers.modules import pxe
from ironic.drivers.modules import seamicro
from ironic.drivers.modules import snmp
from ironic.drivers.modules import ssh
from ironic.drivers.modules.ucs import management as ucs_mgmt
from ironic.drivers.modules.ucs import power as ucs_power
from ironic.drivers.modules import virtualbox
from ironic.drivers import utils


class FakeDriver(base.BaseDriver):
    """Example implementation of a Driver."""

    def __init__(self):
        self.power = fake.FakePower()
        self.deploy = fake.FakeDeploy()

        self.a = fake.FakeVendorA()
        self.b = fake.FakeVendorB()
        self.mapping = {'first_method': self.a,
                        'second_method': self.b,
                        'third_method_sync': self.b}
        self.vendor = utils.MixinVendorInterface(self.mapping)
        self.console = fake.FakeConsole()
        self.management = fake.FakeManagement()
        self.inspect = fake.FakeInspect()


class FakeIPMIToolDriver(base.BaseDriver):
    """Example implementation of a Driver."""

    def __init__(self):
        self.power = ipmitool.IPMIPower()
        self.console = ipmitool.IPMIShellinaboxConsole()
        self.deploy = fake.FakeDeploy()
        self.vendor = ipmitool.VendorPassthru()
        self.management = ipmitool.IPMIManagement()


class FakePXEDriver(base.BaseDriver):
    """Example implementation of a Driver."""

    def __init__(self):
        self.power = fake.FakePower()
        self.deploy = pxe.PXEDeploy()
        self.vendor = pxe.VendorPassthru()


class FakeSSHDriver(base.BaseDriver):
    """Example implementation of a Driver."""

    def __init__(self):
        self.power = ssh.SSHPower()
        self.deploy = fake.FakeDeploy()
        self.management = ssh.SSHManagement()


class FakeIPMINativeDriver(base.BaseDriver):
    """Fake IPMINative driver."""

    def __init__(self):
        if not importutils.try_import('pyghmi'):
            raise exception.DriverLoadError(
                    driver=self.__class__.__name__,
                    reason=_("Unable to import pyghmi IPMI library"))
        self.power = ipminative.NativeIPMIPower()
        self.console = ipminative.NativeIPMIShellinaboxConsole()
        self.deploy = fake.FakeDeploy()
        self.management = ipminative.NativeIPMIManagement()


class FakeSeaMicroDriver(base.BaseDriver):
    """Fake SeaMicro driver."""

    def __init__(self):
        if not importutils.try_import('seamicroclient'):
            raise exception.DriverLoadError(
                    driver=self.__class__.__name__,
                    reason=_("Unable to import seamicroclient library"))
        self.power = seamicro.Power()
        self.deploy = fake.FakeDeploy()
        self.management = seamicro.Management()
        self.vendor = seamicro.VendorPassthru()
        self.console = seamicro.ShellinaboxConsole()


class FakeAgentDriver(base.BaseDriver):
    """Example implementation of an AgentDriver."""

    def __init__(self):
        self.power = fake.FakePower()
        self.deploy = agent.AgentDeploy()
        self.vendor = agent.AgentVendorInterface()


class FakeIBootDriver(base.BaseDriver):
    """Fake iBoot driver."""

    def __init__(self):
        if not importutils.try_import('iboot'):
            raise exception.DriverLoadError(
                    driver=self.__class__.__name__,
                    reason=_("Unable to import iboot library"))
        self.power = iboot.IBootPower()
        self.deploy = fake.FakeDeploy()


class FakeIloDriver(base.BaseDriver):
    """Fake iLO driver, used in testing."""

    def __init__(self):
        if not importutils.try_import('proliantutils'):
            raise exception.DriverLoadError(
                    driver=self.__class__.__name__,
                    reason=_("Unable to import proliantutils library"))
        self.power = ilo_power.IloPower()
        self.deploy = fake.FakeDeploy()
        self.management = ilo_management.IloManagement()
        self.inspect = ilo_inspect.IloInspect()


class FakeDracDriver(base.BaseDriver):
    """Fake Drac driver."""

    def __init__(self):
        if not importutils.try_import('pywsman'):
            raise exception.DriverLoadError(
                    driver=self.__class__.__name__,
                    reason=_('Unable to import pywsman library'))

        self.power = drac_power.DracPower()
        self.deploy = fake.FakeDeploy()
        self.management = drac_mgmt.DracManagement()


class FakeSNMPDriver(base.BaseDriver):
    """Fake SNMP driver."""

    def __init__(self):
        if not importutils.try_import('pysnmp'):
            raise exception.DriverLoadError(
                    driver=self.__class__.__name__,
                    reason=_("Unable to import pysnmp library"))
        self.power = snmp.SNMPPower()
        self.deploy = fake.FakeDeploy()


class FakeIRMCDriver(base.BaseDriver):
    """Fake iRMC driver."""

    def __init__(self):
        if not importutils.try_import('scciclient'):
            raise exception.DriverLoadError(
                    driver=self.__class__.__name__,
                    reason=_("Unable to import python-scciclient library"))
        self.power = irmc_power.IRMCPower()
        self.deploy = fake.FakeDeploy()
        self.management = irmc_management.IRMCManagement()


class FakeVirtualBoxDriver(base.BaseDriver):
    """Fake VirtualBox driver."""

    def __init__(self):
        if not importutils.try_import('pyremotevbox'):
            raise exception.DriverLoadError(
                    driver=self.__class__.__name__,
                    reason=_("Unable to import pyremotevbox library"))
        self.power = virtualbox.VirtualBoxPower()
        self.deploy = fake.FakeDeploy()
        self.management = virtualbox.VirtualBoxManagement()


class FakeIPMIToolDiscoverdDriver(base.BaseDriver):
    """Fake Discoverd driver."""

    def __init__(self):
        self.power = ipmitool.IPMIPower()
        self.console = ipmitool.IPMIShellinaboxConsole()
        self.deploy = fake.FakeDeploy()
        self.vendor = ipmitool.VendorPassthru()
        self.management = ipmitool.IPMIManagement()
        # NOTE(dtantsur): unlike other uses of DiscoverdInspect, this one is
        # unconditional, as this driver is designed for testing discoverd
        # integration.
        self.inspect = discoverd.DiscoverdInspect()


class FakeAMTDriver(base.BaseDriver):
    """Fake AMT driver."""

    def __init__(self):
        if not importutils.try_import('pywsman'):
            raise exception.DriverLoadError(
                    driver=self.__class__.__name__,
                    reason=_("Unable to import pywsman library"))
        self.power = amt_power.AMTPower()
        self.deploy = fake.FakeDeploy()
        self.management = amt_mgmt.AMTManagement()


class FakeUcsDriver(base.BaseDriver):
    """Fake UCS driver."""

    def __init__(self):
        if not importutils.try_import('UcsSdk'):
            raise exception.DriverLoadError(
                driver=self.__class__.__name__,
                reason=_("Unable to import UcsSdk library"))
        self.power = ucs_power.Power()
        self.deploy = fake.FakeDeploy()
        self.management = ucs_mgmt.UcsManagement()
