"""QGF terminal runner for discovered Visual Quar examples and Python tests.

The SDK is an external dependency and is never modified by this runner.
"""
import argparse
import ast
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
EXPECTED = {
    "266": ['true', 'false', 'true'],
    "267": ['false', 'true', 'false', 'true'],
    "268": ['true', 'false', 'false'],
    "269": ['true', 'false', 'false'],
    "270": ['10.0', '0.0'],
    "271": ['true', 'false', 'false'],
    "272": ['true', 'false', 'false'],
    "273": ['true', 'true', 'true', 'true'],
    "274": ['true', 'true', '1.0'],
    "275": ['false', 'true', 'true', '10.0', 'true', 'true'],

    "256": ['0.6', '0.8'],
    "257": ['1.0', '0.0'],
    "258": ['2.0', '0.0'],
    "259": ['1.0', '2.0'],
    "260": ['1.0', '0.0'],
    "261": ['-1.0', '0.0'],
    "262": ['0.0', '-1.0'],
    "263": ['-2.0', '0.0'],
    "264": ['0.0', '0.0'],
    "265": ['0.6', '2.0', '1.0', '-1.0'],

    "246": ['25.0', '0.0', '2.0'],
    "247": ['0.0', '9.0', '-1.0'],
    "248": ['true', 'true', 'false'],
    "249": ['false', 'true', 'false'],
    "250": ['4.0', '0.0', '2.0'],
    "251": ['6.0', '0.0', '4.0'],
    "252": ['0.0', '25.0', '-1.0'],
    "253": ['true', 'false', 'true'],
    "254": ['false', 'false', '-1.0'],
    "255": ['25.0', 'true', 'false', '6.0', '4.0'],

    "236": ['true', 'false', 'true'],
    "237": ['true', 'false', 'false'],
    "238": ['true', 'true', 'false'],
    "239": ['true', 'true', 'false'],
    "240": ['true', 'false', 'false'],
    "241": ['true', 'true', 'false'],
    "242": ['true', 'true', 'false'],
    "243": ['2.0', '3.0', '0.0'],
    "244": ['true', 'false', 'true'],
    "245": ['true', 'true', 'false', '2.0', 'true'],

    "226": ['true', 'false', 'false'],
    "227": ['true', 'false', 'false'],
    "228": ['true', 'false', 'false'],
    "229": ['true', 'false', 'false'],
    "230": ['true', 'false', 'false'],
    "231": ['true', 'false', 'false'],
    "232": ['true', 'false', 'false'],
    "233": ['true', 'false', 'true'],
    "234": ['true', 'false', 'false'],
    "235": ['true', 'true', 'true', 'true', 'false', 'false'],

    "216": ['true', 'false', 'false'],
    "217": ['true', 'false', 'false'],
    "218": ['true', 'false', 'false'],
    "219": ['true', 'false', 'false'],
    "220": ['true', 'false', 'false'],
    "221": ['true', 'false', 'false'],
    "222": ['true', 'false', 'false'],
    "223": ['true', 'false', 'false'],
    "224": ['true', 'false', 'false'],
    "225": ['true', 'true', 'true', 'true', 'true', 'true', 'true', 'false'],

    "206": ['true', 'false', 'false'],
    "207": ['true', 'false', 'false'],
    "208": ['true', 'false', 'false'],
    "209": ['true', 'false', 'false'],
    "210": ['true', 'false', 'false'],
    "211": ['true', 'false', 'false'],
    "212": ['true', 'false', 'false'],
    "213": ['true', 'false', 'false'],
    "214": ['true', 'false', 'true', 'false'],
    "215": ['true', 'true', 'true', 'true', 'true', 'true', 'false'],
    "196": ['true', 'false', 'false'],
    "197": ['true', 'false', 'false'],
    "198": ['true', 'false', 'false'],
    "199": ['true', 'false', 'false'],
    "200": ['true', 'false', 'true', 'false'],
    "201": ['true', 'false', 'false'],
    "202": ['true', 'false', 'false'],
    "203": ['true', 'false', 'true', 'false'],
    "204": ['true', 'false', 'true', 'false'],
    "205": ['true', 'true', 'true', 'true', 'true', '2'],

    "186": ['true', 'false', 'false'],
    "187": ['true', 'false', 'false'],
    "188": ['false', 'true', 'true'],
    "189": ['true', 'false', 'false'],
    "190": ['true', 'false', 'false'],
    "191": ['true', 'false', 'true'],
    "192": ['true', 'false', 'false'],
    "193": ['true', 'false', 'false'],
    "194": ['true', 'false', 'false'],
    "195": ['true', 'false', 'true', 'true', 'true'],

    "176": ['true', 'false', 'false'],
    "177": ['true', 'false', 'false'],
    "178": ['true', 'false', 'false'],
    "179": ['true', 'false', 'false'],
    "180": ['3', 'true', 'false'],
    "181": ['6.0', '13.0'],
    "182": ['4.0', 'false', 'true'],
    "183": ['true', 'false', 'false'],
    "184": ['true', 'false', 'true'],
    "185": ['true', 'true', '13.0', '4.0', 'false'],

    "166": ['true', 'false', 'false'],
    "167": ['true', 'false', 'false'],
    "168": ['13.0', '16.0'],
    "169": ['3.0', '-4.0'],
    "170": ['15.0', '17.0'],
    "171": ['true', 'false', 'false'],
    "172": ['true', 'false'],
    "173": ['true', 'false', 'true', 'false'],
    "174": ['true', 'false', 'true', 'false'],
    "175": ['true', 'true', '13.0', 'false', 'false'],

    "156": ['true', 'false', 'false'],
    "157": ['true', 'false', 'false'],
    "158": ['true', 'false', 'false'],
    "159": ['true', 'false', 'false', 'false'],
    "160": ['true', 'false', 'false'],
    "161": ['true', 'false', 'false'],
    "162": ['true', 'false', 'false'],
    "163": ['true', 'true', 'false', 'false'],
    "164": ['true', 'false', 'true', 'false'],
    "165": ['true', 'true', 'true', 'true', 'true', 'false'],

    "146": ['true', 'false', 'false'],
    "147": ['true', 'false', 'false'],
    "148": ['true', 'false', 'false'],
    "149": ['true', 'false', 'false'],
    "150": ['true', 'false', 'false'],
    "151": ['true', 'false', 'false'],
    "152": ['true', 'false', 'false'],
    "153": ['true', 'false', 'false'],
    "154": ['true', 'false', 'false'],
    "155": ['true', 'false', 'true', 'false', 'false'],

    "136": ['true', 'true', 'false'],
    "137": ['true', 'false', 'false'],
    "138": ['80', '0', '0'],
    "139": ['true', 'false', 'false'],
    "140": ['true', 'false', 'false'],
    "141": ['true', 'false', 'false'],
    "142": ['true', 'false', 'false'],
    "143": ['true', 'false', 'false'],
    "144": ['true', 'false', 'true', 'false'],
    "145": ['true', 'false', 'true', 'false', 'true'],

    "126": ['true', 'false', 'false'],
    "127": ['true', 'false', 'false'],
    "128": ['true', 'false', 'false', 'false'],
    "129": ['true', 'false', 'false'],
    "130": ['false', 'true', 'true'],
    "131": ['true', 'false', 'false'],
    "132": ['true', 'true', 'false'],
    "133": ['true', 'true', 'false', 'false'],
    "134": ['true', 'false', 'false'],
    "135": ['true', 'false', 'false', 'false', 'true'],

    "116": ['true', 'false', 'false'],
    "117": ['true', 'false', 'false'],
    "118": ['true', 'false', 'false'],
    "119": ['true', 'false', 'true', 'false'],
    "120": ['1', '3', '0'],
    "121": ['2', '0', '0'],
    "122": ['true', 'false', 'false'],
    "123": ['true', 'false', 'false'],
    "124": ['true', 'false', 'false'],
    "125": ['true', 'false', 'true', 'false', 'true'],

    "111": ['20.0', '10.0', '0.0'],
    "112": ['15.0', '5.0'],
    "113": ['20.0', '0.0', '0.0'],
    "114": ['true', 'false', 'false'],
    "115": ['0.0', '100.0', 'true', 'true'],
    "106": ['true', 'true', 'false'],
    "107": ['0', '128', '255'],
    "108": ['40.0', '60.0'],
    "109": ['true', 'false'],
    "110": ['true', 'false'],
    "101": ['80.0'],
    "102": ['true', 'false', '32.0'],
    "103": ['true', 'false'],
    "104": ['true', 'false'],
    "105": ['true', 'true', '40.0'],

    "096": ['true', 'false'],
    "097": ['true', 'false'],
    "098": ['0', '127', '255'],
    "099": ['true', 'false'],
    "100": ['40.0', 'true', 'false'],
    "086": ['-4.0', '3.0'],
    "087": ['3.141592653589793', '180.0'],
    "088": ['10.0', '1.0'],
    "089": ['9.0', '3.0'],
    "090": ['21.0'],
    "091": ['10.0', 'false'],
    "092": ['13.0', '3.0'],
    "093": ['true', '0.0'],
    "094": ['40.0', '25.0'],
    "095": ['25.0', '-4.0', '2.0'],

    "081": ['23.0', '0.0'],
    "082": ['25.0', '5.0'],
    "083": ['25.0', '5.0'],
    "084": ['0.6', '0.8'],
    "085": ['false', '0.0', '0.0', '0.0'],

    "080": ['false', 'true', '11.0', '25.0'],
    "079": ['2.5', '15.0'],
    "078": ['6.0', '-2.0'],
    "077": ['7.0', '-3.0'],
    "076": ['7.0', '3.0'],
    "071": ['2', '1', '3', '0'],
    "072": ['true', 'true', '1', '3'],
    "073": ['true', 'true', 'false', '0', '479'],
    "074": ['false', 'true', 'false', '0', '0', 'false'],
    "075": ['2', 'true', '1', '3', 'true', '0', 'false'],
    "070": ['0', '42', '479', '0'],
    "069": ['0', '120', '639', '0'],
    "068": ['false', 'true', 'true', 'false', 'false'],
    "067": ['3', '3', '0', '0'],
    "066": ['2', '2', '1', '0'],
    "065": ['true', '1', 'false', '0'],
    "064": ['2', '3', '0', '0'],
    "063": ['true', 'false', 'false', 'false'],
    "062": ['3', '2', '1', '0'],
    "061": ['2', '1', '3', '0'],
    "060": ['true', 'false', '32767', 'false'],
    "059": ['true', 'false', 'true', 'false'],
    "058": ['true', '1', 'true', '0'],
    "057": ['2', '1', '3', '0'],
    "056": ['0', '1', '2', '3', 'false'],
    "001": ["25.0", "11.0", "-2.0", "25.0"],
    "002": ["7.0", "7.0", "true", "false", "true", "false"],
    "004": ["true", "false", "true", "false", "true", "true", "false", "true"],
    "005": ["0", "1", "3", "2", "0", "0", "0", "5", "15", "0", "true"],
    "006": ["0.0", "0.25", "1.0", "0.0", "0.0", "10.0", "20.0", "30.0", "10.0", "30.0"],
    "007": ["60", "2", "20", "1.0", "1", "5", "0.25", "5", "0"],
    "008": ["2", "4", "1", "0", "0.0", "2.0"],
    "009": ['0', '7', '1', '5', '0', '14', '2', '0', '3'],
    "010": ['2', '55', '2', '15', '0', '15', '4', '0.75'],
    "011": ['1', '10', '2.5', '0', '10', '7.5', '1', '20', '15.0'],
    "012": ['false', 'true', 'false', 'true', '12', '0', '12', '0', '0', '0.0'],
    "013": ['0', '10', '0.0', '2', '0', '10.0', '1', '0', '20.0', '0', '10', '25.0', '30', '4', '3'],
    "014": ['2', '65', '1.0', '2', '25', '1.0', '1', '5', '0.25', '0', '5', '0.25', '5'],
    "015": ['0', '12', '2', '0', '0.0', '0', '0', '10'],
    "016": ['1', '2', '3', 'true', 'false'],
    "017": ['0', '1', 'true', 'false', 'true'],
    "018": ['true', 'true', 'false', 'false'],
    "019": ['0', '1', '2', '3', '3'],
    "020": ['1', '2', '3', '0', '3', '4'],
    "021": ['true', 'true', 'false', 'false', 'true', 'false'],
    "022": ['1', '4', '1', '2', '4'],
    "023": ['3', 'true', '0', '2'],
    "024": ['4', '0', '4', '0', '4', '0', '0'],
    "025": ['true', 'true', 'false', '3', 'false', 'true'],
    "026": ['0', '1', '2', '3', '4', '3'],
    "027": ['true', '0', '0', '1', 'true'],
    "028": ['false', 'false', 'false', 'false', 'false', 'false'],
    "029": ['true', 'false', 'false', 'false', 'false'],
    "030": ['false', '1', 'true', 'true', '0', '3'],
    "031": ['true', 'false', 'true', 'false', '0', '0', '0'],
    "032": ['1', '2', '3', '3', '4', '4', '4'],
    "033": ['3', '4', '0', 'true', 'true'],
    "034": ['true', 'false', 'true', 'false', 'false', 'false', 'false', 'true'],
    "035": ['true', '0', '0', 'true', '4', 'true', '0', 'false'],


    "036": ['true', 'false', 'true', 'false'],
    "037": ['1', '2', '3', '0'],
    "038": ['true', 'true', 'true', 'false'],
    "039": ['false', 'false', 'false', '2'],
    "040": ['true', 'false', 'false', 'false'],
    "041": ['true', 'true', 'false', 'false'],
    "042": ['true', 'false', 'false', 'false'],
    "043": ['true', 'false', '2', '0'],
    "044": ['true', '800', '600', '640'],
    "045": ['true', 'false', '1', '0', '480'],
    "046": ['true', 'false', 'true', 'false'],
    "047": ['true', '2', '1', 'false'],
    "048": ['true', 'false', '1', 'true'],
    "049": ['true', 'false', '0', '2'],
    "050": ['true', 'false', 'false', 'true', 'false'],
    "051": ['2', '2', 'true', '2'],
    "052": ['false', '640', '0', '2'],
    "053": ['true', 'false', 'true', '1', '0'],
    "054": ['2', 'false', '3', '0'],
    "055": ['true', 'true', 'true', 'true', 'false', 'true'],
    "003": [
        "true", "false", "true", "true", "false",
        "0", "1", "1", "1", "2", "3", "3", "true", "false",
        "true", "false", "false", "false", "0", "2",
        "true", "true", "false", "true", "true", "false",
        "true", "false", "true", "true",
    ],
}
EXPECTED_ERRORS = {}  # Example ID -> required diagnostic substring (explicit opt-in).
MODULES = { "266": "core/collision2d.vq", "267": "core/collision2d.vq", "268": "core/collision2d.vq", "269": "core/collision2d.vq", "270": "core/collision2d.vq", "271": "core/collision2d.vq", "272": "core/collision2d.vq", "273": "core/collision2d.vq", "274": "core/collision2d.vq", "275": "core/collision2d.vq",  "256": "core/collision2d.vq", "257": "core/collision2d.vq", "258": "core/collision2d.vq", "259": "core/collision2d.vq", "260": "core/collision2d.vq", "261": "core/collision2d.vq", "262": "core/collision2d.vq", "263": "core/collision2d.vq", "264": "core/collision2d.vq", "265": "core/collision2d.vq",  "246": "core/collision2d.vq", "247": "core/collision2d.vq", "248": "core/collision2d.vq", "249": "core/collision2d.vq", "250": "core/collision2d.vq", "251": "core/collision2d.vq", "252": "core/collision2d.vq", "253": "core/collision2d.vq", "254": "core/collision2d.vq", "255": "core/collision2d.vq",  "236": "core/collision2d.vq", "237": "core/collision2d.vq", "238": "core/collision2d.vq", "239": "core/collision2d.vq", "240": "core/collision2d.vq", "241": "core/collision2d.vq", "242": "core/collision2d.vq", "243": "core/collision2d.vq", "244": "core/collision2d.vq", "245": "core/collision2d.vq",  "226": "core/entity.vq", "227": "core/entity.vq", "228": "core/entity.vq", "229": "core/entity.vq", "230": "core/entity.vq", "231": "core/entity.vq", "232": "core/entity.vq", "233": "core/entity.vq", "234": "core/entity.vq", "235": "core/entity.vq",  "216": "core/entity.vq", "217": "core/entity.vq", "218": "core/entity.vq", "219": "core/entity.vq", "220": "core/entity.vq", "221": "core/entity.vq", "222": "core/entity.vq", "223": "core/entity.vq", "224": "core/entity.vq", "225": "core/entity.vq",  "206": "core/entity.vq", "207": "core/entity.vq", "208": "core/entity.vq", "209": "core/entity.vq", "210": "core/entity.vq", "211": "core/entity.vq", "212": "core/entity.vq", "213": "core/entity.vq", "214": "core/entity.vq", "215": "core/entity.vq", "196": "core/entity.vq", "197": "core/entity.vq", "198": "core/entity.vq", "199": "core/entity.vq", "200": "core/entity.vq", "201": "core/entity.vq", "202": "core/entity.vq", "203": "core/entity.vq", "204": "core/entity.vq", "205": "core/entity.vq",  "186": "core/scene.vq", "187": "core/scene.vq", "188": "core/scene.vq", "189": "core/scene.vq", "190": "core/scene.vq", "191": "core/scene.vq", "192": "core/scene.vq", "193": "core/scene.vq", "194": "core/scene.vq", "195": "core/scene.vq",  "176": "core/scene.vq", "177": "core/scene.vq", "178": "core/scene.vq", "179": "core/scene.vq", "180": "core/scene.vq", "181": "core/scene.vq", "182": "core/scene.vq", "183": "core/scene.vq", "184": "core/scene.vq", "185": "core/scene.vq",  "166": "core/scene.vq", "167": "core/scene.vq", "168": "core/scene.vq", "169": "core/scene.vq", "170": "core/scene.vq", "171": "core/scene.vq", "172": "core/scene.vq", "173": "core/scene.vq", "174": "core/scene.vq", "175": "core/scene.vq",  "156": "core/scene.vq", "157": "core/scene.vq", "158": "core/scene.vq", "159": "core/scene.vq", "160": "core/scene.vq", "161": "core/scene.vq", "162": "core/scene.vq", "163": "core/scene.vq", "164": "core/scene.vq", "165": "core/scene.vq",  "146": "core/resource.vq", "147": "core/resource.vq", "148": "core/resource.vq", "149": "core/resource.vq", "150": "core/resource.vq", "151": "core/resource.vq", "152": "core/resource.vq", "153": "core/resource.vq", "154": "core/resource.vq", "155": "core/resource.vq",  "136": "core/resource.vq", "137": "core/resource.vq", "138": "core/resource.vq", "139": "core/resource.vq", "140": "core/resource.vq", "141": "core/resource.vq", "142": "core/resource.vq", "143": "core/resource.vq", "144": "core/resource.vq", "145": "core/resource.vq",  "126": "core/resource.vq", "127": "core/resource.vq", "128": "core/resource.vq", "129": "core/resource.vq", "130": "core/resource.vq", "131": "core/resource.vq", "132": "core/resource.vq", "133": "core/resource.vq", "134": "core/resource.vq", "135": "core/resource.vq",  "116": "core/resource.vq", "117": "core/resource.vq", "118": "core/resource.vq", "119": "core/resource.vq", "120": "core/resource.vq", "121": "core/resource.vq", "122": "core/resource.vq", "123": "core/resource.vq", "124": "core/resource.vq", "125": "core/resource.vq",  "111": "core/render2d.vq", "112": "core/render2d.vq", "113": "core/render2d.vq", "114": "core/render2d.vq", "115": "core/render2d.vq", "106": "core/render2d.vq", "107": "core/render2d.vq", "108": "core/render2d.vq", "109": "core/render2d.vq", "110": "core/render2d.vq",  "101": "core/render2d.vq", "102": "core/render2d.vq", "103": "core/render2d.vq", "104": "core/render2d.vq", "105": "core/render2d.vq", "096": "core/render2d.vq", "097": "core/render2d.vq", "098": "core/render2d.vq", "099": "core/render2d.vq", "100": "core/render2d.vq",  "086": "core/math/vector2.vq", "087": "core/math/vector2.vq", "088": "core/math/vector2.vq", "089": "core/math/vector2.vq", "090": "core/math/vector2.vq", "091": "core/math/vector2.vq", "092": "core/math/vector2.vq", "093": "core/math/vector2.vq", "094": "core/math/vector2.vq", "095": "core/math/vector2.vq","081": "core/math/vector2.vq", "082": "core/math/vector2.vq", "083": "core/math/vector2.vq", "084": "core/math/vector2.vq", "085": "core/math/vector2.vq", "080": "core/math/vector2.vq", "079": "core/math/vector2.vq", "078": "core/math/vector2.vq", "077": "core/math/vector2.vq", "076": "core/math/vector2.vq", "071": "core/input.vq", "072": "core/input.vq", "073": "core/input.vq", "074": "core/input.vq", "075": "core/input.vq", "070": "core/input.vq", "069": "core/input.vq", "068": "core/input.vq", "067": "core/input.vq", "066": "core/input.vq", "065": "core/input.vq", "064": "core/input.vq", "063": "core/input.vq", "062": "core/input.vq", "061": "core/input.vq", "060": "core/input.vq", "059": "core/input.vq", "058": "core/input.vq", "057": "core/input.vq", "056": "core/input.vq", "055": "core/window.vq", "054": "core/window.vq", "053": "core/window.vq", "052": "core/window.vq", "051": "core/window.vq", "001": "core/math/vector2.vq", "002": "core/math/rect2.vq",
           "003": "core/lifecycle.vq", "004": "core/game_loop.vq",
           "005": "core/game_loop.vq", "006": "core/game_loop.vq",
           "007": "core/game_loop.vq", "008": "core/game_loop.vq",
           "009": "core/game_loop.vq", "010": "core/game_loop.vq",
           "011": "core/game_loop.vq", "012": "core/game_loop.vq",
           "013": "core/game_loop.vq", "014": "core/game_loop.vq",
           "015": "core/game_loop.vq",
           "016": "core/platform.vq",
           "017": "core/platform.vq",
           "018": "core/platform.vq",
           "019": "core/platform.vq",
           "020": "core/platform.vq",
           "021": "core/platform.vq",
           "022": "core/platform.vq",
           "023": "core/platform.vq",
           "024": "core/platform.vq",
           "025": "core/platform.vq",
           "026": "core/platform.vq",
           "027": "core/platform.vq",
           "028": "core/platform.vq",
           "029": "core/platform.vq",
           "030": "core/platform.vq",
           "031": "core/platform.vq",
           "032": "core/platform.vq",
           "033": "core/platform.vq",
           "034": "core/platform.vq",
           "035": "core/platform.vq",
           "036": "core/window.vq",
           "037": "core/window.vq",
           "038": "core/window.vq",
           "039": "core/window.vq",
           "040": "core/window.vq",
           "041": "core/window.vq",
           "042": "core/window.vq",
           "043": "core/window.vq",
           "044": "core/window.vq",
           "045": "core/window.vq",
           "050": "core/window.vq",
           "049": "core/window.vq",
           "048": "core/window.vq",
           "047": "core/window.vq",
           "046": "core/window.vq"
}


def sdk_path(value):
    path = Path(value).expanduser().resolve()
    if not (path / "main.py").is_file():
        raise ValueError("SDK directory must contain main.py")
    if not path.is_dir():
        raise ValueError("SDK path must be a directory")
    return path


def discover_examples():
    """Return canonical example IDs and paths, preferring numbered directories.

    Legacy examples/001_math is retained as a fallback, not a duplicate entry.
    """
    found = {}
    base = ROOT / "examples"
    if not base.is_dir():
        return found
    for source in sorted(base.rglob("main.vq")):
        relative = source.relative_to(base)
        # Numbered case directories: examples/01 core/001 vector2/main.vq
        match = re.match(r"^(\d{3})(?:\D|$)", source.parent.name)
        if not match:
            continue
        case_id = match.group(1)
        # Prefer the canonical categorized layout over legacy examples/001_math.
        is_legacy = len(relative.parts) == 2
        if case_id not in found or (not is_legacy and found[case_id][1]):
            found[case_id] = (source, is_legacy)
    return {key: value[0] for key, value in sorted(found.items())}


def discover_demos():
    """Find standalone graphical demos without including them in example batches."""
    base = ROOT / "demos"
    return {source.parent.name: source for source in sorted(base.glob("*/main.vq"))} if base.is_dir() else {}


def demo_chapter(source):
    """Read the explicit chapter assignment of a demo."""
    import json
    metadata = source.parent / "demo.json"
    try:
        return int(json.loads(metadata.read_text(encoding="utf-8"))["chapter"])
    except (OSError, ValueError, KeyError, TypeError):
        return None


def find_sdl3_library():
    """Resolve an actual SDL3 shared library path; never silently use SDL2."""
    import ctypes.util
    import shutil
    candidate = os.environ.get("QGF_SDL3_LIBRARY")
    if candidate and Path(candidate).is_file():
        return str(Path(candidate).resolve())
    found = ctypes.util.find_library("SDL3")
    names = [found, "libSDL3.so.0", "libSDL3.so", "SDL3.dll", "libSDL3.dylib"]
    folders = [Path("/usr/lib/x86_64-linux-gnu"), Path("/usr/lib/aarch64-linux-gnu"),
               Path("/usr/local/lib"), Path("/usr/lib"), Path("/opt/homebrew/lib")]
    for folder in folders:
        for name in names:
            if name and (folder / name).is_file():
                return str((folder / name).resolve())
    return None


def run_demo(name, sdk, smoke=False):
    """Run a VQ SDL3 demo in its own process; batch mode has a fixed frame count."""
    demos = discover_demos()
    source = demos.get(name)
    if source is None:
        print(f"FAIL: unknown demo {name}")
        return False
    library = find_sdl3_library()
    if library is None:
        print(f"SKIP {name}: SDL3 shared library unavailable (set QGF_SDL3_LIBRARY)")
        return None
    import tempfile
    with tempfile.TemporaryDirectory(prefix="qgf_demo_") as folder:
        temporary = Path(folder) / "main.vq"
        content = source.read_text(encoding="utf-8")
        if smoke:
            marker = "bool batch_mode = false;"
            if content.count(marker) != 1:
                print(f"FAIL {name}: missing canonical batch mode declaration")
                return False
            content = content.replace(marker, "bool batch_mode = true;", 1)
        temporary.write_text(content, encoding="utf-8")
        command = [sys.executable, str(sdk / "main.py"), "--native-library", library,
                   "-f", str(temporary)]
        try:
            result = subprocess.run(command, cwd=sdk, input="1\n", text=True,
                                    capture_output=smoke, timeout=15 if smoke else None,
                                    env={**os.environ, "TERM": "dumb"})
        except subprocess.TimeoutExpired:
            print(f"TIMEOUT {name}")
            return False
        except OSError as error:
            print(f"FAIL {name}: {error}")
            return False
        if smoke:
            if result.stdout:
                print(result.stdout.strip())
            if result.stderr:
                print(result.stderr.strip(), file=sys.stderr)
        success = result.returncode == 0 and (not smoke or "QGF_DEMO_OK" in result.stdout)
        print(f"{'PASS' if success else 'FAIL'} {name} (exit={result.returncode})")
        return success


def run_demo_batch(sdk, chapter=None):
    """Run every selected demo independently; report pass, fail and skip."""
    selected = [(name, source) for name, source in discover_demos().items()
                if chapter is None or demo_chapter(source) == chapter]
    if not selected:
        print("No matching graphical demos")
        return False
    counts = {"PASS": 0, "FAIL": 0, "SKIP": 0}
    for name, _ in selected:
        outcome = run_demo(name, sdk, smoke=True)
        counts["SKIP" if outcome is None else "PASS" if outcome else "FAIL"] += 1
    print("Demo batch: " + " ".join(f"{key}={value}" for key, value in counts.items()))
    return counts["FAIL"] == 0 and counts["SKIP"] == 0


def demo_menu(sdk):
    """Offer both persistent interactive demos and bounded batch checks."""
    while True:
        demos = discover_demos()
        names = list(demos)
        entries = [(0, "Back"), (1, "Run one interactive demo"),
                   (2, "Batch test all graphical demos"),
                   (3, "Batch test demos of a chapter")]
        screen("QGF - 2D DEMOS", entries)
        choice = select(entries)
        if choice is None or choice == "0":
            return
        if choice == "1":
            if not names:
                print("No graphical demos installed")
                continue
            options = [(0, "Back")] + [(i, name) for i, name in enumerate(names, 1)]
            screen("QGF - SINGLE DEMO", options)
            selected = select(options)
            if selected and selected != "0":
                show_result(lambda: run_demo(names[int(selected) - 1], sdk))
        elif choice == "2":
            show_result(lambda: run_demo_batch(sdk))
        elif choice == "3":
            chapter_text = input("Chapter number: ").strip()
            if chapter_text.isdigit():
                show_result(lambda: run_demo_batch(sdk, chapter=int(chapter_text)))


def discover_tests():
    """Only expose infrastructure tests that actually exist."""
    return sorted((ROOT / "tests").glob("test_*.py")) if (ROOT / "tests").is_dir() else []


def module_for(case_id):
    """Find a known library dependency without guessing other dependencies."""
    relative = MODULES.get(case_id)
    return ROOT / relative if relative else None


def availability(case_id, source):
    """Return a reason when an example cannot safely be assembled."""
    module = module_for(case_id)
    if module is None:
        return "no module mapping defined"
    if not module.is_file():
        return f"missing module: {module.relative_to(ROOT)}"
    if not source.is_file():
        return "missing example source"
    return None


def qrvm_source(text):
    """Omit comment-only lines when assembling QRVM input; preserve code."""
    return "\n".join(
        "" if line.lstrip().startswith("//") else line
        for line in text.split("\n")
    )


def classify_execution(result):
    """Classify QRVM termination without confusing expected failures with crashes."""
    combined = (result.stdout + "\n" + result.stderr).lower()
    if result.returncode < 0 or result.returncode in (134, 139, 3221225477):
        return "CRASH"
    if "traceback (most recent call last)" in combined or "segmentation fault" in combined:
        return "CRASH"
    if result.returncode != 0 or "=== QRVM OUTPUT ===" not in result.stdout or "Program executed successfully" not in result.stdout:
        return "FAIL"
    return "PASS"


def run_example_status(case_id, sdk, examples=None):
    """Execute one example and return PASS, EXPECTED ERROR, FAIL, CRASH or SKIP."""
    examples = discover_examples() if examples is None else examples
    source = examples.get(case_id)
    if source is None:
        print(f"FAIL: unknown example {case_id}")
        return "FAIL"
    print(f"\n[{case_id}] {source.relative_to(ROOT) if source.is_relative_to(ROOT) else source}", flush=True)
    reason = availability(case_id, source)
    if reason:
        print(f"SKIP: {reason}")
        return "SKIP"
    module = module_for(case_id)
    try:
        with tempfile.TemporaryDirectory(prefix="qgf_example_") as directory:
            assembled = Path(directory) / "qgf_demo.vq"
            assembled.write_text(qrvm_source(module.read_text(encoding="utf-8")) + "\n" +
                                 qrvm_source(source.read_text(encoding="utf-8")), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(sdk / "main.py"), "-f", str(assembled)],
                cwd=sdk, input="1\n", text=True, capture_output=True,
                timeout=30, env={**os.environ, "TERM": "dumb"})
    except subprocess.TimeoutExpired as error:
        print(f"CRASH: execution timed out ({error.timeout}s)")
        return "CRASH"
    except (OSError, UnicodeError) as error:
        print(f"FAIL: {error}")
        return "FAIL"
    status = classify_execution(result)
    # Expected errors require an explicit baseline; never infer them from failure.
    if status != "PASS":
        print(result.stdout, end="")
        print(result.stderr, end="", file=sys.stderr)
        if status == "FAIL" and case_id in EXPECTED_ERRORS:
            output = result.stdout + "\n" + result.stderr
            if EXPECTED_ERRORS[case_id] in output:
                status = "EXPECTED ERROR"
        print(status)
        return status
    output = result.stdout.split("=== QRVM OUTPUT ===", 1)[1].split(
        "Program executed successfully", 1)[0]
    values = [line.strip().lower() for line in output.splitlines() if line.strip()]
    print("Output:", ", ".join(values))
    expected = EXPECTED.get(case_id)
    if expected is None:
        print("PASS (no output baseline)")
        return "PASS"
    status = "PASS" if values == expected else "FAIL"
    print(status if status == "PASS" else f"FAIL: expected {expected}")
    return status


def run_example(case_id, sdk, examples=None):
    """Compatibility wrapper for callers expecting a boolean."""
    return run_example_status(case_id, sdk, examples) in ("PASS", "EXPECTED ERROR")


def run_selected(sdk, selected, examples=None):
    """Execute a selected subset and print complete status totals."""
    examples = discover_examples() if examples is None else examples
    totals = {status: 0 for status in ("PASS", "EXPECTED ERROR", "FAIL", "CRASH", "SKIP")}
    for key in selected:
        status = run_example_status(key, sdk, examples)
        totals[status] += 1
    print("\nExamples: " + " ".join(f"{key}={value}" for key, value in totals.items()) +
          f" TOTAL={len(selected)}")
    return bool(selected) and totals["FAIL"] == totals["CRASH"] == totals["SKIP"] == 0


def run_all(sdk):
    examples = discover_examples()
    return run_selected(sdk, list(examples), examples)


def select_range(examples, start, end):
    """Select inclusive numeric IDs; report an empty selection as an error."""
    if not start.isdigit() or not end.isdigit() or int(start) > int(end):
        raise ValueError("Range must be two ascending numeric example IDs")
    selected = [key for key in examples if int(start) <= int(key) <= int(end)]
    if not selected:
        raise ValueError(f"No examples found in range {start}-{end}")
    return selected


def discover_chapters(examples):
    """Group examples by their immediate chapter directory."""
    chapters = {}
    for key, source in examples.items():
        relative = source.relative_to(ROOT / "examples")
        if len(relative.parts) < 3:
            continue
        chapter = relative.parts[0]
        match = re.match(r"^(\d+)\b", chapter)
        if match:
            chapters.setdefault(int(match.group(1)), []).append(key)
    return chapters


def select_chapter(examples, chapter):
    chapters = discover_chapters(examples)
    if chapter not in chapters:
        raise ValueError(f"Chapter {chapter} has no examples")
    return chapters[chapter]


def test_kind(source):
    """Identify standard unittest modules; other scripts use the QGF SDK CLI."""
    try:
        tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
    except (OSError, UnicodeError, SyntaxError):
        return "sdk"
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "unittest":
            return "unittest"
        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                if (isinstance(base, ast.Attribute) and base.attr == "TestCase"
                        or isinstance(base, ast.Name) and base.id == "TestCase"):
                    return "unittest"
    return "sdk"


def run_external_files(sdk, filenames):
    """Execute each test independently, continuing after failures and timeouts."""
    passed = failed = skipped = 0
    for source in filenames:
        if not source.is_file():
            print(f"SKIP [{source.name}]: missing test file")
            skipped += 1
            continue
        kind = test_kind(source)
        print(f"\n[Test: {kind}] {source.name}", flush=True)
        if kind == "unittest":
            command = [sys.executable, str(source), "-v"]
        else:
            command = [sys.executable, str(source), "--sdk", str(sdk)]
        try:
            proc = subprocess.run(command, cwd=ROOT, text=True,
                                  capture_output=True, timeout=45)
            print(proc.stdout, end="")
            if proc.stderr:
                print(proc.stderr, end="", file=sys.stderr)
            success = proc.returncode == 0
        except (subprocess.TimeoutExpired, OSError) as error:
            print(f"FAIL: {error}")
            success = False
        if success:
            passed += 1
        else:
            failed += 1
        print("PASS" if success else "FAIL")
    print(f"\nTests: PASS={passed} FAIL={failed} SKIP={skipped} TOTAL={len(filenames)}")
    return failed == 0 and skipped == 0 and passed > 0


def run_external(sdk):
    return run_external_files(sdk, discover_tests())


def clear_screen():
    """Clear interactive terminals without running an external shell command."""
    if sys.stdout.isatty():
        print("\033[2J\033[H", end="", flush=True)


def screen(title, entries):
    clear_screen()
    print("=" * 46)
    print(f"  {title}")
    print("=" * 46)
    for number, label in entries:
        print(f"[{number}] {label}")
    print()


def select(entries):
    valid = {str(number) for number, _ in entries}
    while True:
        try:
            choice = input("Select: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return None
        if choice in valid:
            return choice
        print("Invalid selection. Please try again.")


def show_result(action):
    clear_screen()
    try:
        action()
    except (OSError, UnicodeError, ValueError) as error:
        print(f"FAIL: {error}")
    try:
        input("\nPress Enter to return...")
    except (EOFError, KeyboardInterrupt):
        pass


def example_menu(sdk):
    while True:
        examples = discover_examples()
        ids = list(examples)
        entries = [(0, "Back")]
        for index, key in enumerate(ids, 1):
            reason = availability(key, examples[key])
            suffix = f" [UNAVAILABLE: {reason}]" if reason else ""
            entries.append((index, f"{key} - {examples[key].parent.name}{suffix}"))
        screen("QGF - EXAMPLES", entries)
        choice = select(entries)
        if choice is None or choice == "0":
            return
        key = ids[int(choice) - 1]
        show_result(lambda: run_example(key, sdk, examples))


def range_menu(sdk):
    examples = discover_examples()
    try:
        start = input("First example ID: ").strip()
        end = input("Last example ID: ").strip()
        selected = select_range(examples, start, end)
    except (EOFError, KeyboardInterrupt, ValueError) as error:
        print(f"Invalid range: {error}")
        return
    show_result(lambda: run_selected(sdk, selected, examples))


def chapter_menu(sdk):
    examples = discover_examples()
    chapters = discover_chapters(examples)
    entries = [(0, "Back")]
    entries.extend((number, f"Chapter {number:02d} ({len(ids)} examples)")
                   for number, ids in sorted(chapters.items()))
    screen("QGF - CHAPTERS", entries)
    choice = select(entries)
    if choice is None or choice == "0":
        return
    show_result(lambda: run_selected(sdk, chapters[int(choice)], examples))


def test_menu(sdk):
    while True:
        tests = discover_tests()
        entries = [(0, "Back"), (1, "Run all infrastructure tests")]
        entries.extend((index, source.name) for index, source in enumerate(tests, 2))
        screen("QGF - TESTS", entries)
        choice = select(entries)
        if choice is None or choice == "0":
            return
        if choice == "1":
            show_result(lambda: run_external(sdk))
        else:
            show_result(lambda: run_external_files(sdk, [tests[int(choice) - 2]]))


def list_examples():
    examples = discover_examples()
    if not examples:
        print("No examples found")
    for key, source in examples.items():
        reason = availability(key, source)
        print(f"[{key}] {source.relative_to(ROOT)}" +
              (f" — UNAVAILABLE: {reason}" if reason else ""))


def interactive(sdk):
    entries = [(0, "Exit"), (1, "Run one example"),
               (2, "Run all available examples"),
               (3, "External infrastructure tests"),
               (4, "List examples"), (5, "SDK information"),
               (6, "Run example range"), (7, "Run chapter"),
               (8, "2D graphical demos")]
    while True:
        screen("QUAR GAME FRAMEWORK / 0.0.1", entries)
        choice = select(entries)
        if choice is None or choice == "0":
            clear_screen()
            return 0
        if choice == "1":
            example_menu(sdk)
        elif choice == "2":
            show_result(lambda: run_all(sdk))
        elif choice == "3":
            test_menu(sdk)
        elif choice == "4":
            show_result(list_examples)
        elif choice == "6":
            range_menu(sdk)
        elif choice == "7":
            chapter_menu(sdk)
        elif choice == "8":
            demo_menu(sdk)
        elif choice == "5":
            show_result(lambda: print(f"SDK: {sdk}\nQRVM entry point: {sdk / 'main.py'}"))


def main():
    parser = argparse.ArgumentParser(description="QGF test and example menu")
    parser.add_argument("--sdk", default=os.environ.get("QUAR_SDK", "sdk"))
    parser.add_argument("--external", action="store_true")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--example", help="Example ID (e.g. 001)")
    parser.add_argument("--range", nargs=2, metavar=("FIRST", "LAST"), help="Inclusive example ID range")
    parser.add_argument("--chapter", type=int, help="Run all examples in a chapter")
    parser.add_argument("--list", action="store_true", help="List examples without launching SDK")
    parser.add_argument("--demo", help="Run a named 2D demo interactively")
    parser.add_argument("--demo-smoke", help="Run a named 2D demo with a bounded smoke test")
    parser.add_argument("--list-demos", action="store_true", help="List installed 2D demos")
    parser.add_argument("--demo-all", action="store_true", help="Batch test all graphical demos")
    parser.add_argument("--demo-chapter", type=int, help="Batch test graphical demos of a chapter")
    parser.add_argument("--check", action="store_true", help="Check example dependencies without executing")
    args = parser.parse_args()
    if args.list_demos:
        demos = discover_demos()
        print("\n".join(demos) if demos else "No graphical demos installed")
        return 0
    if args.list:
        list_examples()
        return 0
    if args.check:
        examples = discover_examples()
        if not examples:
            print("FAIL: no examples found")
            return 1
        for key, source in examples.items():
            reason = availability(key, source)
            print(f"[{key}] {'UNAVAILABLE: ' + reason if reason else 'READY'}")
        return 0 if all(availability(key, source) is None for key, source in examples.items()) else 1
    try:
        sdk = sdk_path(args.sdk)
    except ValueError as error:
        parser.error(str(error))
    if args.demo_all or args.demo_chapter is not None:
        return 0 if run_demo_batch(sdk, chapter=args.demo_chapter) else 1
    if args.demo or args.demo_smoke:
        return 0 if run_demo(args.demo or args.demo_smoke, sdk, smoke=bool(args.demo_smoke)) else 1
    if args.external:
        return 0 if run_external(sdk) else 1
    if args.all:
        return 0 if run_all(sdk) else 1
    if args.range or args.chapter is not None:
        examples = discover_examples()
        try:
            selected = (select_range(examples, *args.range) if args.range else
                        select_chapter(examples, args.chapter))
        except ValueError as error:
            parser.error(str(error))
        return 0 if run_selected(sdk, selected, examples) else 1
    if args.example:
        return 0 if run_example(args.example, sdk) else 1
    return interactive(sdk)


if __name__ == "__main__":
    raise SystemExit(main())
