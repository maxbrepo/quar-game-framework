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
    "540": ['true', 'false'],
    "541": ['true', 'false'],
    "542": ['true', 'false'],
    "543": ['true', 'false'],
    "544": ['1', '3'],
    "545": ['true', 'false'],
    "546": ['true', 'false'],
    "547": ['true', 'false'],
    "548": ['true', 'false'],
    "549": ['true', 'false', '0'],

    "530": ['true', 'true', 'false'],
    "531": ['false', 'true', 'true'],
    "532": ['true', 'false', 'false'],
    "533": ['true', 'false'],
    "534": ['true', 'false', 'false'],
    "535": ['true', 'false'],
    "536": ['true', 'false', 'false'],
    "537": ['true', 'false'],
    "538": ['2'],
    "539": ['true', 'false', 'false'],
    "520": ['true', 'true'],
    "521": ['false', 'false'],
    "522": ['true', 'true'],
    "523": ['true', 'true'],
    "524": ['true', 'false'],
    "525": ['true', 'false'],
    "526": ['true', 'false'],
    "527": ['true', 'false'],
    "528": ['2', '1'],
    "529": ['true', 'false', 'true'],
    "510": ['true'],
    "511": ['false'],
    "512": ['true'],
    "513": ['false'],
    "514": ['true'],
    "515": ['false'],
    "516": ['true'],
    "517": ['1'],
    "518": ['true'],
    "519": ['true', 'true', 'true'],

    "500": ['true'],
    "501": ['false'],
    "502": ['false'],
    "503": ['false'],
    "504": ['true'],
    "505": ['false'],
    "506": ['false'],
    "507": ['2', 'true'],
    "508": ['0.02', '50.0'],
    "509": ['true', 'true', 'true'],

    "490": ['3.0'],
    "491": ['0.0'],
    "492": ['6.5'],
    "493": ['4'],
    "494": ['4.0'],
    "495": ['2.0'],
    "496": ['8.0'],
    "497": ['50.0'],
    "498": ['true'],
    "499": ['2.0', 'true', '0.0'],

    "480": ['true'],
    "481": ['false'],
    "482": ['true'],
    "483": ['false'],
    "484": ['true'],
    "485": ['false'],
    "486": ['true', 'false'],
    "487": ['5', '4'],
    "488": ['2', '2'],
    "489": ['true', 'false', '3'],

    "470": ['true'],
    "471": ['false'],
    "472": ['true'],
    "473": ['false'],
    "474": ['7'],
    "475": ['5'],
    "476": ['true'],
    "477": ['2.5'],
    "478": ['2.5'],
    "479": ['1.0', 'true', '3'],

    "460": ['70.0'],
    "461": ['80.0'],
    "462": ['80.0'],
    "463": ['50.0'],
    "464": ['75.0'],
    "465": ['500.0'],
    "466": ['20.0'],
    "467": ['true'],
    "468": ['90.0'],
    "469": ['80.0', '20.0', '30.0'],
    "450": ['3.0'],
    "451": ['2.0'],
    "452": ['3.0'],
    "453": ['2.0'],
    "454": ['1.5'],
    "455": ['400.0'],
    "456": ['50.0'],
    "457": ['true', 'false'],
    "458": ['true', 'false'],
    "459": ['500.0', '90.0'],
    "440": ['20.0'],
    "441": ['8.0'],
    "442": ['10.0'],
    "443": ['25.0'],
    "444": ['20.0', '5.0'],
    "445": ['5.0'],
    "446": ['100.0', '6.0'],
    "447": ['20.0', '80.0'],
    "448": ['30.0'],
    "449": ['30.0', '70.0', '50.0'],

    "430": ['true'],
    "431": ['false'],
    "432": ['true'],
    "433": ['400.0'],
    "434": ['420.0'],
    "435": ['320.0'],
    "436": ['20.0'],
    "437": ['35.0'],
    "438": ['100.0'],
    "439": ['0.0', '100.0'],

    "420": ['true', '25.0'],
    "421": ['0.0', 'false'],
    "422": ['0', '2'],
    "423": ['true', 'false'],
    "424": ['true', 'false'],
    "425": ['20.0', '0.0'],
    "426": ['20.0', '10.0'],
    "427": ['60.0', '10.0'],
    "428": ['false', '0'],
    "429": ['true', '2', '40.0'],

    "410": ['true', 'false'],
    "411": ['true', 'false'],
    "412": ['true', 'false'],
    "413": ['true'],
    "414": ['false'],
    "415": ['true', 'false'],
    "416": ['0', '2'],
    "417": ['0.25', '1.0'],
    "418": ['20.0'],
    "419": ['true', '1', 'false'],

    "400": ['true', 'false'],
    "401": ['true', 'false'],
    "402": ['true', 'false'],
    "403": ['2', '0'],
    "404": ['2', '1'],
    "405": ['true', 'false'],
    "406": ['0.25', '0.0'],
    "407": ['50.0'],
    "408": ['85.0'],
    "409": ['0', 'true'],
    "390": ['true'],
    "391": ['false'],
    "392": ['true', 'false'],
    "393": ['true'],
    "394": ['false'],
    "395": ['true'],
    "396": ['true'],
    "397": ['50.0', '50.0'],
    "398": ['50.0', '200.0'],
    "399": ['true', 'false'],

    "380": ['0.125'],
    "381": ['0.0'],
    "382": ['0.0'],
    "383": ['0.0'],
    "384": ['0.25'],
    "385": ['0.0'],
    "386": ['true', 'false'],
    "387": ['true'],
    "388": ['false'],
    "389": ['0.125', '0.25', 'false'],

    "370": ['true', 'false'],
    "371": ['true', 'false'],
    "372": ['2', '-1'],
    "373": ['true'],
    "374": ['false'],
    "375": ['true'],
    "376": ['true', 'false'],
    "377": ['true', 'false'],
    "378": ['false'],
    "379": ['0', '100', 'false'],
    "360": ['true'],
    "361": ['false'],
    "362": ['true'],
    "363": ['false'],
    "364": ['true'],
    "365": ['true'],
    "366": ['true'],
    "367": ['true'],
    "368": ['0.125'],
    "369": ['true', 'false', '0.25'],

    "350": ['true'],
    "351": ['false'],
    "352": ['1.0'],
    "353": ['0.25'],
    "354": ['true'],
    "355": ['false'],
    "356": ['false'],
    "357": ['true'],
    "358": ['true'],
    "359": ['-1.0'],

    "340": ['6'],
    "341": ['5'],
    "342": ['11'],
    "343": ['5'],
    "344": ['0.25'],
    "345": ['0.5'],
    "346": ['0.0'],
    "347": ['true'],
    "348": ['false', 'false'],
    "349": ['7', '48', '16'],
    "330": ['true'],
    "331": ['false'],
    "332": ['0'],
    "333": ['4'],
    "334": ['8'],
    "335": ['0.0'],
    "336": ['1.25'],
    "337": ['true', 'false'],
    "338": ['2', '1'],
    "339": ['32', '16'],

    "320": ['0'],
    "321": ['3'],
    "322": ['1'],
    "323": ['3'],
    "324": ['true', 'false'],
    "325": ['0.25'],
    "326": ['0.25'],
    "327": ['1.0'],
    "328": ['16', '32'],
    "329": ['0', '2', '0.1'],
    "310": ["true"],
    "311": ["false"],
    "312": ["2"],
    "313": ["0"],
    "314": ["3"],
    "315": ["3"],
    "316": ["2.0"],
    "317": ["1.0"],
    "318": ["1.5"],
    "319": ["32"],

    "302": ['6.0'],
    "303": ['6.0'],
    "304": ['4.0'],
    "305": ['8.0'],
    "306": ['0.0'],
    "307": ['-2.0'],
    "308": ['1.0', '1.0'],
    "309": ['2.0', '1.0', '5.0'],

    "294": ['8.0'],
    "295": ['5.0'],
    "296": ['10.0'],
    "297": ['7.5'],
    "298": ['8.0'],
    "299": ['true', 'false'],
    "300": ['0.0', '-2.5'],
    "301": ['7.5', '8.0', '-3.0'],

    "286": ['true', 'false'],
    "287": ['true', 'false'],
    "288": ['6.0'],
    "289": ['0.0', '1.0'],
    "290": ['-5.0', '10.0'],
    "291": ['-1.0'],
    "292": ['-1.0'],
    "293": ['true', '2.0', '-8.0', '0.0'],
    "276": ['true', 'false'],
    "277": ['true', 'false'],
    "278": ['8.0'],
    "279": ['4.0'],
    "280": ['11.0'],
    "281": ['4.0', '0.0'],
    "282": ['24.0'],
    "283": ['29.0'],
    "284": ['5.0', '-5.0'],
    "285": ['20.0', '6.0'],

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
MODULES = { "540": "core/packaging.vq", "541": "core/packaging.vq", "542": "core/packaging.vq", "543": "core/packaging.vq", "544": "core/packaging.vq", "545": "core/packaging.vq", "546": "core/packaging.vq", "547": "core/packaging.vq", "548": "core/packaging.vq", "549": "core/packaging.vq",  "530": "core/packaging.vq", "531": "core/packaging.vq", "532": "core/packaging.vq", "533": "core/packaging.vq", "534": "core/packaging.vq", "535": "core/packaging.vq", "536": "core/packaging.vq", "537": "core/packaging.vq", "538": "core/packaging.vq", "539": "core/packaging.vq", "520": "core/packaging.vq", "521": "core/packaging.vq", "522": "core/packaging.vq", "523": "core/packaging.vq", "524": "core/packaging.vq", "525": "core/packaging.vq", "526": "core/packaging.vq", "527": "core/packaging.vq", "528": "core/packaging.vq", "529": "core/packaging.vq", "510": "core/packaging.vq", "511": "core/packaging.vq", "512": "core/packaging.vq", "513": "core/packaging.vq", "514": "core/packaging.vq", "515": "core/packaging.vq", "516": "core/packaging.vq", "517": "core/packaging.vq", "518": "core/packaging.vq", "519": "core/packaging.vq",  "500": "core/debug.vq", "501": "core/debug.vq", "502": "core/debug.vq", "503": "core/debug.vq", "504": "core/debug.vq", "505": "core/debug.vq", "506": "core/debug.vq", "507": "core/debug.vq", "508": "core/debug.vq", "509": "core/debug.vq",  "490": "core/debug.vq", "491": "core/debug.vq", "492": "core/debug.vq", "493": "core/debug.vq", "494": "core/debug.vq", "495": "core/debug.vq", "496": "core/debug.vq", "497": "core/debug.vq", "498": "core/debug.vq", "499": "core/debug.vq",  "480": "core/debug.vq", "481": "core/debug.vq", "482": "core/debug.vq", "483": "core/debug.vq", "484": "core/debug.vq", "485": "core/debug.vq", "486": "core/debug.vq", "487": "core/debug.vq", "488": "core/debug.vq", "489": "core/debug.vq",  "470": "core/debug.vq", "471": "core/debug.vq", "472": "core/debug.vq", "473": "core/debug.vq", "474": "core/debug.vq", "475": "core/debug.vq", "476": "core/debug.vq", "477": "core/debug.vq", "478": "core/debug.vq", "479": "core/debug.vq",  "460": "core/camera2d.vq", "461": "core/camera2d.vq", "462": "core/camera2d.vq", "463": "core/camera2d.vq", "464": "core/camera2d.vq", "465": "core/camera2d.vq", "466": "core/camera2d.vq", "467": "core/camera2d.vq", "468": "core/camera2d.vq", "469": "core/camera2d.vq",  "450": "core/camera2d.vq", "451": "core/camera2d.vq", "452": "core/camera2d.vq", "453": "core/camera2d.vq", "454": "core/camera2d.vq", "455": "core/camera2d.vq", "456": "core/camera2d.vq", "457": "core/camera2d.vq", "458": "core/camera2d.vq", "459": "core/camera2d.vq",  "440": "core/camera2d.vq", "441": "core/camera2d.vq", "442": "core/camera2d.vq", "443": "core/camera2d.vq", "444": "core/camera2d.vq", "445": "core/camera2d.vq", "446": "core/camera2d.vq", "447": "core/camera2d.vq", "448": "core/camera2d.vq", "449": "core/camera2d.vq",  "430": "core/camera2d.vq", "431": "core/camera2d.vq", "432": "core/camera2d.vq", "433": "core/camera2d.vq", "434": "core/camera2d.vq", "435": "core/camera2d.vq", "436": "core/camera2d.vq", "437": "core/camera2d.vq", "438": "core/camera2d.vq", "439": "core/camera2d.vq",  "420": "core/ui.vq", "421": "core/ui.vq", "422": "core/ui.vq", "423": "core/ui.vq", "424": "core/ui.vq", "425": "core/ui.vq", "426": "core/ui.vq", "427": "core/ui.vq", "428": "core/ui.vq", "429": "core/ui.vq",  "410": "core/ui.vq", "411": "core/ui.vq", "412": "core/ui.vq", "413": "core/ui.vq", "414": "core/ui.vq", "415": "core/ui.vq", "416": "core/ui.vq", "417": "core/ui.vq", "418": "core/ui.vq", "419": "core/ui.vq",  "400": "core/ui.vq", "401": "core/ui.vq", "402": "core/ui.vq", "403": "core/ui.vq", "404": "core/ui.vq", "405": "core/ui.vq", "406": "core/ui.vq", "407": "core/ui.vq", "408": "core/ui.vq", "409": "core/ui.vq", "390": "core/ui.vq", "391": "core/ui.vq", "392": "core/ui.vq", "393": "core/ui.vq", "394": "core/ui.vq", "395": "core/ui.vq", "396": "core/ui.vq", "397": "core/ui.vq", "398": "core/ui.vq", "399": "core/ui.vq",  "380": "core/audio.vq", "381": "core/audio.vq", "382": "core/audio.vq", "383": "core/audio.vq", "384": "core/audio.vq", "385": "core/audio.vq", "386": "core/audio.vq", "387": "core/audio.vq", "388": "core/audio.vq", "389": "core/audio.vq",  "370": "core/audio.vq", "371": "core/audio.vq", "372": "core/audio.vq", "373": "core/audio.vq", "374": "core/audio.vq", "375": "core/audio.vq", "376": "core/audio.vq", "377": "core/audio.vq", "378": "core/audio.vq", "379": "core/audio.vq",  "360": "core/audio.vq", "361": "core/audio.vq", "362": "core/audio.vq", "363": "core/audio.vq", "364": "core/audio.vq", "365": "core/audio.vq", "366": "core/audio.vq", "367": "core/audio.vq", "368": "core/audio.vq", "369": "core/audio.vq",  "350": "core/audio.vq", "351": "core/audio.vq", "352": "core/audio.vq", "353": "core/audio.vq", "354": "core/audio.vq", "355": "core/audio.vq", "356": "core/audio.vq", "357": "core/audio.vq", "358": "core/audio.vq", "359": "core/audio.vq",  "340": "core/animation2d.vq", "341": "core/animation2d.vq", "342": "core/animation2d.vq", "343": "core/animation2d.vq", "344": "core/animation2d.vq", "345": "core/animation2d.vq", "346": "core/animation2d.vq", "347": "core/animation2d.vq", "348": "core/animation2d.vq", "349": "core/animation2d.vq", "330": "core/animation2d.vq", "331": "core/animation2d.vq", "332": "core/animation2d.vq", "333": "core/animation2d.vq", "334": "core/animation2d.vq", "335": "core/animation2d.vq", "336": "core/animation2d.vq", "337": "core/animation2d.vq", "338": "core/animation2d.vq", "339": "core/animation2d.vq",  "320": "core/animation2d.vq", "321": "core/animation2d.vq", "322": "core/animation2d.vq", "323": "core/animation2d.vq", "324": "core/animation2d.vq", "325": "core/animation2d.vq", "326": "core/animation2d.vq", "327": "core/animation2d.vq", "328": "core/animation2d.vq", "329": "core/animation2d.vq", "310": "core/animation2d.vq", "311": "core/animation2d.vq", "312": "core/animation2d.vq", "313": "core/animation2d.vq", "314": "core/animation2d.vq", "315": "core/animation2d.vq", "316": "core/animation2d.vq", "317": "core/animation2d.vq", "318": "core/animation2d.vq", "319": "core/animation2d.vq",  "302": "core/physics2d.vq", "303": "core/physics2d.vq", "304": "core/physics2d.vq", "305": "core/physics2d.vq", "306": "core/physics2d.vq", "307": "core/physics2d.vq", "308": "core/physics2d.vq", "309": "core/physics2d.vq",  "294": "core/physics2d.vq", "295": "core/physics2d.vq", "296": "core/physics2d.vq", "297": "core/physics2d.vq", "298": "core/physics2d.vq", "299": "core/physics2d.vq", "300": "core/physics2d.vq", "301": "core/physics2d.vq",  "286": "core/physics2d.vq", "287": "core/physics2d.vq", "288": "core/physics2d.vq", "289": "core/physics2d.vq", "290": "core/physics2d.vq", "291": "core/physics2d.vq", "292": "core/physics2d.vq", "293": "core/physics2d.vq", "276": "core/physics2d.vq", "277": "core/physics2d.vq", "278": "core/physics2d.vq", "279": "core/physics2d.vq", "280": "core/physics2d.vq", "281": "core/physics2d.vq", "282": "core/physics2d.vq", "283": "core/physics2d.vq", "284": "core/physics2d.vq", "285": "core/physics2d.vq",  "266": "core/collision2d.vq", "267": "core/collision2d.vq", "268": "core/collision2d.vq", "269": "core/collision2d.vq", "270": "core/collision2d.vq", "271": "core/collision2d.vq", "272": "core/collision2d.vq", "273": "core/collision2d.vq", "274": "core/collision2d.vq", "275": "core/collision2d.vq",  "256": "core/collision2d.vq", "257": "core/collision2d.vq", "258": "core/collision2d.vq", "259": "core/collision2d.vq", "260": "core/collision2d.vq", "261": "core/collision2d.vq", "262": "core/collision2d.vq", "263": "core/collision2d.vq", "264": "core/collision2d.vq", "265": "core/collision2d.vq",  "246": "core/collision2d.vq", "247": "core/collision2d.vq", "248": "core/collision2d.vq", "249": "core/collision2d.vq", "250": "core/collision2d.vq", "251": "core/collision2d.vq", "252": "core/collision2d.vq", "253": "core/collision2d.vq", "254": "core/collision2d.vq", "255": "core/collision2d.vq",  "236": "core/collision2d.vq", "237": "core/collision2d.vq", "238": "core/collision2d.vq", "239": "core/collision2d.vq", "240": "core/collision2d.vq", "241": "core/collision2d.vq", "242": "core/collision2d.vq", "243": "core/collision2d.vq", "244": "core/collision2d.vq", "245": "core/collision2d.vq",  "226": "core/entity.vq", "227": "core/entity.vq", "228": "core/entity.vq", "229": "core/entity.vq", "230": "core/entity.vq", "231": "core/entity.vq", "232": "core/entity.vq", "233": "core/entity.vq", "234": "core/entity.vq", "235": "core/entity.vq",  "216": "core/entity.vq", "217": "core/entity.vq", "218": "core/entity.vq", "219": "core/entity.vq", "220": "core/entity.vq", "221": "core/entity.vq", "222": "core/entity.vq", "223": "core/entity.vq", "224": "core/entity.vq", "225": "core/entity.vq",  "206": "core/entity.vq", "207": "core/entity.vq", "208": "core/entity.vq", "209": "core/entity.vq", "210": "core/entity.vq", "211": "core/entity.vq", "212": "core/entity.vq", "213": "core/entity.vq", "214": "core/entity.vq", "215": "core/entity.vq", "196": "core/entity.vq", "197": "core/entity.vq", "198": "core/entity.vq", "199": "core/entity.vq", "200": "core/entity.vq", "201": "core/entity.vq", "202": "core/entity.vq", "203": "core/entity.vq", "204": "core/entity.vq", "205": "core/entity.vq",  "186": "core/scene.vq", "187": "core/scene.vq", "188": "core/scene.vq", "189": "core/scene.vq", "190": "core/scene.vq", "191": "core/scene.vq", "192": "core/scene.vq", "193": "core/scene.vq", "194": "core/scene.vq", "195": "core/scene.vq",  "176": "core/scene.vq", "177": "core/scene.vq", "178": "core/scene.vq", "179": "core/scene.vq", "180": "core/scene.vq", "181": "core/scene.vq", "182": "core/scene.vq", "183": "core/scene.vq", "184": "core/scene.vq", "185": "core/scene.vq",  "166": "core/scene.vq", "167": "core/scene.vq", "168": "core/scene.vq", "169": "core/scene.vq", "170": "core/scene.vq", "171": "core/scene.vq", "172": "core/scene.vq", "173": "core/scene.vq", "174": "core/scene.vq", "175": "core/scene.vq",  "156": "core/scene.vq", "157": "core/scene.vq", "158": "core/scene.vq", "159": "core/scene.vq", "160": "core/scene.vq", "161": "core/scene.vq", "162": "core/scene.vq", "163": "core/scene.vq", "164": "core/scene.vq", "165": "core/scene.vq",  "146": "core/resource.vq", "147": "core/resource.vq", "148": "core/resource.vq", "149": "core/resource.vq", "150": "core/resource.vq", "151": "core/resource.vq", "152": "core/resource.vq", "153": "core/resource.vq", "154": "core/resource.vq", "155": "core/resource.vq",  "136": "core/resource.vq", "137": "core/resource.vq", "138": "core/resource.vq", "139": "core/resource.vq", "140": "core/resource.vq", "141": "core/resource.vq", "142": "core/resource.vq", "143": "core/resource.vq", "144": "core/resource.vq", "145": "core/resource.vq",  "126": "core/resource.vq", "127": "core/resource.vq", "128": "core/resource.vq", "129": "core/resource.vq", "130": "core/resource.vq", "131": "core/resource.vq", "132": "core/resource.vq", "133": "core/resource.vq", "134": "core/resource.vq", "135": "core/resource.vq",  "116": "core/resource.vq", "117": "core/resource.vq", "118": "core/resource.vq", "119": "core/resource.vq", "120": "core/resource.vq", "121": "core/resource.vq", "122": "core/resource.vq", "123": "core/resource.vq", "124": "core/resource.vq", "125": "core/resource.vq",  "111": "core/render2d.vq", "112": "core/render2d.vq", "113": "core/render2d.vq", "114": "core/render2d.vq", "115": "core/render2d.vq", "106": "core/render2d.vq", "107": "core/render2d.vq", "108": "core/render2d.vq", "109": "core/render2d.vq", "110": "core/render2d.vq",  "101": "core/render2d.vq", "102": "core/render2d.vq", "103": "core/render2d.vq", "104": "core/render2d.vq", "105": "core/render2d.vq", "096": "core/render2d.vq", "097": "core/render2d.vq", "098": "core/render2d.vq", "099": "core/render2d.vq", "100": "core/render2d.vq",  "086": "core/math/vector2.vq", "087": "core/math/vector2.vq", "088": "core/math/vector2.vq", "089": "core/math/vector2.vq", "090": "core/math/vector2.vq", "091": "core/math/vector2.vq", "092": "core/math/vector2.vq", "093": "core/math/vector2.vq", "094": "core/math/vector2.vq", "095": "core/math/vector2.vq","081": "core/math/vector2.vq", "082": "core/math/vector2.vq", "083": "core/math/vector2.vq", "084": "core/math/vector2.vq", "085": "core/math/vector2.vq", "080": "core/math/vector2.vq", "079": "core/math/vector2.vq", "078": "core/math/vector2.vq", "077": "core/math/vector2.vq", "076": "core/math/vector2.vq", "071": "core/input.vq", "072": "core/input.vq", "073": "core/input.vq", "074": "core/input.vq", "075": "core/input.vq", "070": "core/input.vq", "069": "core/input.vq", "068": "core/input.vq", "067": "core/input.vq", "066": "core/input.vq", "065": "core/input.vq", "064": "core/input.vq", "063": "core/input.vq", "062": "core/input.vq", "061": "core/input.vq", "060": "core/input.vq", "059": "core/input.vq", "058": "core/input.vq", "057": "core/input.vq", "056": "core/input.vq", "055": "core/window.vq", "054": "core/window.vq", "053": "core/window.vq", "052": "core/window.vq", "051": "core/window.vq", "001": "core/math/vector2.vq", "002": "core/math/rect2.vq",
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
    """Discover versioned graphical demos recursively, preserving legacy CLI aliases."""
    base = ROOT / "demos"
    if not base.is_dir():
        return {}
    demos = {}
    for source in sorted(base.rglob("main.vq")):
        relative = source.relative_to(base)
        if len(relative.parts) == 4:
            version, chapter, folder, _ = relative.parts
            if not (version.count(".") == 2 and chapter[:2].isdigit()):
                continue
            key = f"{version}/{chapter}/{folder}"
            demos[key] = source
        elif len(relative.parts) == 2:
            demos[source.parent.name] = source
    return demos


def resolve_demo(name, demos):
    """Accept a canonical versioned ID or an unambiguous legacy demo name."""
    if name in demos:
        return name
    matches = [key for key in demos if key.rsplit("/", 1)[-1] == name or (name.startswith("d") and key.rsplit("/", 1)[-1] == name[1:])]
    if len(matches) > 1:
        # Do not silently choose a release when a name exists in several versions.
        return None
    if len(matches) == 1:
        return matches[0]
    return None


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


def demo_execution_succeeded(result):
    """Require a clean SDK run and a standalone VQ completion marker.

    The SDK may print diagnostics yet return zero, so the process status alone
    cannot be treated as a successful graphical demo.
    """
    if result.returncode != 0:
        return False
    stdout = result.stdout or ""
    stderr = result.stderr or ""
    if not any(line.strip() == "QGF_DEMO_OK" for line in stdout.splitlines()):
        return False
    diagnostic = re.compile(
        r"(?im)^\s*(?:semantic|lexer|parser|runtime|syntax|type|ffi|native)\s+error\s*:|"
        r"^\s*(?:error|fatal error|exception|traceback)\s*[:(]|"
        r"^\s*Traceback \(most recent call last\):"
    )
    return diagnostic.search(stdout + "\n" + stderr) is None


class BatchCancelled(Exception):
    """User requested to stop the active test sequence."""


def interruptible_run(command, *, cwd, timeout, input_text=None, env=None):
    """Run a child process while watching ESC on a POSIX terminal.

    Captured output is returned as a CompletedProcess. ESC cancels the whole
    current sequence; Ctrl+C works as a fallback outside interactive terminals.
    """
    import contextlib
    import signal
    import time

    @contextlib.contextmanager
    def escape_reader():
        if os.name != "posix" or not sys.stdin.isatty():
            yield None
            return
        import termios
        import tty
        fd = sys.stdin.fileno()
        original = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            yield fd
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, original)

    with tempfile.TemporaryFile(mode="w+t", encoding="utf-8") as output:
        proc = subprocess.Popen(
            command, cwd=cwd, stdin=subprocess.PIPE if input_text is not None else subprocess.DEVNULL,
            stdout=output, stderr=subprocess.STDOUT, text=True, env=env,
            start_new_session=(os.name == "posix"))
        try:
            if input_text is not None:
                try:
                    proc.stdin.write(input_text)
                    proc.stdin.flush()
                except BrokenPipeError:
                    pass
                finally:
                    proc.stdin.close()
            started = time.monotonic()
            with escape_reader() as terminal:
                while proc.poll() is None:
                    if timeout is not None and time.monotonic() - started >= timeout:
                        raise subprocess.TimeoutExpired(command, timeout)
                    if terminal is not None:
                        import select
                        if select.select([terminal], [], [], 0.05)[0]:
                            key = os.read(terminal, 1)
                            if key == b"\x1b":
                                raise BatchCancelled()
                    else:
                        time.sleep(0.05)
            output.seek(0)
            return subprocess.CompletedProcess(command, proc.returncode, output.read(), "")
        except BaseException:
            if proc.poll() is None:
                if os.name == "posix":
                    os.killpg(proc.pid, signal.SIGTERM)
                else:
                    proc.terminate()
                try:
                    proc.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    if os.name == "posix":
                        os.killpg(proc.pid, signal.SIGKILL)
                    else:
                        proc.kill()
                    proc.wait()
            raise


FPS_CHOICES = ("default", "5", "10", "15", "30", "60", "90", "120", "144", "300", "unlimited", "custom")


def parse_fps(value):
    """Return None for default, zero for unlimited, or a positive FPS cap."""
    if value is None or str(value).lower() == "default":
        return None
    if str(value).lower() == "unlimited":
        return 0
    try:
        number = int(str(value))
    except ValueError as error:
        raise ValueError("FPS must be default, unlimited, or a positive integer") from error
    if number < 1 or number > 10000:
        raise ValueError("FPS must be between 1 and 10000")
    return number


def apply_fps_cap(content, fps):
    """Apply pacing to a single-render-loop demo without changing frame budgets."""
    if fps is None:
        return content
    # Only demos with one present and one delay can safely use this transformation.
    if content.count('SDL_RenderPresent(renderer);') != 1 or content.count('SDL_Delay(delay_ms);') != 1:
        raise ValueError("demo does not support external FPS pacing")
    if 'while (running) {' not in content:
        raise ValueError("demo has no canonical rendering loop")
    if fps == 0:
        return content.replace('SDL_Delay(delay_ms);', 'SDL_Delay(0);', 1)
    # SDL_GetTicks provides elapsed-time pacing, rather than a fixed delay
    # after rendering. Millisecond granularity is a known limitation.
    declaration = 'extern "C" u64 SDL_GetTicks();'
    if declaration not in content:
        content = content.replace('extern "C" void SDL_Delay(u32 milliseconds);',
                                  'extern "C" void SDL_Delay(u32 milliseconds);\n' + declaration, 1)
    period = max(1, 1000 // fps)
    # Keep arithmetic in u64: Visual Quar rejects mixed-width operations.
    content = content.replace('while (running) {',
                              f'while (running) {{\n    u64 qgf_frame_start_ms = SDL_GetTicks();\n    u64 qgf_period_ms = {period};', 1)
    pacing = ("while (SDL_GetTicks() - qgf_frame_start_ms < qgf_period_ms) {\n"
              "        SDL_Delay(1);\n"
              "    }")
    return content.replace('SDL_Delay(delay_ms);', pacing, 1)



def fps_menu(current):
    """Return a selected FPS cap, or the previous selection on cancellation."""
    entries = [(index + 1, name) for index, name in enumerate(FPS_CHOICES)]
    screen("QGF - FPS CAP", [(0, "Back")] + entries)
    selected = select([(0, "Back")] + entries)
    if not selected or selected == "0":
        return current
    choice = FPS_CHOICES[int(selected) - 1]
    if choice == "custom":
        choice = input("Custom FPS (1-10000): ").strip()
    try:
        return parse_fps(choice)
    except ValueError as error:
        print(f"Invalid FPS: {error}")
        return current


def audit_demo_fps(chapter=None):
    """Report structural FPS-cap compatibility without executing or changing demos."""
    selected = [(name, source) for name, source in discover_demos().items()
                if "/" in name and (chapter is None or demo_chapter(source) == chapter)]
    if not selected:
        print("No matching graphical demos")
        return False
    counts = {"SUPPORTED": 0, "UNSUPPORTED": 0}
    for name, source in selected:
        try:
            apply_fps_cap(source.read_text(encoding="utf-8"), 60)
        except (ValueError, OSError) as error:
            counts["UNSUPPORTED"] += 1
            print(f"UNSUPPORTED {name}: {error}")
        else:
            counts["SUPPORTED"] += 1
            print(f"SUPPORTED {name}")
    print("FPS compatibility audit: " + " ".join(f"{key}={value}" for key, value in counts.items()))
    print("Structural check only: does not validate actual FPS or Visual Quar execution")
    return True


def run_demo(name, sdk, smoke=False, fps=None):
    """Run a VQ SDL3 demo in its own process; batch mode has a fixed frame count."""
    demos = discover_demos()
    resolved = resolve_demo(name, demos)
    source = demos.get(resolved)
    if source is None:
        print(f"FAIL: unknown or ambiguous demo {name}; use --list-demos for canonical IDs")
        return False
    configured_library = os.environ.get("QGF_SDL3_LIBRARY")
    if configured_library and not Path(configured_library).is_file():
        print(f"FAIL {name}: QGF_SDL3_LIBRARY does not point to a file: {configured_library}")
        return False
    library = find_sdl3_library()
    if library is None:
        print(f"SKIP {name}: SDL3 shared library unavailable (set QGF_SDL3_LIBRARY)")
        return None
    if not (sdk / "main.py").is_file():
        print(f"FAIL {name}: Visual Quar SDK entry point not found: {sdk / 'main.py'}")
        return False
    import tempfile
    with tempfile.TemporaryDirectory(prefix="qgf_demo_") as folder:
        temporary = Path(folder) / "main.vq"
        content = source.read_text(encoding="utf-8")
        if smoke:
            import json
            try:
                metadata = json.loads((source.parent / "demo.json").read_text(encoding="utf-8"))
                frames = metadata["batch_frames"]
                if not isinstance(frames, int) or isinstance(frames, bool) or not 1 <= frames <= 3600:
                    raise ValueError("batch_frames must be an integer from 1 to 3600")
            except (OSError, KeyError, ValueError, TypeError) as error:
                print(f"FAIL {name}: invalid demo metadata ({error})")
                return False
            # Both historical literal limits and the newer max_frames declaration
            # are canonical. Keep the demo's batch frame budget independent of FPS.
            frame_marker = "if (frame_count >= 60)"
            variable_marker = "if (frame_count >= max_frames)"
            if variable_marker in content:
                import re
                declaration = re.compile(r"\bu64 max_frames = [0-9]+;")
                if len(declaration.findall(content)) != 1:
                    print(f"FAIL {name}: missing unique max_frames declaration")
                    return False
                content = declaration.sub(f"u64 max_frames = {frames};", content, count=1)
            elif frame_marker in content:
                content = content.replace(frame_marker, f"if (frame_count >= {frames})")
            else:
                print(f"FAIL {name}: missing canonical frame limit")
                return False
            marker = "bool batch_mode = false;"
            if content.count(marker) != 1:
                print(f"FAIL {name}: missing canonical batch mode declaration")
                return False
            content = content.replace(marker, "bool batch_mode = true;", 1)
        try:
            content = apply_fps_cap(content, fps)
        except ValueError as error:
            print(f"SKIP {name}: {error}")
            return None
        temporary.write_text(content, encoding="utf-8")
        command = [sys.executable, str(sdk / "main.py"), "--native-library", library,
                   "-f", str(temporary)]
        try:
            result = interruptible_run(command, cwd=sdk, input_text="1\n",
                                       timeout=15 if smoke else None,
                                       env={**os.environ, "TERM": "dumb"})
        except subprocess.TimeoutExpired:
            print(f"TIMEOUT {name}")
            return False
        except OSError as error:
            print(f"FAIL {name}: {error}")
            return False
        if result.stdout:
            print(result.stdout.strip())
        if result.stderr:
            print(result.stderr.strip(), file=sys.stderr)
        success = demo_execution_succeeded(result)
        print(f"{'PASS' if success else 'FAIL'} {name} (exit={result.returncode})")
        return success


def run_demo_batch(sdk, chapter=None, fps=None):
    """Run every selected demo independently; report pass, fail and skip."""
    selected = [(name, source) for name, source in discover_demos().items()
                if chapter is None or demo_chapter(source) == chapter]
    # Keep legacy aliases for compatibility, but execute each migrated demo once.
    migrated = {key.rsplit("/", 1)[-1] for key, _ in selected if "/" in key}
    selected = [(key, source) for key, source in selected
                if "/" in key or key.removeprefix("d") not in migrated]
    if not selected:
        print("No matching graphical demos")
        return False
    counts = {"PASS": 0, "FAIL": 0, "SKIP": 0}
    for name, _ in selected:
        outcome = run_demo(name, sdk, smoke=True, fps=fps)
        counts["SKIP" if outcome is None else "PASS" if outcome else "FAIL"] += 1
    print("Demo batch: " + " ".join(f"{key}={value}" for key, value in counts.items()))
    return counts["FAIL"] == 0 and counts["SKIP"] == 0


def demo_menu(sdk):
    """Offer both persistent interactive demos and bounded batch checks."""
    fps = None
    while True:
        demos = discover_demos()
        names = list(demos)
        entries = [(0, "Back"), (1, "Run one interactive demo"),
                   (2, "Batch test all graphical demos"),
                   (3, "Batch test demos of a chapter"),
                   (4, f"FPS cap: {fps if fps is not None else 'Default'}")]
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
                show_result(lambda: run_demo(names[int(selected) - 1], sdk, fps=fps))
        elif choice == "2":
            show_result(lambda: run_demo_batch(sdk, fps=fps))
        elif choice == "4":
            fps = fps_menu(fps)
        elif choice == "3":
            chapter_text = input("Chapter number: ").strip()
            if chapter_text.isdigit():
                show_result(lambda: run_demo_batch(sdk, chapter=int(chapter_text), fps=fps))


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
            result = interruptible_run(
                [sys.executable, str(sdk / "main.py"), "-f", str(assembled)],
                cwd=sdk, input_text="1\n", timeout=30,
                env={**os.environ, "TERM": "dumb"})
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
            proc = interruptible_run(command, cwd=ROOT, timeout=45)
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
        if number == 8 and title == "QUAR GAME FRAMEWORK / 0.0.1":
            print("-" * 46)
        if number == 2 and title == "QGF - 2D DEMOS":
            print("-" * 46)
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
    except BatchCancelled:
        print("\nCANCELLED: test sequence stopped by ESC")
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
    parser.add_argument("--fps", default="default", help="FPS cap: default, unlimited, or 1-10000")
    parser.add_argument("--fps-audit", action="store_true", help="Check FPS pacing compatibility without running demos")
    parser.add_argument("--demo-all", action="store_true", help="Batch test all graphical demos")
    parser.add_argument("--demo-chapter", type=int, help="Batch test graphical demos of a chapter")
    parser.add_argument("--check", action="store_true", help="Check example dependencies without executing")
    args = parser.parse_args()
    try:
        fps = parse_fps(args.fps)
    except ValueError as error:
        parser.error(str(error))
    if args.fps_audit:
        return 0 if audit_demo_fps(chapter=args.demo_chapter) else 1
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
        return 0 if run_demo_batch(sdk, chapter=args.demo_chapter, fps=fps) else 1
    if args.demo or args.demo_smoke:
        return 0 if run_demo(args.demo or args.demo_smoke, sdk, smoke=bool(args.demo_smoke), fps=fps) else 1
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
    try:
        raise SystemExit(main())
    except BatchCancelled:
        print("\nCANCELLED: test sequence stopped by ESC")
        raise SystemExit(130)
    except KeyboardInterrupt:
        print("\nCANCELLED: interrupted by Ctrl+C")
        raise SystemExit(130)
