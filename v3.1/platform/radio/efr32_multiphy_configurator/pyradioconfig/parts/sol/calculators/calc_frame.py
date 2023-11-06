from pyradioconfig.parts.ocelot.calculators.calc_frame import CALC_Frame_ocelot

class Calc_Frame_Sol(CALC_Frame_ocelot):

    def calc_rxctrl_ifinputwidth_reg(self, model):
        #This method calculates the IFINPUTWIDTH field

        #Read in model vars
        demod_select = model.vars.demod_select.value

        #Calculate the field
        if demod_select == model.vars.demod_select.var_enum.SOFT_DEMOD:
            ifinputwidth = 3
        else:
            ifinputwidth = 0

        #Write the register
        self._reg_write(model.vars.FRC_RXCTRL_IFINPUTWIDTH, ifinputwidth)

    def calc_ctrl_lpmodedis_reg(self, model):
        #This method calculates the LPMODEDIS field

        #Read in model vars
        demod_select = model.vars.demod_select.value

        # Calculate the field
        if demod_select == model.vars.demod_select.var_enum.SOFT_DEMOD:
            lpmodedis = 1
        else:
            lpmodedis = 0

        # Write the register
        self._reg_write(model.vars.FRC_CTRL_LPMODEDIS, lpmodedis)