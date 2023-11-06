from pyradioconfig.parts.common.phys.phy_common import PHY_COMMON_FRAME_154
from pyradioconfig.parts.lynx.phys.PHY_internal_base import Phy_Internal_Base_Lynx
from pyradioconfig.calculator_model_framework.interfaces.iphy import IPhy
from pyradioconfig.parts.lynx.phys.Phys_IEEE802154 import PHYS_IEEE802154_Lynx

from py_2_and_3_compatibility import *

class Phys_Internal_Base_Standard_SUNFSK_Sol(IPhy):
    # Inherit none

    # Reference \\silabs.com\mcuandwireless\026 Shared Docs\0260_Standards\std_body\IEEE_802_15_4\IEEE Std 802.15.4-2015.pdf
    # Ch 20. SUN FSK PHY
    def SUN_FSK_2GFSK_base(self, phy, model):

        # General Inputs
        phy.profile_inputs.diff_encoding_mode.value = model.vars.diff_encoding_mode.var_enum.DISABLED
        phy.profile_inputs.dsss_chipping_code.value = long(0)
        phy.profile_inputs.dsss_len.value = 0
        phy.profile_inputs.dsss_spreading_factor.value = 0
        phy.profile_inputs.fec_en.value = model.vars.fec_en.var_enum.NONE
        phy.profile_inputs.fsk_symbol_map.value = model.vars.fsk_symbol_map.var_enum.MAP0  # Table 20.8.SUN 2-FSK symbol encoding
        phy.profile_inputs.modulation_type.value = model.vars.modulation_type.var_enum.FSK2
        phy.profile_inputs.preamble_pattern.value = 1
        phy.profile_inputs.preamble_pattern_len.value = 2
        phy.profile_inputs.shaping_filter.value = model.vars.shaping_filter.var_enum.Gaussian  # 17.2.4 GFSK modulation
        phy.profile_inputs.shaping_filter_param.value = 0.5
        # TODO: Do we support both uncoded and coded?  If so, need to create additional config's
        phy.profile_inputs.syncword_0.value = 0b1001000001001110  # Table 20.2.SUN FSK PHY SFD values for 2-FSK (uncoded), page 494
        #phy.profile_inputs.syncword_0.value = 0b0110111101001110  # Table 20.2.SUN FSK PHY SFD values for 2-FSK (FEC coded), page 494
        phy.profile_inputs.syncword_1.value = long(0)
        phy.profile_inputs.syncword_length.value = 16
        phy.profile_inputs.syncword_tx_skip.value = False
        phy.profile_inputs.xtal_frequency_hz.value = 38400000

        # Packet Inputs
        phy.profile_inputs.frame_length_type.value = model.vars.frame_length_type.var_enum.VARIABLE_LENGTH
        phy.profile_inputs.frame_bitendian.value = model.vars.frame_bitendian.var_enum.MSB_FIRST
        phy.profile_inputs.payload_crc_en.value = True
        phy.profile_inputs.payload_addtrailtxdata_en.value = False

        # Variable length includes header
        phy.profile_inputs.header_calc_crc.value = True
        phy.profile_inputs.header_en.value = True
        phy.profile_inputs.header_size.value = 8
        phy.profile_inputs.header_white_en.value = True  # 17.2.3 Data whitening. Support for data whitening is optional.

        # Whitening Inputs
        phy.profile_inputs.white_poly.value = model.vars.white_poly.var_enum.PN9
        phy.profile_inputs.white_seed.value = 0b111111111
        phy.profile_inputs.white_output_bit.value = 0

        # CRC Inputs
        phy.profile_inputs.crc_bit_endian.value = model.vars.crc_bit_endian.var_enum.MSB_FIRST
        phy.profile_inputs.crc_byte_endian.value = model.vars.crc_byte_endian.var_enum.MSB_FIRST
        phy.profile_inputs.crc_input_order.value = model.vars.crc_input_order.var_enum.MSB_FIRST
        phy.profile_inputs.crc_invert.value = False
        phy.profile_inputs.crc_pad_input.value = False

    # Created for marketing request - named Internal because it doesn't exactly match any of the SUN FSK operating modes
    def PHY_Internal_SUN_FSK_915MHz_2FSK_9p6kbps_mi1p0_trecs(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='IEEE 802.15.4 SUN FSK 915MHz 2FSK 9.6kbps mi=1.0', phy_name=phy_name)

        self.SUN_FSK_2GFSK_base(phy, model)
        phy.profile_inputs.base_frequency_hz.value = long(902200000)     # Freq mapping Table 10.10. 50Kbps Operating mode in 902-928
        phy.profile_inputs.baudrate_tol_ppm.value = 300                 # 802.15.4-2015, 20.6.5
        phy.profile_inputs.bitrate.value = 9600
        phy.profile_inputs.channel_spacing_hz.value = 200000            # Freq mapping Table 10.10. 50Kbps Operating mode in 902-928
        phy.profile_inputs.crc_poly.value = model.vars.crc_poly.var_enum.CCITT_16  # 802.15.4-2015, 7.2.10 (assume 16bits)
        phy.profile_inputs.crc_seed.value = long(0x0000)                # 802.15.4-2015, 7.2.10 Figure 7-4 (assume 16bits)
        phy.profile_inputs.deviation.value = 4800                       # 9600*1.0 / 2
        phy.profile_inputs.preamble_length.value = 8 * 8                # phyFskPreambleLength = 8 (assume 64bits)
        phy.profile_inputs.rx_xtal_error_ppm.value = 6                  # 0802.15.4-2015, 20.6.3 Equation = 6
        phy.profile_inputs.tx_xtal_error_ppm.value = 6                  # 0802.15.4-2015, 20.6.3 Equation = 6

        return phy

    # Created for marketing request - named Internal because it doesn't exactly match any of the SUN FSK operating modes
    def PHY_Internal_SUN_FSK_915MHz_2FSK_10kbps_mi0p5_trecs(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='IEEE 802.15.4 SUN FSK 915MHz 2FSK 10kbps mi=0.5', phy_name=phy_name)

        self.SUN_FSK_2GFSK_base(phy, model)
        phy.profile_inputs.base_frequency_hz.value = long(902200000)     # Freq mapping Table 10.10. 50Kbps Operating mode in 902-928
        phy.profile_inputs.baudrate_tol_ppm.value = 300                 # 802.15.4-2015, 20.6.5
        phy.profile_inputs.bitrate.value = 10000
        phy.profile_inputs.channel_spacing_hz.value = 200000            # Freq mapping Table 10.10. 50Kbps Operating mode in 902-928
        phy.profile_inputs.crc_poly.value = model.vars.crc_poly.var_enum.CCITT_16  # 802.15.4-2015, 7.2.10 (assume 16bits)
        phy.profile_inputs.crc_seed.value = long(0x0000)                # 802.15.4-2015, 7.2.10 Figure 7-4 (assume 16bits)
        phy.profile_inputs.deviation.value = 2500                       # 10000*0.5 / 2
        phy.profile_inputs.preamble_length.value = 8 * 8                # phyFskPreambleLength = 8 (assume 64bits)
        phy.profile_inputs.rx_xtal_error_ppm.value = 3                  # 0802.15.4-2015, 20.6.3 Equation = 3
        phy.profile_inputs.tx_xtal_error_ppm.value = 3                  # 0802.15.4-2015, 20.6.3 Equation = 3
        #phy.profile_outputs.MODEM_VITERBIDEMOD_VITERBIKSI1.override = 64
        #phy.profile_outputs.MODEM_VITERBIDEMOD_VITERBIKSI2.override = 42
        #phy.profile_outputs.MODEM_VITERBIDEMOD_VITERBIKSI3.override = 27

        return phy

    # Created for marketing request
    def PHY_Internal_SUN_FSK_866MHz_2FSK_50kbps_mi0p5_trecs(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='IEEE 802.15.4 SUN FSK 866MHz 2FSK 50kbps mi=0.5', phy_name=phy_name)

        self.SUN_FSK_2GFSK_base(phy, model)
        phy.profile_inputs.base_frequency_hz.value = long(863125000)    # Freq mapping Table 10.10. 50Kbps Operating mode in 863-870
        phy.profile_inputs.baudrate_tol_ppm.value = 300                 # 802.15.4-2015, 20.6.5
        phy.profile_inputs.bitrate.value = 50000
        phy.profile_inputs.channel_spacing_hz.value = 200000            # Freq mapping Table 10.10. 50Kbps Operating mode in 863-870
        phy.profile_inputs.crc_poly.value = model.vars.crc_poly.var_enum.CCITT_16  # 802.15.4-2015, 7.2.10 (assume 16bits)
        phy.profile_inputs.crc_seed.value = long(0x0000)                # 802.15.4-2015, 7.2.10 Figure 7-4 (assume 16bits)
        phy.profile_inputs.deviation.value = 12500                       # 50000*0.5 / 2
        phy.profile_inputs.preamble_length.value = 8 * 8                # phyFskPreambleLength = 8 (assume 64bits)
        phy.profile_inputs.rx_xtal_error_ppm.value = 16                 # 0802.15.4-2015, 20.6.3 Equation = 16
        phy.profile_inputs.tx_xtal_error_ppm.value = 16                 # 0802.15.4-2015, 20.6.3 Equation = 16
        phy.profile_inputs.target_osr.value = 5
        #phy.profile_outputs.MODEM_VITERBIDEMOD_VITERBIKSI1.override = 64
        #phy.profile_outputs.MODEM_VITERBIDEMOD_VITERBIKSI2.override = 45
        #phy.profile_outputs.MODEM_VITERBIDEMOD_VITERBIKSI3.override = 29

        return phy

    # Created for marketing request
    def PHY_Internal_SUN_FSK_915MHz_2FSK_50kbps_mi1p0_trecs(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='IEEE 802.15.4 SUN FSK 915MHz 2FSK 50kbps mi=1.0', phy_name=phy_name)

        self.SUN_FSK_2GFSK_base(phy, model)
        phy.profile_inputs.base_frequency_hz.value = long(902200000)    # Freq mapping Table 10.10. 50Kbps Operating mode in 902-928
        phy.profile_inputs.baudrate_tol_ppm.value = 300                 # 802.15.4-2015, 20.6.5
        phy.profile_inputs.bitrate.value = 50000
        phy.profile_inputs.channel_spacing_hz.value = 200000            # Freq mapping Table 10.10. 50Kbps Operating mode in 902-928
        phy.profile_inputs.crc_poly.value = model.vars.crc_poly.var_enum.CCITT_16  # 802.15.4-2015, 7.2.10 (assume 16bits)
        phy.profile_inputs.crc_seed.value = long(0x0000)                # 802.15.4-2015, 7.2.10 Figure 7-4 (assume 16bits)
        phy.profile_inputs.deviation.value = 25000                      # 50000*1.0 / 2
        phy.profile_inputs.preamble_length.value = 8 * 8                # phyFskPreambleLength = 8 (assume 64bits)
        phy.profile_inputs.rx_xtal_error_ppm.value = 30                 # 0802.15.4-2015, 20.6.3 Equation = 30
        phy.profile_inputs.tx_xtal_error_ppm.value = 30                 # 0802.15.4-2015, 20.6.3 Equation = 30

        return phy

    # Created for marketing request
    def PHY_Internal_SUN_FSK_915MHz_2FSK_200kbps_mi0p5_trecs(self, model, phy_name=None):
        phy = self._makePhy(model, model.profiles.Base, readable_name='IEEE 802.15.4 SUN FSK 915MHz 2FSK 200kbps mi=0.5', phy_name=phy_name)

        self.SUN_FSK_2GFSK_base(phy, model)
        phy.profile_inputs.base_frequency_hz.value = long(902600000)    # Freq mapping Table 10.10.  200Kbps Operating mode #3 in 902-928
        phy.profile_inputs.baudrate_tol_ppm.value = 300                 # 802.15.4-2015, 20.6.5
        phy.profile_inputs.bitrate.value = 200000
        phy.profile_inputs.channel_spacing_hz.value = 400000            # Freq mapping Table 10.10. 200Kbps Operating mode #3 in 902-928
        phy.profile_inputs.crc_poly.value = model.vars.crc_poly.var_enum.CCITT_16  # 802.15.4-2015, 7.2.10 (assume 16bits)
        phy.profile_inputs.crc_seed.value = long(0x0000)                # 802.15.4-2015, 7.2.10 Figure 7-4 (assume 16bits)
        phy.profile_inputs.deviation.value = 50000                      # 200000*0.5 / 2
        phy.profile_inputs.preamble_length.value = 8 * 8                # phyFskPreambleLength = 8 (assume 64bits)
        phy.profile_inputs.rx_xtal_error_ppm.value = 50                 # 0802.15.4-2015, 20.6.3 Equation = 30
        phy.profile_inputs.tx_xtal_error_ppm.value = 50                 # 0802.15.4-2015, 20.6.3 Equation = 30
        phy.profile_inputs.target_osr.value = 5

        # KSI values for BT=0.5 (calc_ksi_wdec1.m)
        #phy.profile_outputs.MODEM_VITERBIDEMOD_VITERBIKSI1.override = 64
        #phy.profile_outputs.MODEM_VITERBIDEMOD_VITERBIKSI2.override = 45
        #phy.profile_outputs.MODEM_VITERBIDEMOD_VITERBIKSI3.override = 29

        # KSI values for BT=2 (calc_ksi_wdec1.m)
        #phy.profile_inputs.shaping_filter_param.value = 2.0
        #phy.profile_outputs.MODEM_VITERBIDEMOD_VITERBIKSI1.override = 64
        #phy.profile_outputs.MODEM_VITERBIDEMOD_VITERBIKSI2.override = 49
        #phy.profile_outputs.MODEM_VITERBIDEMOD_VITERBIKSI3.override = 39


        return phy
