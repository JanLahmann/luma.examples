# -*- coding: utf-8 -*-
# Copyright (c) 2014-2022 Richard Hull and contributors
# See LICENSE.rst for details.

import sys
import logging

from luma.core import cmdline, error
from luma.led_matrix.device import ws2812

MY_MATRIX_22x20 = [
  0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22,
 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65,
 87, 86, 85, 84, 83, 82, 81, 80, 79, 78, 77, 76, 75, 74, 73, 72, 71, 70, 69, 68, 67, 66,
 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99,100,101,102,103,104,105,106,107,108,109,
131,130,129,128,127,126,125,124,123,122,121,120,119,118,117,116,115,114,113,112,111,110,
132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,
175,174,173,172,171,170,169,168,167,166,165,164,163,162,161,160,159,158,157,156,155,154,
176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,
219,218,217,216,215,214,213,212,211,210,209,208,207,206,205,204,203,202,201,200,199,198,
220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,
263,262,261,260,259,258,257,256,255,254,253,252,251,250,249,248,247,246,245,244,243,242,
264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,
307,306,305,304,303,302,301,300,299,298,297,296,295,294,293,292,291,290,289,288,287,286,
308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,
351,350,349,348,347,346,345,344,343,342,341,340,339,338,337,336,335,334,333,332,331,330,
352,353,354,355,356,357,358,359,360,361,362,363,364,365,366,367,368,369,370,371,372,373,
395,394,393,392,391,390,389,388,387,386,385,384,383,382,381,380,379,378,377,376,375,374,
396,397,398,399,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,
439,438,437,436,435,434,433,432,431,430,429,428,427,426,425,424,423,422,421,420,419,418,
]

# logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)-15s - %(message)s'
)
# ignore PIL debug messages
logging.getLogger('PIL').setLevel(logging.ERROR)


def display_settings(device, args):
    """
    Display a short summary of the settings.

    :rtype: str
    """
    iface = ''
    display_types = cmdline.get_display_types()
    if args.display not in display_types['emulator']:
        iface = f'Interface: {args.interface}\n'

    lib_name = cmdline.get_library_for_display_type(args.display)
    if lib_name is not None:
        lib_version = cmdline.get_library_version(lib_name)
    else:
        lib_name = lib_version = 'unknown'

    import luma.core
    version = f'luma.{lib_name} {lib_version} (luma.core {luma.core.__version__})'

    return f'Version: {version}\nDisplay: {args.display}\n{iface}Dimensions: {device.width} x {device.height}\n{"-" * 60}'


def get_device(actual_args=None):
    """
    Create device from command-line arguments and return it.
    """
    if actual_args is None:
        actual_args = sys.argv[1:]
    parser = cmdline.create_parser(description='luma.examples arguments')
    args = parser.parse_args(actual_args)

    if args.config:
        # load config from file
        config = cmdline.load_config(args.config)
        args = parser.parse_args(config + actual_args)

    # create device
    try:
#        device = cmdline.create_device(args)
        device = ws2812(width=22, height=20, mapping=MY_MATRIX_22x20)
        device.contrast(1)
        print(display_settings(device, args))
        return device

    except error.Error as e:
        parser.error(e)
        return None
