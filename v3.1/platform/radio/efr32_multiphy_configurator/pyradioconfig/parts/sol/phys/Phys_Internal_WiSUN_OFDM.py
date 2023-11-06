#This file contains internal OFDM PHYs, some of which are temporarily used solely for a unique PHY name across test parameters
from pyradioconfig.parts.sol.phys.Phys_Studio_WiSUN_OFDM import Phys_Studio_WiSUN_OFDM_Sol
from pyradioconfig.calculator_model_framework.decorators.phy_decorators import do_not_inherit_phys

@do_not_inherit_phys
class Phys_Internal_WiSUN_OFDM_Sol(Phys_Studio_WiSUN_OFDM_Sol):

    def PHY_ValOnly_WISUN_868MHz_OFDM_OPT1_MCS0(self, model):
        phy = super().PHY_IEEE802154_WISUN_868MHz_OFDM_OPT1(model, phy_name='PHY_ValOnly_WISUN_868MHz_OFDM_OPT1_MCS0')
        return phy

    def PHY_ValOnly_WISUN_868MHz_OFDM_OPT1_MCS1(self, model):
        phy = super().PHY_IEEE802154_WISUN_868MHz_OFDM_OPT1(model, phy_name='PHY_ValOnly_WISUN_868MHz_OFDM_OPT1_MCS1')
        return phy

    def PHY_ValOnly_WISUN_868MHz_OFDM_OPT1_MCS2(self, model):
        phy = super().PHY_IEEE802154_WISUN_868MHz_OFDM_OPT1(model, phy_name='PHY_ValOnly_WISUN_868MHz_OFDM_OPT1_MCS2')
        return phy

    def PHY_ValOnly_WISUN_868MHz_OFDM_OPT1_MCS3(self, model):
        phy = super().PHY_IEEE802154_WISUN_868MHz_OFDM_OPT1(model, phy_name='PHY_ValOnly_WISUN_868MHz_OFDM_OPT1_MCS3')
        return phy

    def PHY_ValOnly_WISUN_868MHz_OFDM_OPT1_MCS4(self, model):
        phy = super().PHY_IEEE802154_WISUN_868MHz_OFDM_OPT1(model, phy_name='PHY_ValOnly_WISUN_868MHz_OFDM_OPT1_MCS4')
        return phy

    def PHY_ValOnly_WISUN_868MHz_OFDM_OPT1_MCS5(self, model):
        phy = super().PHY_IEEE802154_WISUN_868MHz_OFDM_OPT1(model, phy_name='PHY_ValOnly_WISUN_868MHz_OFDM_OPT1_MCS5')
        return phy

    def PHY_ValOnly_WISUN_868MHz_OFDM_OPT1_MCS6(self, model):
        phy = super().PHY_IEEE802154_WISUN_868MHz_OFDM_OPT1(model, phy_name='PHY_ValOnly_WISUN_868MHz_OFDM_OPT1_MCS6')
        return phy

    def PHY_ValOnly_WISUN_868MHz_OFDM_OPT2_MCS0(self, model):
        phy = super().PHY_IEEE802154_WISUN_868MHz_OFDM_OPT2(model, phy_name='PHY_ValOnly_WISUN_868MHz_OFDM_OPT2_MCS0')
        return phy

    def PHY_ValOnly_WISUN_868MHz_OFDM_OPT2_MCS1(self, model):
        phy = super().PHY_IEEE802154_WISUN_868MHz_OFDM_OPT2(model, phy_name='PHY_ValOnly_WISUN_868MHz_OFDM_OPT2_MCS1')
        return phy

    def PHY_ValOnly_WISUN_868MHz_OFDM_OPT2_MCS2(self, model):
        phy = super().PHY_IEEE802154_WISUN_868MHz_OFDM_OPT2(model, phy_name='PHY_ValOnly_WISUN_868MHz_OFDM_OPT2_MCS2')
        return phy

    def PHY_ValOnly_WISUN_868MHz_OFDM_OPT2_MCS3(self, model):
        phy = super().PHY_IEEE802154_WISUN_868MHz_OFDM_OPT2(model, phy_name='PHY_ValOnly_WISUN_868MHz_OFDM_OPT2_MCS3')
        return phy

    def PHY_ValOnly_WISUN_868MHz_OFDM_OPT2_MCS4(self, model):
        phy = super().PHY_IEEE802154_WISUN_868MHz_OFDM_OPT2(model, phy_name='PHY_ValOnly_WISUN_868MHz_OFDM_OPT2_MCS4')
        return phy

    def PHY_ValOnly_WISUN_868MHz_OFDM_OPT2_MCS5(self, model):
        phy = super().PHY_IEEE802154_WISUN_868MHz_OFDM_OPT2(model, phy_name='PHY_ValOnly_WISUN_868MHz_OFDM_OPT2_MCS5')
        return phy

    def PHY_ValOnly_WISUN_868MHz_OFDM_OPT2_MCS6(self, model):
        phy = super().PHY_IEEE802154_WISUN_868MHz_OFDM_OPT2(model, phy_name='PHY_ValOnly_WISUN_868MHz_OFDM_OPT2_MCS6')
        return phy

    def PHY_ValOnly_WISUN_868MHz_OFDM_OPT3_MCS0(self, model):
        phy = super().PHY_IEEE802154_WISUN_868MHz_OFDM_OPT3(model, phy_name='PHY_ValOnly_WISUN_868MHz_OFDM_OPT3_MCS0')
        return phy

    def PHY_ValOnly_WISUN_868MHz_OFDM_OPT3_MCS1(self, model):
        phy = super().PHY_IEEE802154_WISUN_868MHz_OFDM_OPT3(model, phy_name='PHY_ValOnly_WISUN_868MHz_OFDM_OPT3_MCS1')
        return phy

    def PHY_ValOnly_WISUN_868MHz_OFDM_OPT3_MCS2(self, model):
        phy = super().PHY_IEEE802154_WISUN_868MHz_OFDM_OPT3(model, phy_name='PHY_ValOnly_WISUN_868MHz_OFDM_OPT3_MCS2')
        return phy

    def PHY_ValOnly_WISUN_868MHz_OFDM_OPT3_MCS3(self, model):
        phy = super().PHY_IEEE802154_WISUN_868MHz_OFDM_OPT3(model, phy_name='PHY_ValOnly_WISUN_868MHz_OFDM_OPT3_MCS3')
        return phy

    def PHY_ValOnly_WISUN_868MHz_OFDM_OPT3_MCS4(self, model):
        phy = super().PHY_IEEE802154_WISUN_868MHz_OFDM_OPT3(model, phy_name='PHY_ValOnly_WISUN_868MHz_OFDM_OPT3_MCS4')
        return phy

    def PHY_ValOnly_WISUN_868MHz_OFDM_OPT3_MCS5(self, model):
        phy = super().PHY_IEEE802154_WISUN_868MHz_OFDM_OPT3(model, phy_name='PHY_ValOnly_WISUN_868MHz_OFDM_OPT3_MCS5')
        return phy

    def PHY_ValOnly_WISUN_868MHz_OFDM_OPT3_MCS6(self, model):
        phy = super().PHY_IEEE802154_WISUN_868MHz_OFDM_OPT3(model, phy_name='PHY_ValOnly_WISUN_868MHz_OFDM_OPT3_MCS6')
        return phy

    def PHY_ValOnly_WISUN_868MHz_OFDM_OPT4_MCS0(self, model):
        phy = super().PHY_IEEE802154_WISUN_868MHz_OFDM_OPT4(model, phy_name='PHY_ValOnly_WISUN_868MHz_OFDM_OPT4_MCS0')
        return phy

    def PHY_ValOnly_WISUN_868MHz_OFDM_OPT4_MCS1(self, model):
        phy = super().PHY_IEEE802154_WISUN_868MHz_OFDM_OPT4(model, phy_name='PHY_ValOnly_WISUN_868MHz_OFDM_OPT4_MCS1')
        return phy

    def PHY_ValOnly_WISUN_868MHz_OFDM_OPT4_MCS2(self, model):
        phy = super().PHY_IEEE802154_WISUN_868MHz_OFDM_OPT4(model, phy_name='PHY_ValOnly_WISUN_868MHz_OFDM_OPT4_MCS2')
        return phy

    def PHY_ValOnly_WISUN_868MHz_OFDM_OPT4_MCS3(self, model):
        phy = super().PHY_IEEE802154_WISUN_868MHz_OFDM_OPT4(model, phy_name='PHY_ValOnly_WISUN_868MHz_OFDM_OPT4_MCS3')
        return phy

    def PHY_ValOnly_WISUN_868MHz_OFDM_OPT4_MCS4(self, model):
        phy = super().PHY_IEEE802154_WISUN_868MHz_OFDM_OPT4(model, phy_name='PHY_ValOnly_WISUN_868MHz_OFDM_OPT4_MCS4')
        return phy

    def PHY_ValOnly_WISUN_868MHz_OFDM_OPT4_MCS5(self, model):
        phy = super().PHY_IEEE802154_WISUN_868MHz_OFDM_OPT4(model, phy_name='PHY_ValOnly_WISUN_868MHz_OFDM_OPT4_MCS5')
        return phy

    def PHY_ValOnly_WISUN_868MHz_OFDM_OPT4_MCS6(self, model):
        phy = super().PHY_IEEE802154_WISUN_868MHz_OFDM_OPT4(model, phy_name='PHY_ValOnly_WISUN_868MHz_OFDM_OPT4_MCS6')
        return phy