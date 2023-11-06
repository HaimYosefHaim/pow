from pyradioconfig.parts.sol.phys.Phys_Studio_Connect import PHYS_Studio_Connect_Sol
from pyradioconfig.calculator_model_framework.interfaces.iphy import IPhy
from pyradioconfig.calculator_model_framework.interfaces.iphy import IPhy
from pyradioconfig.parts.ocelot.phys.Phys_Studio_Connect import PHYS_connect_Ocelot

class Phys_Internal_Connect(IPhy):

    def PHY_Datasheet_Connect_920MHz_2GFSK_100kbps(self, model):
        phy = PHYS_Studio_Connect_Sol().PHY_Studio_Connect_920MHz_2GFSK_100kbps(model,
                                                                         phy_name='PHY_Datasheet_Connect_920MHz_2GFSK_100kbps')
        phy.profile_inputs.rx_xtal_error_ppm.value = 0
        phy.profile_inputs.tx_xtal_error_ppm.value = 0

    def PHY_Datasheet_Connect_920MHz_2GFSK_100kbps_trecs_ANTDIV(self, model):
        phy = PHYS_Studio_Connect_Sol().PHY_Studio_Connect_920MHz_2GFSK_100kbps(model,
                                                                         phy_name='PHY_Datasheet_Connect_920MHz_2GFSK_100kbps_trecs_ANTDIV')
        phy.profile_inputs.rx_xtal_error_ppm.value = 0
        phy.profile_inputs.tx_xtal_error_ppm.value = 0
        phy.profile_inputs.preamble_length.value = 8 * 8

        phy.profile_outputs.MODEM_CTRL3_ANTDIVMODE.override = 5
        phy.profile_outputs.MODEM_PHDMODANTDIV_SKIP2ANT.override = 1
        phy.profile_outputs.MODEM_PHDMODANTDIV_ANTWAIT.override = 24

        phy.profile_outputs.MODEM_PHDMODANTDIV_SKIPRSSITHD.override = 10

        phy.profile_outputs.MODEM_AFC_AFCONESHOT.override = 1

        phy.profile_outputs.MODEM_REALTIMCFE_RTSCHWIN.override = 3
        phy.profile_outputs.MODEM_TRECPMDET_PMCOSTVALTHD.override = 2

        phy.profile_outputs.MODEM_PHDMODANTDIV_RECHKCORREN.override = 1

    def PHY_Datasheet_Connect_917MHz_2GFSK_4p8kbps(self, model):
        phy = self.PHY_Studio_Connect_917MHz_2GFSK_4p8kbps(model, phy_name='PHY_Datasheet_Connect_917MHz_2GFSK_4p8kbps')

        phy.profile_inputs.rx_xtal_error_ppm.value = 0
        phy.profile_inputs.tx_xtal_error_ppm.value = 0

    def PHY_Datasheet_Connect_915MHz_2GFSK_500kbps(self, model):
        phy = PHYS_Studio_Connect_Sol().PHY_Studio_Connect_915MHz_2GFSK_500kbps(model,
                                                                                phy_name='PHY_Datasheet_Connect_915MHz_2GFSK_500kbps')
        phy.profile_inputs.rx_xtal_error_ppm.value = 0
        phy.profile_inputs.tx_xtal_error_ppm.value = 0

    def PHY_Connect_915MHz_2GFSK_500kbps_bcr_antdiv(self, model, phy_name=None):
            phy = self._makePhy(model, model.profiles.Connect, 'US FCC 915, Brazil 915',
                                readable_name="PHY_Connect_915MHz 2GFSK 500kbps BCR antdiv")

            # : Common base funtion for all connect PHYs
            PHYS_connect_Ocelot().Connect_base(phy, model)
            phy.profile_inputs.rx_xtal_error_ppm.value = 20
            phy.profile_inputs.tx_xtal_error_ppm.value = 20
            phy.profile_inputs.deviation.value = 250000  # 175000
            phy.profile_inputs.base_frequency_hz.value = 915000000
            phy.profile_inputs.bitrate.value = 500000
            phy.profile_inputs.preamble_length.value = 64
            phy.profile_inputs.syncword_tx_skip.value = False
            phy.profile_inputs.asynchronous_rx_enable.value = False
            phy.profile_inputs.channel_spacing_hz.value = 400000
            phy.profile_inputs.test_ber.value = False
            phy.profile_inputs.fec_en.value = model.vars.fec_en.var_enum.NONE
            phy.profile_inputs.manchester_mapping.value = model.vars.manchester_mapping.var_enum.Default

            phy.profile_inputs.antdivmode.value = model.vars.antdivmode.var_enum.PHDEMODANTDIV

            return phy

    def PHY_Studio_Connect_917MHz_2GFSK_4p8kbps(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Connect, phy_description='Korea 915',
                            readable_name="Connect 917MHz 2GFSK 4.8kbps", phy_name=phy_name)

        # : Common base funtion for all connect PHYs
        PHYS_connect_Ocelot().Connect_base(phy, model)

        # Add data-rate specific parameters
        phy.profile_inputs.bitrate.value = 4800
        phy.profile_inputs.deviation.value = 2400

        # Add band-specific parameters
        phy.profile_inputs.base_frequency_hz.value = 917100000
        phy.profile_inputs.channel_spacing_hz.value = 200000

        return phy
