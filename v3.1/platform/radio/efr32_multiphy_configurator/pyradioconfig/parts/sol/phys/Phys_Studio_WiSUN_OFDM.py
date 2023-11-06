from pyradioconfig.calculator_model_framework.interfaces.iphy import IPhy

class Phys_Studio_WiSUN_OFDM_Sol(IPhy):

    # Owner: Casey Weltzin
    # Jira Link: https://jira.silabs.com/browse/PGSOLVALTEST-2 through https://jira.silabs.com/browse/PGSOLVALTEST-8
    def PHY_IEEE802154_WISUN_868MHz_OFDM_OPT1(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.WiSUN_OFDM, readable_name='Wi-SUN EU-868MHz, OFDM OPTION 1',
                            phy_name=phy_name)

        # Select the correct Wi-SUN OFDM Option
        phy.profile_inputs.ofdm_option.value = model.vars.ofdm_option.var_enum.OPT1

        # Define WiSUN Profile / Region specific inputs
        phy.profile_inputs.base_frequency_hz.value = 863100000
        phy.profile_inputs.channel_spacing_hz.value = 1200000
        phy.profile_inputs.fcs_type_802154.value = model.vars.fcs_type_802154.var_enum.FOUR_BYTE

        # Default xtal frequency of 39MHz
        phy.profile_inputs.xtal_frequency_hz.value = 39000000

    # Owner: Casey Weltzin
    # Jira Link: https://jira.silabs.com/browse/PGSOLVALTEST-9 through https://jira.silabs.com/browse/PGSOLVALTEST-15
    def PHY_IEEE802154_WISUN_868MHz_OFDM_OPT2(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.WiSUN_OFDM, readable_name='Wi-SUN EU-868MHz, OFDM OPTION 2',
                            phy_name=phy_name)

        # Select the correct Wi-SUN OFDM Option
        phy.profile_inputs.ofdm_option.value = model.vars.ofdm_option.var_enum.OPT2

        # Define WiSUN Profile / Region specific inputs
        phy.profile_inputs.base_frequency_hz.value = 863100000
        phy.profile_inputs.channel_spacing_hz.value = 800000
        phy.profile_inputs.fcs_type_802154.value = model.vars.fcs_type_802154.var_enum.FOUR_BYTE

        # Default xtal frequency of 39MHz
        phy.profile_inputs.xtal_frequency_hz.value = 39000000

    # Owner: Casey Weltzin
    # Jira Link: https://jira.silabs.com/browse/PGSOLVALTEST-16 through https://jira.silabs.com/browse/PGSOLVALTEST-22
    def PHY_IEEE802154_WISUN_868MHz_OFDM_OPT3(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.WiSUN_OFDM, readable_name='Wi-SUN EU-868MHz, OFDM OPTION 3',
                            phy_name=phy_name)

        # Select the correct Wi-SUN OFDM Option
        phy.profile_inputs.ofdm_option.value = model.vars.ofdm_option.var_enum.OPT3

        # Define WiSUN Profile / Region specific inputs
        phy.profile_inputs.base_frequency_hz.value = 863100000
        phy.profile_inputs.channel_spacing_hz.value = 400000
        phy.profile_inputs.fcs_type_802154.value = model.vars.fcs_type_802154.var_enum.FOUR_BYTE

        # Default xtal frequency of 39MHz
        phy.profile_inputs.xtal_frequency_hz.value = 39000000

    # Owner: Casey Weltzin
    # Jira Link: https://jira.silabs.com/browse/PGSOLVALTEST-23 through https://jira.silabs.com/browse/PGSOLVALTEST-29
    def PHY_IEEE802154_WISUN_868MHz_OFDM_OPT4(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.WiSUN_OFDM, readable_name='Wi-SUN EU-868MHz, OFDM OPTION 4',
                            phy_name=phy_name)

        # Select the correct Wi-SUN OFDM Option
        phy.profile_inputs.ofdm_option.value = model.vars.ofdm_option.var_enum.OPT4

        # Define WiSUN Profile / Region specific inputs
        phy.profile_inputs.base_frequency_hz.value = 863100000
        phy.profile_inputs.channel_spacing_hz.value = 200000
        phy.profile_inputs.fcs_type_802154.value = model.vars.fcs_type_802154.var_enum.FOUR_BYTE

        # Default xtal frequency of 39MHz
        phy.profile_inputs.xtal_frequency_hz.value = 39000000