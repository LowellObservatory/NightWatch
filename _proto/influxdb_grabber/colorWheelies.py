# -*- coding: utf-8 -*-
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
#  Created on 12 Dec 2018
#
#  @author: rhamilton

"""
"""

from __future__ import division, print_function, absolute_import

import colorsys

import numpy as np


def default_colorset():
    """
    Taken from the default Grafana color set:
    https://github.com/grafana/grafana/blob/master/public/app/core/utils/colors.ts
    """

    const_colors = ['#7EB26D',  # 0: pale green
                    '#EAB839',  # 1: mustard
                    '#6ED0E0',  # 2: light blue
                    '#EF843C',  # 3: orange
                    '#E24D42',  # 4: red
                    '#1F78C1',  # 5: ocean
                    '#BA43A9',  # 6: purple
                    '#705DA0',  # 7: violet
                    '#508642',  # 8: dark green
                    '#CCA300',  # 9: dark sand
                    '#447EBC',
                    '#C15C17',
                    '#890F02',
                    '#0A437C',
                    '#6D1F62',
                    '#584477',
                    '#B7DBAB',
                    '#F4D598',
                    '#70DBED',
                    '#F9BA8F',
                    '#F29191',
                    '#82B5D8',
                    '#E5A8E2',
                    '#AEA2E0',
                    '#629E51',
                    '#E5AC0E',
                    '#64B0C8',
                    '#E0752D',
                    '#BF1B00',
                    '#0A50A1',
                    '#962D82',
                    '#614D93',
                    '#9AC48A',
                    '#F2C96D',
                    '#65C5DB',
                    '#F9934E',
                    '#EA6460',
                    '#5195CE',
                    '#D683CE',
                    '#806EB7',
                    '#3F6833',
                    '#967302',
                    '#2F575E',
                    '#99440A',
                    '#58140C',
                    '#052B51',
                    '#511749',
                    '#3F2B5B',
                    '#E0F9D7',
                    '#FCEACA',
                    '#CFFAFF',
                    '#F9E2D2',
                    '#FCE2DE',
                    '#BADFF4',
                    '#F9D9F9',
                    '#DEDAF7',
                    ]
    return const_colors


def sortByHue(colorset):
    """
    Given a list of hex/html colors, sort them according to their hue
    so it makes sense in a plot for the largest amount of people
    """

    h = []
    for c in colorset:
        if len(c) == 7 and c[0] == "#":
            r, g, b = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)
            hue, lig, sat = colorsys.rgb_to_hls(r, g, b)
            h.append(hue)

    if len(h) > 0:
        isort = np.argsort(h)
        return np.array(colorset)[isort]
    else:
        return np.array(colorset)


def getColors():
    """
    """
    dset = default_colorset()
    sset = sortByHue(dset)

    return dset, sset
