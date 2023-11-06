from pyradioconfig.parts.ocelot.phys.Phys_Internal_Base_Customer_Chamberlain import Phys_Chamberlain_Ocelot
from py_2_and_3_compatibility import *

class Phys_Chamberlain_Sol(Phys_Chamberlain_Ocelot):

    # Copied from Jumbo and modified
    def PHY_Chamberlain_OOK_PHY0_310_narrow(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='PHY_Chamberlain_OOK_PHY0_310_narrow', phy_name=phy_name)

        self.Chamberlain_OOK_base(phy, model)

        # Add values to existing inputs
        phy.profile_inputs.base_frequency_hz.value = long(310000000)
        #channel spacing not configurable to 5M
        phy.profile_inputs.bandwidth_hz.value = 170000
        #slicer is also changed at runtime
        phy.profile_inputs.ook_slicer_level.value = 3
        phy.profile_inputs.frequency_comp_mode.value = model.vars.frequency_comp_mode.var_enum.INTERNAL_LOCK_AT_FRAME_DETECT

        # These overrides maintain PHY outputs despite OOK calculator changes
        phy.profile_outputs.AGC_CTRL0_MODE.override = 1
        phy.profile_outputs.AGC_GAINSTEPLIM0_CFLOOPSTEPMAX.override = 5
        phy.profile_outputs.MODEM_CTRL5_RESYNCBAUDTRANS.override = 0
        #phy.profile_outputs.MODEM_CF_DEC2.override = 36
        #phy.profile_outputs.MODEM_RXBR_RXBRINT.override = 2
        model.vars.dynamic_slicer_enabled.value_forced = False

    # Copied from Jumbo and modified
    def PHY_Chamberlain_OOK_PHY1_390(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='Chamberlain_OOK_PHY1_390', phy_name=phy_name)

        self.Chamberlain_OOK_base(phy, model)

        # Add values to existing inputs
        phy.profile_inputs.base_frequency_hz.value = long(390000000)
        phy.profile_inputs.bandwidth_hz.value = 620000
        phy.profile_inputs.ook_slicer_level.value = 3
        phy.profile_inputs.frequency_comp_mode.value = model.vars.frequency_comp_mode.var_enum.INTERNAL_LOCK_AT_FRAME_DETECT

        # These overrides maintain PHY outputs despite OOK calculator changes
        phy.profile_outputs.AGC_CTRL0_MODE.override = 1
        phy.profile_outputs.AGC_GAINSTEPLIM0_CFLOOPSTEPMAX.override = 5
        phy.profile_outputs.MODEM_CTRL5_RESYNCBAUDTRANS.override = 0
        model.vars.dynamic_slicer_enabled.value_forced = False

    # Copied from Jumbo and modified
    def PHY_Chamberlain_OOK_PHY1_390_narrow(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='Chamberlain_OOK_PHY1_390_narrow', phy_name=phy_name)

        self.Chamberlain_OOK_base(phy, model)

        # Add values to existing inputs
        phy.profile_inputs.base_frequency_hz.value = long(390000000)
        phy.profile_inputs.bandwidth_hz.value = 210000
        phy.profile_inputs.ook_slicer_level.value = 3
        phy.profile_inputs.frequency_comp_mode.value = model.vars.frequency_comp_mode.var_enum.INTERNAL_LOCK_AT_FRAME_DETECT

        # These overrides maintain PHY outputs despite OOK calculator changes
        phy.profile_outputs.AGC_CTRL0_MODE.override = 1
        phy.profile_outputs.AGC_GAINSTEPLIM0_CFLOOPSTEPMAX.override = 5
        phy.profile_outputs.MODEM_CTRL5_RESYNCBAUDTRANS.override = 0
        #phy.profile_outputs.MODEM_CF_DEC2.override = 57
        #phy.profile_outputs.MODEM_RXBR_RXBRINT.override = 2
        model.vars.dynamic_slicer_enabled.value_forced = False

    # Copied from Jumbo and modified
    def PHY_Chamberlain_OOK_PHY2_433(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='Chamberlain_OOK_PHY2_433', phy_name=phy_name)

        self.Chamberlain_OOK_base(phy, model)

        # Add values to existing inputs
        phy.profile_inputs.base_frequency_hz.value = long(433300000)
        phy.profile_inputs.channel_spacing_hz.value = 620000 #uneven channel map, only works for the first 2
        phy.profile_inputs.bandwidth_hz.value = 220000
        phy.profile_inputs.ook_slicer_level.value = 3
        phy.profile_inputs.frequency_comp_mode.value = model.vars.frequency_comp_mode.var_enum.INTERNAL_LOCK_AT_FRAME_DETECT

        # These overrides maintain PHY outputs despite OOK calculator changes
        phy.profile_outputs.AGC_CTRL0_MODE.override = 1
        phy.profile_outputs.AGC_GAINSTEPLIM0_CFLOOPSTEPMAX.override = 5
        phy.profile_outputs.MODEM_CTRL5_RESYNCBAUDTRANS.override = 0
        #phy.profile_outputs.MODEM_CF_DEC0.override = 3
        #phy.profile_outputs.MODEM_CF_DEC1.override = 3
        #phy.profile_outputs.MODEM_CF_DEC2.override = 60
        #phy.profile_outputs.MODEM_RXBR_RXBRINT.override = 2
        model.vars.dynamic_slicer_enabled.value_forced = False

    def PHY_Chamberlain_OOK_PHY3_868(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='Chamberlain_OOK_PHY3_868', phy_name=phy_name)

        self.Chamberlain_OOK_base(phy, model)

        # Add values to existing inputs
        phy.profile_inputs.base_frequency_hz.value = 868300000
        phy.profile_inputs.channel_spacing_hz.value = 650000  # uneven channel map, only works for the first 2
        phy.profile_inputs.bandwidth_hz.value = 180000
        phy.profile_inputs.frequency_comp_mode.value = model.vars.frequency_comp_mode.var_enum.INTERNAL_LOCK_AT_FRAME_DETECT
        phy.profile_inputs.syncword_length.value = 20
        phy.profile_inputs.syncword_0.value = 0xAA555

        # These overrides maintain PHY outputs despite OOK calculator changes
        phy.profile_outputs.AGC_CTRL0_MODE.override = 1
        phy.profile_outputs.MODEM_CTRL5_RESYNCBAUDTRANS.override = 0

        # phy.profile_outputs.AGC_AGCPERIOD1_PERIODLOW.override = 9896
        phy.profile_outputs.AGC_CTRL0_MODE.override = 1
        phy.profile_outputs.AGC_CTRL2_SAFEMODE.override = 0
        phy.profile_outputs.AGC_CTRL3_RFPKDDEB.override = 0
        phy.profile_outputs.AGC_STEPDWN_STEPDWN0.override = 1
        phy.profile_outputs.AGC_STEPDWN_STEPDWN1.override = 2
        phy.profile_outputs.AGC_STEPDWN_STEPDWN2.override = 4
        phy.profile_outputs.AGC_STEPDWN_STEPDWN3.override = 6
        phy.profile_outputs.AGC_STEPDWN_STEPDWN4.override = 6
        phy.profile_outputs.AGC_STEPDWN_STEPDWN5.override = 6
        phy.profile_outputs.MODEM_CTRL0_MAPFSK.override = 0
        phy.profile_outputs.MODEM_MODINDEX_MODINDEXE.override = 25
        #FIXME new override for Sol
        phy.profile_outputs.MODEM_BCRDEMODCTRL_MANCHPH.override = 0

        return phy
