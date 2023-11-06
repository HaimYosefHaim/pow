from pyradioconfig.calculator_model_framework.interfaces.iphy import IPhy
from pyradioconfig.parts.sol.phys.Phys_Studio_Base import PHYS_Studio_Base_Sol
from pyradioconfig.parts.sol.phys.Phys_Studio_Connect import PHYS_Studio_Connect_Sol

class PHYS_Internal_Base_ValOnly_Sol(IPhy):

    ##########Datasheet PHYs##########

    # These PHYs call the PHYs we expose in Studio, but set the xtal tol to 0ppm for spec setting

    # Owner: Casey Weltzin
    # Jira Link: https://jira.silabs.com/browse/PGSOLVALTEST-48
    def PHY_Datasheet_915M_2GFSK_2Mbps_500K(self, model, phy_name=None):
        phy = PHYS_Studio_Base_Sol().PHY_Studio_915M_2GFSK_2Mbps_500K(model, phy_name='PHY_Datasheet_915M_2GFSK_2Mbps_500K')

        phy.profile_inputs.rx_xtal_error_ppm.value = 0
        phy.profile_inputs.tx_xtal_error_ppm.value = 0

    # Owner: Casey Weltzin
    # Jira Link: https://jira.silabs.com/browse/PGSOLVALTEST-47
    def PHY_Datasheet_915M_2GFSK_500Kbps_175K_mi0p7(self, model, phy_name=None):
        phy = PHYS_Studio_Base_Sol().PHY_Studio_915M_2GFSK_500Kbps_175K_mi0p7(model, phy_name = 'PHY_Datasheet_915M_2GFSK_500Kbps_175K_mi0p7')

        phy.profile_inputs.rx_xtal_error_ppm.value = 0
        phy.profile_inputs.tx_xtal_error_ppm.value = 0

    # Owner: Casey Weltzin
    # Jira Link: https://jira.silabs.com/browse/PGSOLVALTEST-82
    def PHY_Datasheet_915M_2GFSK_600bps_800(self, model, phy_name=None):
        phy = PHYS_Studio_Base_Sol().PHY_Studio_915M_2GFSK_600bps_800(model, phy_name = 'PHY_Datasheet_915M_2GFSK_600bps_800')

        phy.profile_inputs.rx_xtal_error_ppm.value = 0
        phy.profile_inputs.tx_xtal_error_ppm.value = 0

    # Owner: Casey Weltzin
    # Jira Link: https://jira.silabs.com/browse/PGSOLVALTEST-49
    def PHY_Datasheet_868M_GMSK_500Kbps(self, model, phy_name=None):
        phy = PHYS_Studio_Base_Sol().PHY_Studio_868M_GMSK_500Kbps(model, phy_name = 'PHY_Datasheet_868M_GMSK_500Kbps')

        phy.profile_inputs.rx_xtal_error_ppm.value = 0
        phy.profile_inputs.tx_xtal_error_ppm.value = 0

    # Owner: Casey Weltzin
    # Jira Link: https://jira.silabs.com/browse/PGSOLVALTEST-51
    def PHY_Datasheet_868M_2GFSK_38p4Kbps_20K(self, model, phy_name=None):
        phy = PHYS_Studio_Base_Sol().PHY_Studio_868M_2GFSK_38p4Kbps_20K(model, phy_name = 'PHY_Datasheet_868M_2GFSK_38p4Kbps_20K')

        phy.profile_inputs.rx_xtal_error_ppm.value = 0
        phy.profile_inputs.tx_xtal_error_ppm.value = 0

    # Owner: Casey Weltzin
    # Jira Link: https://jira.silabs.com/browse/PGSOLVALTEST-50
    def PHY_Datasheet_868M_2GFSK_600bps_800(self, model, phy_name=None):
        phy = PHYS_Studio_Base_Sol().PHY_Studio_868M_2GFSK_600bps_800(model, phy_name = 'PHY_Datasheet_868M_2GFSK_600bps_800')

        phy.profile_inputs.rx_xtal_error_ppm.value = 0
        phy.profile_inputs.tx_xtal_error_ppm.value = 0

    # Owner: Casey Weltzin
    # Jira Link: https://jira.silabs.com/browse/PGSOLVALTEST-52
    def PHY_Datasheet_490M_2GFSK_38p4Kbps_20K(self, model, phy_name=None):
        phy = PHYS_Studio_Base_Sol().PHY_Studio_490M_2GFSK_38p4Kbps_20K(model, phy_name = 'PHY_Datasheet_490M_2GFSK_38p4Kbps_20K')

        phy.profile_inputs.rx_xtal_error_ppm.value = 0
        phy.profile_inputs.tx_xtal_error_ppm.value = 0

    # Owner: Casey Weltzin
    # Jira Link: https://jira.silabs.com/browse/PGSOLVALTEST-53
    def PHY_Datasheet_490M_2GFSK_10Kbps_5K(self, model, phy_name=None):
        phy = PHYS_Studio_Base_Sol().PHY_Studio_490M_2GFSK_10Kbps_5K(model, phy_name = 'PHY_Datasheet_490M_2GFSK_10Kbps_5K')

        phy.profile_inputs.rx_xtal_error_ppm.value = 0
        phy.profile_inputs.tx_xtal_error_ppm.value = 0

    # Owner: Casey Weltzin
    # Jira Link: https://jira.silabs.com/browse/PGSOLVALTEST-54
    def PHY_Datasheet_490M_2GFSK_2p4Kbps_1p2K(self, model, phy_name=None):
        phy = PHYS_Studio_Base_Sol().PHY_Studio_490M_2GFSK_2p4Kbps_1p2K(model, phy_name = 'PHY_Datasheet_490M_2GFSK_2p4Kbps_1p2K')

        phy.profile_inputs.rx_xtal_error_ppm.value = 0
        phy.profile_inputs.tx_xtal_error_ppm.value = 0

    # Owner: Casey Weltzin
    # Jira Link: https://jira.silabs.com/browse/PGSOLVALTEST-46
    def PHY_Datasheet_915M_4GFSK_200Kbps_16p6K(self, model, phy_name=None):
        phy = PHYS_Studio_Base_Sol().PHY_Studio_915M_4GFSK_200Kbps_16p6K(model, phy_name = 'PHY_Datasheet_915M_4GFSK_200Kbps_16p6K')

        phy.profile_inputs.rx_xtal_error_ppm.value = 0
        phy.profile_inputs.tx_xtal_error_ppm.value = 0

    # Owner: Casey Weltzin
    # Jira Link: https://jira.silabs.com/browse/PGSOLVALTEST-45
    def PHY_Datasheet_Connect_920MHz_2GFSK_100kbps(self, model, phy_name=None):
        phy = PHYS_Studio_Connect_Sol().PHY_Studio_Connect_920MHz_2GFSK_100kbps(model, phy_name='PHY_Datasheet_Connect_920MHz_2GFSK_100kbps')

        phy.profile_inputs.rx_xtal_error_ppm.value = 0
        phy.profile_inputs.tx_xtal_error_ppm.value = 0

    # Owner: Casey Weltzin
    # Jira Link: https://jira.silabs.com/browse/PGSOLVALTEST-43
    def PHY_Datasheet_Connect_915MHz_2GFSK_500kbps(self, model, phy_name=None):
        phy = PHYS_Studio_Connect_Sol().PHY_Studio_Connect_915MHz_2GFSK_500kbps(model, phy_name='PHY_Datasheet_Connect_915MHz_2GFSK_500kbps')

        phy.profile_inputs.rx_xtal_error_ppm.value = 0
        phy.profile_inputs.tx_xtal_error_ppm.value = 0

    # Owner: Casey Weltzin
    # Jira Link: https://jira.silabs.com/browse/PGSOLVALTEST-44
    def PHY_Datasheet_Connect_863MHz_2GFSK_100kbps(self, model, phy_name=None):
        phy = PHYS_Studio_Connect_Sol().PHY_Studio_Connect_863MHz_2GFSK_100kbps(model, phy_name='PHY_Datasheet_Connect_863MHz_2GFSK_100kbps')

        phy.profile_inputs.rx_xtal_error_ppm.value = 0
        phy.profile_inputs.tx_xtal_error_ppm.value = 0

    # Owner: Casey Weltzin
    # Jira Link: https://jira.silabs.com/browse/PGSOLVALTEST-42
    def PHY_Datasheet_Connect_490MHz_2GFSK_200kbps(self, model, phy_name=None):
        phy = PHYS_Studio_Connect_Sol().PHY_Studio_Connect_490MHz_2GFSK_200kbps(model, phy_name='PHY_Datasheet_Connect_490MHz_2GFSK_200kbps')

        phy.profile_inputs.rx_xtal_error_ppm.value = 0
        phy.profile_inputs.tx_xtal_error_ppm.value = 0