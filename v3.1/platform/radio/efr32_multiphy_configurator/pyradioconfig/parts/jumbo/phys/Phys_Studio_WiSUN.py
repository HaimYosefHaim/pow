from pyradioconfig.calculator_model_framework.interfaces.iphy import IPhy
from pyradioconfig.parts.ocelot.phys.Phys_Studio_WiSUN import PHYS_IEEE802154_WiSUN_Ocelot

class PHYS_IEEE802154_WiSUN_Jumbo(IPhy):

    ### PHYs Tested by Apps ###

    def PHY_IEEE802154_WISUN_868MHz_2GFSK_50kbps_1a_EU(self, model, phy_name=None):
        #Inherit the PHY from Ocelot
        phy = PHYS_IEEE802154_WiSUN_Ocelot().PHY_IEEE802154_WISUN_868MHz_2GFSK_50kbps_1a_EU(model)

        # Default xtal frequency of 38.4MHz
        phy.profile_inputs.xtal_frequency_hz.value = 38400000

    def PHY_IEEE802154_WISUN_873MHz_2GFSK_50kbps_1a_EU(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.WiSUN, readable_name='Wi-SUN FAN, EU-873MHz, 1a (2FSK 50kbps mi=0.5)',
                            phy_name=phy_name)

        # Select the correct SUNFSK mode
        phy.profile_inputs.wisun_mode.value = model.vars.wisun_mode.var_enum.Mode1a

        # Define WiSUN Profile / Region specific inputs
        phy.profile_inputs.base_frequency_hz.value = 870100000  # FAN EU Mode #1a, WiSUN 20140727-PHY-Profile Table 3
        phy.profile_inputs.channel_spacing_hz.value = 100000  # FAN EU Mode #1a, WiSUN 20140727-PHY-Profile Table 3
        phy.profile_inputs.preamble_length.value = 8 * 8  # FAN EU Mode #1a, WiSUN 20140727-PHY-Profile Table 6
        phy.profile_inputs.crc_poly.value = model.vars.crc_poly.var_enum.ANSIX366_1979  # 802.15.4-2015, 7.2.10

        # Default xtal frequency of 38.4MHz
        phy.profile_inputs.xtal_frequency_hz.value = 38400000

        return phy


    def PHY_IEEE802154_WISUN_866MHz_2GFSK_50kbps_1a_IN(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.WiSUN, readable_name='Wi-SUN FAN, IN-866MHz, 1a (2FSK 50kbps mi=0.5)',
                            phy_name=phy_name)

        # Select the correct SUNFSK mode
        phy.profile_inputs.wisun_mode.value = model.vars.wisun_mode.var_enum.Mode1a

        # Define WiSUN Profile / Region specific inputs
        phy.profile_inputs.base_frequency_hz.value = 865100000  # FAN IN Mode #1a, WiSUN 20140727-PHY-Profile Table 3
        phy.profile_inputs.channel_spacing_hz.value = 100000  # FAN IN Mode #1a, WiSUN 20140727-PHY-Profile Table 3
        phy.profile_inputs.preamble_length.value = 8 * 8  # FAN IN Mode #1a, WiSUN 20140727-PHY-Profile Table 6
        phy.profile_inputs.crc_poly.value = model.vars.crc_poly.var_enum.ANSIX366_1979  # 802.15.4-2015, 7.2.10

        # Default xtal frequency of 38.4MHz
        phy.profile_inputs.xtal_frequency_hz.value = 38400000

        return phy

    def PHY_IEEE802154_WISUN_915MHz_2GFSK_50kbps_1b_NA(self, model, phy_name=None):
        phy = PHYS_IEEE802154_WiSUN_Ocelot().PHY_IEEE802154_WISUN_915MHz_2GFSK_50kbps_1b_NA(model)

        # Default xtal frequency of 38.4MHz
        phy.profile_inputs.xtal_frequency_hz.value = 38400000

    def PHY_IEEE802154_WISUN_922MHz_2GFSK_50kbps_1b_VN(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.WiSUN, readable_name='Wi-SUN FAN, VN-922MHz, 1b (2FSK 50kbps mi=1.0)',
                            phy_name=phy_name)

        # Select the correct SUNFSK mode
        phy.profile_inputs.wisun_mode.value = model.vars.wisun_mode.var_enum.Mode1b

        # Define WiSUN Profile / Region specific inputs
        phy.profile_inputs.base_frequency_hz.value = 920200000  # FAN VN Mode #1b, WiSUN 20140727-PHY-Profile Table 3
        phy.profile_inputs.channel_spacing_hz.value = 200000  # FAN VN Mode #1b, WiSUN 20140727-PHY-Profile Table 3
        phy.profile_inputs.preamble_length.value = 8 * 8  # FAN VN Mode #1b, WiSUN 20140727-PHY-Profile Table 6
        phy.profile_inputs.crc_poly.value = model.vars.crc_poly.var_enum.ANSIX366_1979  # 802.15.4-2015, 7.2.10

        # Default xtal frequency of 38.4MHz
        phy.profile_inputs.xtal_frequency_hz.value = 38400000

    def PHY_IEEE802154_WISUN_868MHz_2GFSK_100kbps_2a_EU(self, model, phy_name=None):
        phy = PHYS_IEEE802154_WiSUN_Ocelot().PHY_IEEE802154_WISUN_868MHz_2GFSK_100kbps_2a_EU(model)

        # Default xtal frequency of 38.4MHz
        phy.profile_inputs.xtal_frequency_hz.value = 38400000

    def PHY_IEEE802154_WISUN_873MHz_2GFSK_100kbps_2a_EU(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.WiSUN, readable_name='Wi-SUN FAN, EU-873MHz, 2a (2FSK 100kbps mi=0.5)',
                            phy_name=phy_name)

        # Select the correct SUNFSK mode
        phy.profile_inputs.wisun_mode.value = model.vars.wisun_mode.var_enum.Mode2a

        # Define WiSUN Profile / Region specific inputs
        phy.profile_inputs.base_frequency_hz.value = 870200000  # FAN EU Mode #2a, WiSUN 20140727-PHY-Profile Table 3
        phy.profile_inputs.channel_spacing_hz.value = 200000  # FAN EU Mode #2a, WiSUN 20140727-PHY-Profile Table 3
        phy.profile_inputs.preamble_length.value = 8 * 8  # FAN EU Mode #2a, WiSUN 20140727-PHY-Profile Table 6
        phy.profile_inputs.crc_poly.value = model.vars.crc_poly.var_enum.ANSIX366_1979  # 802.15.4-2015, 7.2.10

        # Default xtal frequency of 38.4MHz
        phy.profile_inputs.xtal_frequency_hz.value = 38400000

        return phy

    def PHY_IEEE802154_WISUN_866MHz_2GFSK_100kbps_2a_IN(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.WiSUN, readable_name='Wi-SUN FAN, IN-866MHz, 2a (2FSK 100kbps mi=0.5)',
                            phy_name=phy_name)

        # Select the correct SUNFSK mode
        phy.profile_inputs.wisun_mode.value = model.vars.wisun_mode.var_enum.Mode2a

        # Define WiSUN Profile / Region specific inputs
        phy.profile_inputs.base_frequency_hz.value = 865100000  # FAN EU Mode #2a, WiSUN 20140727-PHY-Profile Table 3
        phy.profile_inputs.channel_spacing_hz.value = 200000  # FAN EU Mode #2a, WiSUN 20140727-PHY-Profile Table 3
        phy.profile_inputs.preamble_length.value = 8 * 8  # FAN EU Mode #2a, WiSUN 20140727-PHY-Profile Table 6
        phy.profile_inputs.crc_poly.value = model.vars.crc_poly.var_enum.ANSIX366_1979  # 802.15.4-2015, 7.2.10

        # Default xtal frequency of 38.4MHz
        phy.profile_inputs.xtal_frequency_hz.value = 38400000

    def PHY_IEEE802154_WISUN_915MHz_2GFSK_100kbps_2a_NA(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.WiSUN, readable_name='Wi-SUN FAN, NA-915MHz, 2a (2FSK 100kbps mi=0.5)',
                            phy_name=phy_name)

        # Select the correct SUNFSK mode
        phy.profile_inputs.wisun_mode.value = model.vars.wisun_mode.var_enum.Mode2a

        # Define WiSUN Profile / Region specific inputs
        phy.profile_inputs.base_frequency_hz.value = 902200000  # FAN EU Mode #2a, WiSUN 20140727-PHY-Profile Table 3
        phy.profile_inputs.channel_spacing_hz.value = 200000  # FAN EU Mode #2a, WiSUN 20140727-PHY-Profile Table 3
        phy.profile_inputs.preamble_length.value = 8 * 8  # FAN EU Mode #2a, WiSUN 20140727-PHY-Profile Table 6
        phy.profile_inputs.crc_poly.value = model.vars.crc_poly.var_enum.ANSIX366_1979  # 802.15.4-2015, 7.2.10

        # Default xtal frequency of 38.4MHz
        phy.profile_inputs.xtal_frequency_hz.value = 38400000

    def PHY_IEEE802154_WISUN_922MHz_2GFSK_100kbps_2a_VN(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.WiSUN, readable_name='Wi-SUN FAN, VN-922MHz, 2a (2FSK 100kbps mi=0.5)',
                            phy_name=phy_name)

        # Select the correct SUNFSK mode
        phy.profile_inputs.wisun_mode.value = model.vars.wisun_mode.var_enum.Mode2a

        # Define WiSUN Profile / Region specific inputs
        phy.profile_inputs.base_frequency_hz.value = 920200000  # FAN EU Mode #2a, WiSUN 20140727-PHY-Profile Table 3
        phy.profile_inputs.channel_spacing_hz.value = 200000  # FAN EU Mode #2a, WiSUN 20140727-PHY-Profile Table 3
        phy.profile_inputs.preamble_length.value = 8 * 8  # FAN EU Mode #2a, WiSUN 20140727-PHY-Profile Table 6
        phy.profile_inputs.crc_poly.value = model.vars.crc_poly.var_enum.ANSIX366_1979  # 802.15.4-2015, 7.2.10

        # Default xtal frequency of 38.4MHz
        phy.profile_inputs.xtal_frequency_hz.value = 38400000

    def PHY_IEEE802154_WISUN_915MHz_2GFSK_150kbps_3_NA(self, model, phy_name=None):
        phy = PHYS_IEEE802154_WiSUN_Ocelot().PHY_IEEE802154_WISUN_915MHz_2GFSK_150kbps_3_NA(model)

        # Default xtal frequency of 38.4MHz
        phy.profile_inputs.xtal_frequency_hz.value = 38400000

    def PHY_IEEE802154_WISUN_868MHz_2GFSK_150kbps_3_EU(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.WiSUN, readable_name='Wi-SUN FAN, EU-868MHz, 3 (2FSK 150kbps mi=0.5)',
                            phy_name=phy_name)

        # Select the correct SUNFSK mode
        phy.profile_inputs.wisun_mode.value = model.vars.wisun_mode.var_enum.Mode3

        #Define WiSUN Profile / Region specific inputs
        phy.profile_inputs.base_frequency_hz.value = 863100000 # FAN NA Mode #3, WiSUN 20140727-PHY-Profile Table 3
        phy.profile_inputs.channel_spacing_hz.value = 200000 # FAN NA Mode #3, WiSUN 20140727-PHY-Profile Table 3
        phy.profile_inputs.preamble_length.value = 12 * 8 # FAN NA Mode #3, WiSUN 20140727-PHY-Profile Table 6
        phy.profile_inputs.crc_poly.value = model.vars.crc_poly.var_enum.ANSIX366_1979  # 802.15.4-2015, 7.2.10

        # Default xtal frequency of 38.4MHz
        phy.profile_inputs.xtal_frequency_hz.value = 38400000

    def PHY_IEEE802154_WISUN_873MHz_2GFSK_150kbps_3_EU(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.WiSUN, readable_name='Wi-SUN FAN, EU-873MHz, 3 (2FSK 150kbps mi=0.5)',
                            phy_name=phy_name)

        # Select the correct SUNFSK mode
        phy.profile_inputs.wisun_mode.value = model.vars.wisun_mode.var_enum.Mode3

        # Define WiSUN Profile / Region specific inputs
        phy.profile_inputs.base_frequency_hz.value = 870200000  # FAN NA Mode #3, WiSUN 20140727-PHY-Profile Table 3
        phy.profile_inputs.channel_spacing_hz.value = 200000  # FAN NA Mode #3, WiSUN 20140727-PHY-Profile Table 3
        phy.profile_inputs.preamble_length.value = 12 * 8  # FAN NA Mode #3, WiSUN 20140727-PHY-Profile Table 6
        phy.profile_inputs.crc_poly.value = model.vars.crc_poly.var_enum.ANSIX366_1979  # 802.15.4-2015, 7.2.10

        # Default xtal frequency of 38.4MHz
        phy.profile_inputs.xtal_frequency_hz.value = 38400000

    def PHY_IEEE802154_WISUN_866MHz_2GFSK_150kbps_3_IN(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.WiSUN, readable_name='Wi-SUN FAN, IN-866MHz, 3 (2FSK 150kbps mi=0.5)',
                            phy_name=phy_name)

        # Select the correct SUNFSK mode
        phy.profile_inputs.wisun_mode.value = model.vars.wisun_mode.var_enum.Mode3

        # Define WiSUN Profile / Region specific inputs
        phy.profile_inputs.base_frequency_hz.value = 865100000  # FAN NA Mode #3, WiSUN 20140727-PHY-Profile Table 3
        phy.profile_inputs.channel_spacing_hz.value = 200000  # FAN NA Mode #3, WiSUN 20140727-PHY-Profile Table 3
        phy.profile_inputs.preamble_length.value = 12 * 8  # FAN NA Mode #3, WiSUN 20140727-PHY-Profile Table 6
        phy.profile_inputs.crc_poly.value = model.vars.crc_poly.var_enum.ANSIX366_1979  # 802.15.4-2015, 7.2.10

        # Default xtal frequency of 38.4MHz
        phy.profile_inputs.xtal_frequency_hz.value = 38400000

    def PHY_IEEE802154_WISUN_922MHz_2GFSK_150kbps_3_VN(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.WiSUN, readable_name='Wi-SUN FAN, VN-922MHz, 3 (2FSK 150kbps mi=0.5)',
                            phy_name=phy_name)

        # Select the correct SUNFSK mode
        phy.profile_inputs.wisun_mode.value = model.vars.wisun_mode.var_enum.Mode3

        # Define WiSUN Profile / Region specific inputs
        phy.profile_inputs.base_frequency_hz.value = 920400000  # FAN NA Mode #3, WiSUN 20140727-PHY-Profile Table 3
        phy.profile_inputs.channel_spacing_hz.value = 400000  # FAN NA Mode #3, WiSUN 20140727-PHY-Profile Table 3
        phy.profile_inputs.preamble_length.value = 12 * 8  # FAN NA Mode #3, WiSUN 20140727-PHY-Profile Table 6
        phy.profile_inputs.crc_poly.value = model.vars.crc_poly.var_enum.ANSIX366_1979  # 802.15.4-2015, 7.2.10

        # Default xtal frequency of 38.4MHz
        phy.profile_inputs.xtal_frequency_hz.value = 38400000