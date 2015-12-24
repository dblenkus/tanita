# -*- coding: utf-8 -*-

# Copyright 2015 Domen Blenkuš
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import argparse
from datetime import datetime
import os
import re
from io import BytesIO

import matplotlib
matplotlib.use('Agg')  # requied to work in virtualenv
import matplotlib.pyplot as plt


line_regex = re.compile(  # pylint: disable=invalid-name
    r'DT,"(?P<date>[0-9/]+)",Ti,"(?P<time>[0-9:]+)",Bt,(?P<body_type>[02]),GE,'
    r'(?P<gender>[12]),AG,(?P<age>\d+),Hm,(?P<height>\d+\.\d),AL,'
    r'(?P<activity>[123]),Wk,(?P<weight>\d+\.\d),MI,(?P<bmi>\d+\.\d),FW,'
    r'(?P<fat>\d+\.\d),Fr,(?P<fat_rarm>\d+\.\d),Fl,(?P<fat_larm>\d+\.\d),FR,'
    r'(?P<fat_rleg>\d+\.\d),FL,(?P<fat_lleg>\d+\.\d),FT,'
    r'(?P<fat_trunk>\d+\.\d),mW,(?P<muscle>\d+\.\d),mr,'
    r'(?P<muscle_rarm>\d+\.\d),ml,(?P<muscle_larm>\d+\.\d),mR,'
    r'(?P<muscle_rleg>\d+\.\d),mL,(?P<muscle_lleg>\d+\.\d),mT,'
    r'(?P<muscle_trunk>\d+\.\d),bW,(?P<bones>\d+\.\d),IF,(?P<visceral>\d+),rD,'
    r'(?P<calories>\d+),rA,(?P<meta_age>\d+),ww,(?P<water>\d+\.\d)')


def get_args():
    parser = argparse.ArgumentParser(
        description='Process data from Tanita BC-601 Body Composition '
                    'Monitor.')
    parser.add_argument('path', help="path to the input file")
    parser.add_argument('-o', '--output', default="tanita_report.pdf",
                        help="output file")
    return parser.parse_args()


def parse_line(line):
    vals = line_regex.search(line).groupdict()
    vals['date_time'] = datetime.strptime(
        '{} {}'.format(vals.pop('date'), vals.pop('time')),
        "%d/%m/%Y %H:%M:%S")
    vals['body_type'] = 'standard' if vals['body_type'] == 0 else 'athletic'
    vals['gender'] = 'male' if vals['gender'] == 1 else 'female'

    return vals


def plot_dates_graph(dates, data):
    plt.xticks(rotation=90)
    for entry in data:
        plt.plot_date(dates, entry['values'], 'o-', label=entry['label'])
    plt.legend(loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.05))
    plt.tight_layout()

    graph_png = BytesIO()
    plt.savefig(graph_png, format='png')
    graph_png.seek(0)  # rewind the data

    plt.clf()

    return graph_png


def main():
    args = get_args()

    if not os.path.isfile(args.path):
        raise IOError("File '{}' does not exist.".format(args.path))

    parsed = []
    with open(args.path) as f_input:
        for line in f_input.readlines():
            parsed.append(parse_line(line))

    collected = {}
    for measure in parsed:
        for key, value in measure.items():
            try:
                collected[key].append(value)
            except KeyError:
                collected[key] = [value]

    dates = matplotlib.dates.date2num(collected['date_time'])

    fat_png = plot_dates_graph(dates, [
        {'values': collected['fat'], 'label': 'Total'},
        {'values': collected['fat_larm'], 'label': 'Left arm'},
        {'values': collected['fat_rarm'], 'label': 'Right arm'},
        {'values': collected['fat_lleg'], 'label': 'Left leg'},
        {'values': collected['fat_rleg'], 'label': 'Right leg'},
        {'values': collected['fat_trunk'], 'label': 'Trunk'},
    ])
    open('fat.png', 'w').write(fat_png.read())

    muscle_png = plot_dates_graph(dates, [
        {'values': collected['muscle'], 'label': 'Total'},
        {'values': collected['muscle_larm'], 'label': 'Left arm'},
        {'values': collected['muscle_rarm'], 'label': 'Right arm'},
        {'values': collected['muscle_lleg'], 'label': 'Left leg'},
        {'values': collected['muscle_rleg'], 'label': 'Right leg'},
        {'values': collected['muscle_trunk'], 'label': 'Trunk'},
    ])
    open('muscle.png', 'w').write(muscle_png.read())

if __name__ == '__main__':
    main()
