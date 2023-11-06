from pyradioconfig.parts.ocelot.calculators.calc_agc import CALC_AGC_ocelot

class Calc_AGC_Bobcat(CALC_AGC_ocelot):

    def calc_lnamixrfatt_reg(self, model):

        #Values from Sanjeev Suresh

        lnamixrfatt = [0, 1, 2, 4, 6, 8, 11, 15, 18, 24, 31, 33, 47, 63, 110, 127]
        pnindexmax = 14

        #Write registers
        self._reg_write(model.vars.AGC_PNRFATT0_LNAMIXRFATT1, lnamixrfatt[0])
        self._reg_write(model.vars.AGC_PNRFATT0_LNAMIXRFATT2, lnamixrfatt[1])
        self._reg_write(model.vars.AGC_PNRFATT0_LNAMIXRFATT3, lnamixrfatt[2])
        self._reg_write(model.vars.AGC_PNRFATT1_LNAMIXRFATT4, lnamixrfatt[3])
        self._reg_write(model.vars.AGC_PNRFATT1_LNAMIXRFATT5, lnamixrfatt[4])
        self._reg_write(model.vars.AGC_PNRFATT1_LNAMIXRFATT6, lnamixrfatt[5])
        self._reg_write(model.vars.AGC_PNRFATT2_LNAMIXRFATT7, lnamixrfatt[6])
        self._reg_write(model.vars.AGC_PNRFATT2_LNAMIXRFATT8, lnamixrfatt[7])
        self._reg_write(model.vars.AGC_PNRFATT2_LNAMIXRFATT9, lnamixrfatt[8])
        self._reg_write(model.vars.AGC_PNRFATT3_LNAMIXRFATT10, lnamixrfatt[9])
        self._reg_write(model.vars.AGC_PNRFATT3_LNAMIXRFATT11, lnamixrfatt[10])
        self._reg_write(model.vars.AGC_PNRFATT3_LNAMIXRFATT12, lnamixrfatt[11])
        self._reg_write(model.vars.AGC_PNRFATT4_LNAMIXRFATT13, lnamixrfatt[12])
        self._reg_write(model.vars.AGC_PNRFATT4_LNAMIXRFATT14, lnamixrfatt[13])
        self._reg_write(model.vars.AGC_PNRFATT4_LNAMIXRFATT15, lnamixrfatt[14])
        self._reg_write(model.vars.AGC_PNRFATT5_LNAMIXRFATT16, 0)
        self._reg_write(model.vars.AGC_PNRFATT5_LNAMIXRFATT17, 0)
        self._reg_write(model.vars.AGC_PNRFATT5_LNAMIXRFATT18, 0)
        self._reg_write(model.vars.AGC_PNRFATT6_LNAMIXRFATT19, 0)
        self._reg_write(model.vars.AGC_PNRFATT6_LNAMIXRFATT20, 0)
        self._reg_write(model.vars.AGC_PNRFATT6_LNAMIXRFATT21, 0)
        self._reg_write(model.vars.AGC_PNRFATT7_LNAMIXRFATT22, 0)
        self._reg_write(model.vars.AGC_PNRFATT7_LNAMIXRFATT23, 0)
        self._reg_write(model.vars.AGC_PNRFATT7_LNAMIXRFATT24, 0)

        self._reg_write(model.vars.AGC_GAINSTEPLIM1_PNINDEXMAX, pnindexmax)

    def calc_lnamixenrfpkdlothresh_reg(self, model):
        pass
