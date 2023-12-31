'''
Created on Aug 22, 2013

@author: sesuskic
'''

__all__ = ["RampData"]

class RampData(object):

    # ---- Ramp Data  ----
    # Manchester Lookup 

    RampData_Manch_DataRate   = [0, 0.5, 1, 11.204, 11.345, 11.451, 11.542, 11.623, 11.698, 11.77,\
                                  11.839, 11.908, 11.979, 12.05, 12.126, 12.206, 12.294, 12.397, 12.521, 12.695,\
                                  13.096, 14.998, 15.235, 15.396, 15.526, 15.634, 15.729, 15.819, 15.9, 15.977,\
                                  16.048, 16.12, 16.186, 16.252, 16.316, 16.377, 16.442, 16.501, 16.564, 16.627,\
                                  16.687, 16.747, 16.812, 16.873, 16.939, 17.005, 17.071, 17.142, 17.213, 17.288,\
                                  17.364, 17.448, 17.533, 17.63, 17.731, 17.846, 17.973, 18.122, 18.302, 18.552,\
                                  18.98, 22.622, 23.178, 23.493, 23.728, 23.919, 24.079, 24.227, 24.354, 24.477,\
                                  24.593, 24.695, 24.791, 24.888, 24.977, 25, ]

    RampData_Manch_RampRate   = [8, 4, 2, 2.0528, 2.1155, 2.1831, 2.2526, 2.323, 2.3935, 2.464,\
                                  2.5341, 2.6033, 2.6714, 2.7386, 2.804, 2.8675, 2.9281, 2.9845, 3.035, 3.0721,\
                                  3.0545, 2.7337, 2.7568, 2.7929, 2.834, 2.8784, 2.9246, 2.9712, 3.0188, 3.0669,\
                                  3.1157, 3.1638, 3.2127, 3.2611, 3.3096, 3.3583, 3.4059, 3.4543, 3.5017, 3.5485,\
                                  3.5957, 3.6424, 3.6879, 3.7337, 3.7783, 3.8225, 3.8662, 3.9086, 3.9506, 3.9912,\
                                  4.0313, 4.0692, 4.1066, 4.1408, 4.1734, 4.2027, 4.2285, 4.2489, 4.2618, 4.2584,\
                                  4.2149, 3.5806, 3.5379, 3.533, 3.5401, 3.5536, 3.5716, 3.5911, 3.6133, 3.6361,\
                                  3.6596, 3.685, 3.711, 3.7368, 3.7634, 3.7908, ]

    RampData_NRZ_DataRate     = [0, 0.5, 1, 31.74, 31.85, 31.96, 32.071, 32.171, 32.271, 32.371,\
                                  32.473, 32.575, 32.664, 32.767, 32.858, 32.963, 33.055, 33.147, 33.24, 33.333,\
                                  33.427, 33.522, 33.617, 33.712, 33.809, 33.905, 34.002, 34.1, 34.199, 34.298,\
                                  34.397, 34.497, 34.598, 34.714, 34.815, 34.918, 35.036, 35.14, 35.259, 35.379,\
                                  35.5, 35.622, 35.745, 35.884, 36.009, 36.166, 36.308, 36.467, 36.628, 36.807,\
                                  36.988, 37.186, 37.404, 37.642, 37.917, 38.249, 38.641, 39.206, 40.607, 43.753,\
                                  44.409, 44.865, 45.256, 45.554, 45.856, 46.111, 46.343, 46.551, 46.761, 46.946,\
                                  47.132, 47.32, 47.483, 47.646, 47.784, 47.949, 48.088, 48.228, 48.368, 48.51,\
                                  48.623, 48.766, 48.881, 48.996, 49.112, 49.229, 49.346, 49.464, 49.582, 49.701,\
                                  49.79, 49.91, 50, 50.121, 50.212, 50.303, 50.425, 50.517, 50.61, 50.703,\
                                  50.796, 50.889, 50.983, 51.077, 51.171, 51.266, 51.361, 51.457, 51.553, 51.649,\
                                  51.713, 51.81, 51.907, 51.972, 52.07, 52.168, 52.234, 52.333, 52.399, 52.498,\
                                  52.565, 52.665, 52.732, 52.833, 52.9, 53.001, 53.069, 53.171, 53.239, 53.308,\
                                  53.411, 53.479, 53.548, 53.652, 53.722, 53.791, 53.896, 53.966, 54.036, 54.107,\
                                  54.213, 54.284, 54.355, 54.426, 54.498, 54.605, 54.677, 54.749, 54.822, 54.894,\
                                  54.967, 55.076, 55.15, 55.223, 55.296, 55.37, 55.444, 55.518, 55.593, 55.705,\
                                  55.78, 55.855, 55.93, 56.005, 56.081, 56.157, 56.233, 56.309, 56.386, 56.463,\
                                  56.578, 56.655, 56.733, 56.81, 56.888, 56.966, 57.045, 57.123, 57.202, 57.281,\
                                  57.36, 57.439, 57.519, 57.599, 57.679, 57.799, 57.88, 57.961, 58.042, 58.123,\
                                  58.205, 58.287, 58.368, 58.451, 58.533, 58.616, 58.699, 58.782, 58.907, 58.991,\
                                  59.075, 59.159, 59.243, 59.328, 59.413, 59.498, 59.626, 59.712, 59.798, 59.885,\
                                  59.971, 60.058, 60.145, 60.276, 60.364, 60.452, 60.54, 60.628, 60.761, 60.85,\
                                  60.94, 61.029, 61.164, 61.255, 61.345, 61.481, 61.573, 61.664, 61.802, 61.894,\
                                  61.987, 62.126, 62.219, 62.312, 62.453, 62.547, 62.689, 62.784, 62.926, 63.022,\
                                  ]

    RampData_NRZ_RampRate     = [8, 4, 2, 2.0164, 2.0408, 2.0651, 2.0891, 2.1137, 2.1382, 2.1624,\
                                  2.1865, 2.2103, 2.2349, 2.2583, 2.2825, 2.3056, 2.3295, 2.3532, 2.3767, 2.4,\
                                  2.4232, 2.4462, 2.469, 2.4917, 2.5142, 2.5365, 2.5586, 2.5806, 2.6024, 2.6241,\
                                  2.6456, 2.6669, 2.688, 2.7079, 2.7287, 2.7493, 2.7686, 2.7889, 2.8078, 2.8265,\
                                  2.845, 2.8634, 2.8815, 2.8982, 2.916, 2.931, 2.947, 2.9615, 2.9758, 2.9886,\
                                  3.001, 3.0119, 3.021, 3.0286, 3.033, 3.0328, 3.0279, 3.0097, 2.9306, 2.7427,\
                                  2.7247, 2.7193, 2.7179, 2.722, 2.7259, 2.7325, 2.7404, 2.7497, 2.7587, 2.7692,\
                                  2.7794, 2.7895, 2.801, 2.8124, 2.8252, 2.8363, 2.8489, 2.8614, 2.8738, 2.886,\
                                  2.8998, 2.9119, 2.9255, 2.939, 2.9524, 2.9657, 2.979, 2.9921, 3.0051, 3.0181,\
                                  3.0327, 3.0455, 3.06, 3.0726, 3.0869, 3.1012, 3.1135, 3.1276, 3.1417, 3.1557,\
                                  3.1696, 3.1834, 3.1972, 3.2108, 3.2245, 3.238, 3.2515, 3.2649, 3.2782, 3.2914,\
                                  3.3067, 3.3198, 3.3329, 3.3479, 3.3608, 3.3737, 3.3886, 3.4013, 3.4161, 3.4287,\
                                  3.4434, 3.4558, 3.4704, 3.4827, 3.4972, 3.5093, 3.5237, 3.5358, 3.55, 3.5642,\
                                  3.5761, 3.5902, 3.6042, 3.6159, 3.6298, 3.6437, 3.6552, 3.669, 3.6827, 3.6964,\
                                  3.7076, 3.7212, 3.7347, 3.7482, 3.7616, 3.7725, 3.7859, 3.7991, 3.8124, 3.8255,\
                                  3.8387, 3.8492, 3.8622, 3.8752, 3.8881, 3.901, 3.9138, 3.9266, 3.9394, 3.9494,\
                                  3.962, 3.9746, 3.9871, 3.9996, 4.012, 4.0244, 4.0368, 4.0491, 4.0613, 4.0735,\
                                  4.0829, 4.0949, 4.107, 4.119, 4.1309, 4.1428, 4.1546, 4.1664, 4.1782, 4.1899,\
                                  4.2015, 4.2131, 4.2247, 4.2362, 4.2477, 4.2561, 4.2674, 4.2787, 4.29, 4.3012,\
                                  4.3124, 4.3235, 4.3345, 4.3455, 4.3565, 4.3674, 4.3783, 4.3891, 4.3968, 4.4075,\
                                  4.4181, 4.4287, 4.4393, 4.4498, 4.4603, 4.4707, 4.4779, 4.4882, 4.4985, 4.5087,\
                                  4.5188, 4.529, 4.539, 4.5458, 4.5557, 4.5656, 4.5755, 4.5853, 4.5917, 4.6014,\
                                  4.6111, 4.6207, 4.6269, 4.6364, 4.6458, 4.6518, 4.6612, 4.6705, 4.6762, 4.6854,\
                                  4.6946, 4.7001, 4.7092, 4.7182, 4.7236, 4.7324, 4.7377, 4.7465, 4.7516, 4.7602,\
                                  ]


