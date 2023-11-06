
# -*- coding: utf-8 -*-

from . static import Base_RM_Field


class RM_Field_CW_CWCFG1_MODULATION(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_CW_CWCFG1_MODULATION, self).__init__(register,
            'MODULATION', 'CW.CWCFG1.MODULATION', 'read-write',
            u"",
            0, 8)
        self.__dict__['zz_frozen'] = True


class RM_Field_CW_CWCFG1_FREQ(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_CW_CWCFG1_FREQ, self).__init__(register,
            'FREQ', 'CW.CWCFG1.FREQ', 'read-write',
            u"",
            16, 16)
        self.__dict__['zz_frozen'] = True


class RM_Field_CW_CWCFG2_AMP(Base_RM_Field):
    def __init__(self, register):
        self.__dict__['zz_frozen'] = False
        super(RM_Field_CW_CWCFG2_AMP, self).__init__(register,
            'AMP', 'CW.CWCFG2.AMP', 'read-write',
            u"",
            0, 16)
        self.__dict__['zz_frozen'] = True


