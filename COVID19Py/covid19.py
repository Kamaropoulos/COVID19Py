from typing import Dict, List
import requests
import json


class COVID19(object):
    sourced=None
    def __init__(self,sourced=None):
        if sourced is not None:
            self.sourced = sourced
        
    

    def _update(self, timelines):
        latest = self.getLatest()
        locations = self.getLocations(timelines)
        if self.latestData:
            self.previousData = self.latestData
        self.latestData = {
            "latest": latest,
            "locations": locations
        }

    

    def _request(self, endpoint, params=None):
        if params is None:
            params = {}
        response = requests.get(self.sourced.url + endpoint, {**params, "source":self.sourced.data_source})
        response.raise_for_status()
        return response.json()

    def getAll(self, timelines=False):
        self._update(timelines)
        return self.latestData

    def getLatestChanges(self):
        changes = None
        if self.previousData:
            changes = {
                "confirmed": self.latestData["latest"]["confirmed"] - self.latestData["latest"]["confirmed"],
                "deaths": self.latestData["latest"]["deaths"] - self.latestData["latest"]["deaths"],
                "recovered": self.latestData["latest"]["recovered"] - self.latestData["latest"]["recovered"],
            }
        else:
            changes = {
                "confirmed": 0,
                "deaths": 0,
                "recovered": 0,
            }
        return changes

    def getLatest(self) -> List[Dict[str, int]]:
        """
        :return: The latest amount of total confirmed cases, deaths, and recoveries.
        """
        data = self._request("/v2/latest")
        return data["latest"]

    def getLocations(self, timelines=False, rank_by: str = None) -> List[Dict]:
        """
        Gets all locations affected by COVID-19, as well as latest case data.
        :param timelines: Whether timeline information should be returned as well.
        :param rank_by: Category to rank results by. ex: confirmed
        :return: List of dictionaries representing all affected locations.
        """
        data = None
        if timelines:
            data = self._request("/v2/locations", {"timelines": str(timelines).lower()})
        else:
            data = self._request("/v2/locations")

        data = data["locations"]
        
        ranking_criteria = ['confirmed', 'deaths', 'recovered']
        if rank_by is not None:
            if rank_by not in ranking_criteria:
                raise ValueError("Invalid ranking criteria. Expected one of: %s" % ranking_criteria)

            ranked = sorted(data, key=lambda i: i['latest'][rank_by], reverse=True)
            data = ranked

        return data
    
    


    def getCountInfo(self,count,timelines=False) -> List[Dict]:

        data = None

        if count.nameOfCount is not None:
            if timelines:
               data = self._request("/v2/locations", {"country": count.nameOfCount, "timelines": str(timelines).lower()})

            else:
                 data = self._request("/v2/locations", {"country": count.nameOfCount})

            return data["locations"]

        if count.Count_Code is not None:
            if timelines:
               data = self._request("/v2/locations", {"country_code": count.Count_Code, "timelines": str(timelines).lower()})

            else:
                 data = self._request("/v2/locations", {"country_code": count.Count_Code})
            return data["locations"]     

        if count.Count_num is not None:
            if timelines:
               data = self._request("/v2/locations", {"country_code": count.Count_num, "timelines": str(timelines).lower()})

            else:
                 data = self._request("/v2/locations", {"country_code": count.Count_num})
            return data["locations"] 








###################################################




class fetchData(object):

    default_url = "https://covid-tracker-us.herokuapp.com"
    url = ""
    data_source = ""
    previousData = None
    latestData = None
    _valid_data_sources = []

    mirrors_source = "https://raw.github.com/Kamaropoulos/COVID19Py/master/mirrors.json"
    mirrors = None

    def __init__(self, url="https://covid-tracker-us.herokuapp.com", data_source='jhu'):
        # Skip mirror checking if custom url was passed
        if url == self.default_url:
            # Load mirrors
            response = requests.get(self.mirrors_source)
            response.raise_for_status()
            self.mirrors = response.json()

            # Try to get sources as a test
            for mirror in self.mirrors:
                # Set URL of mirror
                self.url = mirror["url"]
                result = None
                try:
                    result = self._getSources()
                except Exception as e:
                    # URL did not work, reset it and move on
                    self.url = ""
                    continue

                # TODO: Should have a better health-check, this is way too hacky...
                if "jhu" in result:
                    # We found a mirror that worked just fine, let's stick with it
                    break

                # None of the mirrors worked. Raise an error to inform the user.
                raise RuntimeError("No available API mirror was found.")

        else:
            self.url = url

        self._valid_data_sources = self._getSources()
        if data_source not in self._valid_data_sources:
            raise ValueError("Invalid data source. Expected one of: %s" % self._valid_data_sources)
        self.data_source = data_source

    def _getSources(self):
        response = requests.get(self.url + "/v2/sources")
        response.raise_for_status()
        return response.json()["sources"]

        ##################################################################################

###########################################################################################################
class CaseByCountry():

    nameOfCount = ''
    Count_Code = ''
    Count_num = ''
    nameOfCount_check = False
    Count_Code_check = False
    Count_num_check = False
    

    def __init__(self,nameOfCount=None,Count_Code=None,Count_num=None):




        if nameOfCount is not None:
            self.nameOfCount = nameOfCount
            self.nameOfCount_check = True

        if Count_Code is not None:
            self.Count_Code = Count_Code
            self.Count_Code_check = True


        if Count_num is not None:
            self.Count_num = Count_num
            self.Count_num_check = True 

        country_dict = {'Afghanistan': 'AF',
                'Albania': 'AL',
                'Algeria': 'DZ',
                'American Samoa': 'AS',
                'Andorra': 'AD',
                'Angola': 'AO',
                'Anguilla': 'AI',
                'Antarctica': 'AQ',
                'Antigua and Barbuda': 'AG',
                'Argentina': 'AR',
                'Armenia': 'AM',
                'Aruba': 'AW',
                'Australia': 'AU',
                'Austria': 'AT',
                'Azerbaijan': 'AZ',
                'Bahamas': 'BS',
                'Bahrain': 'BH',
                'Bangladesh': 'BD',
                'Barbados': 'BB',
                'Belarus': 'BY',
                'Belgium': 'BE',
                'Belize': 'BZ',
                'Benin': 'BJ',
                'Bermuda': 'BM',
                'Bhutan': 'BT',
                'Bolivia, Plurinational State of': 'BO',
                'Bonaire, Sint Eustatius and Saba': 'BQ',
                'Bosnia and Herzegovina': 'BA',
                'Botswana': 'BW',
                'Bouvet Island': 'BV',
                'Brazil': 'BR',
                'British Indian Ocean Territory': 'IO',
                'Brunei Darussalam': 'BN',
                'Bulgaria': 'BG',
                'Burkina Faso': 'BF',
                'Burundi': 'BI',
                'Cambodia': 'KH',
                'Cameroon': 'CM',
                'Canada': 'CA',
                'Cape Verde': 'CV',
                'Cayman Islands': 'KY',
                'Central African Republic': 'CF',
                'Chad': 'TD',
                'Chile': 'CL',
                'China': 'CN',
                'Christmas Island': 'CX',
                'Cocos (Keeling) Islands': 'CC',
                'Colombia': 'CO',
                'Comoros': 'KM',
                'Congo': 'CG',
                'Congo, the Democratic Republic of the': 'CD',
                'Cook Islands': 'CK',
                'Costa Rica': 'CR',
                'Country name': 'Code',
                'Croatia': 'HR',
                'Cuba': 'CU',
                'Curaçao': 'CW',
                'Cyprus': 'CY',
                'Czech Republic': 'CZ',
                "Côte d'Ivoire": 'CI',
                'Denmark': 'DK',
                'Djibouti': 'DJ',
                'Dominica': 'DM',
                'Dominican Republic': 'DO',
                'Ecuador': 'EC',
                'Egypt': 'EG',
                'El Salvador': 'SV',
                'Equatorial Guinea': 'GQ',
                'Eritrea': 'ER',
                'Estonia': 'EE',
                'Ethiopia': 'ET',
                'Falkland Islands (Malvinas)': 'FK',
                'Faroe Islands': 'FO',
                'Fiji': 'FJ',
                'Finland': 'FI',
                'France': 'FR',
                'French Guiana': 'GF',
                'French Polynesia': 'PF',
                'French Southern Territories': 'TF',
                'Gabon': 'GA',
                'Gambia': 'GM',
                'Georgia': 'GE',
                'Germany': 'DE',
                'Ghana': 'GH',
                'Gibraltar': 'GI',
                'Greece': 'GR',
                'Greenland': 'GL',
                'Grenada': 'GD',
                'Guadeloupe': 'GP',
                'Guam': 'GU',
                'Guatemala': 'GT',
                'Guernsey': 'GG',
                'Guinea': 'GN',
                'Guinea-Bissau': 'GW',
                'Guyana': 'GY',
                'Haiti': 'HT',
                'Heard Island and McDonald Islands': 'HM',
                'Holy See (Vatican City State)': 'VA',
                'Honduras': 'HN',
                'Hong Kong': 'HK',
                'Hungary': 'HU',
                'ISO 3166-2:GB': '(.uk)',
                'Iceland': 'IS',
                'India': 'IN',
                'Indonesia': 'ID',
                'Iran, Islamic Republic of': 'IR',
                'Iraq': 'IQ',
                'Ireland': 'IE',
                'Isle of Man': 'IM',
                'Israel': 'IL',
                'Italy': 'IT',
                'Jamaica': 'JM',
                'Japan': 'JP',
                'Jersey': 'JE',
                'Jordan': 'JO',
                'Kazakhstan': 'KZ',
                'Kenya': 'KE',
                'Kiribati': 'KI',
                "Korea, Democratic People's Republic of": 'KP',
                'Korea, Republic of': 'KR',
                'Kuwait': 'KW',
                'Kyrgyzstan': 'KG',
                "Lao People's Democratic Republic": 'LA',
                'Latvia': 'LV',
                'Lebanon': 'LB',
                'Lesotho': 'LS',
                'Liberia': 'LR',
                'Libya': 'LY',
                'Liechtenstein': 'LI',
                'Lithuania': 'LT',
                'Luxembourg': 'LU',
                'Macao': 'MO',
                'Macedonia, the former Yugoslav Republic of': 'MK',
                'Madagascar': 'MG',
                'Malawi': 'MW',
                'Malaysia': 'MY',
                'Maldives': 'MV',
                'Mali': 'ML',
                'Malta': 'MT',
                'Marshall Islands': 'MH',
                'Martinique': 'MQ',
                'Mauritania': 'MR',
                'Mauritius': 'MU',
                'Mayotte': 'YT',
                'Mexico': 'MX',
                'Micronesia, Federated States of': 'FM',
                'Moldova, Republic of': 'MD',
                'Monaco': 'MC',
                'Mongolia': 'MN',
                'Montenegro': 'ME',
                'Montserrat': 'MS',
                'Morocco': 'MA',
                'Mozambique': 'MZ',
                'Myanmar': 'MM',
                'Namibia': 'NA',
                'Nauru': 'NR',
                'Nepal': 'NP',
                'Netherlands': 'NL',
                'New Caledonia': 'NC',
                'New Zealand': 'NZ',
                'Nicaragua': 'NI',
                'Niger': 'NE',
                'Nigeria': 'NG',
                'Niue': 'NU',
                'Norfolk Island': 'NF',
                'Northern Mariana Islands': 'MP',
                'Norway': 'NO',
                'Oman': 'OM',
                'Pakistan': 'PK',
                'Palau': 'PW',
                'Palestine, State of': 'PS',
                'Panama': 'PA',
                'Papua New Guinea': 'PG',
                'Paraguay': 'PY',
                'Peru': 'PE',
                'Philippines': 'PH',
                'Pitcairn': 'PN',
                'Poland': 'PL',
                'Portugal': 'PT',
                'Puerto Rico': 'PR',
                'Qatar': 'QA',
                'Romania': 'RO',
                'Russian Federation': 'RU',
                'Rwanda': 'RW',
                'Réunion': 'RE',
                'Saint Barthélemy': 'BL',
                'Saint Helena, Ascension and Tristan da Cunha': 'SH',
                'Saint Kitts and Nevis': 'KN',
                'Saint Lucia': 'LC',
                'Saint Martin (French part)': 'MF',
                'Saint Pierre and Miquelon': 'PM',
                'Saint Vincent and the Grenadines': 'VC',
                'Samoa': 'WS',
                'San Marino': 'SM',
                'Sao Tome and Principe': 'ST',
                'Saudi Arabia': 'SA',
                'Senegal': 'SN',
                'Serbia': 'RS',
                'Seychelles': 'SC',
                'Sierra Leone': 'SL',
                'Singapore': 'SG',
                'Sint Maarten (Dutch part)': 'SX',
                'Slovakia': 'SK',
                'Slovenia': 'SI',
                'Solomon Islands': 'SB',
                'Somalia': 'SO',
                'South Africa': 'ZA',
                'South Georgia and the South Sandwich Islands': 'GS',
                'South Sudan': 'SS',
                'Spain': 'ES',
                'Sri Lanka': 'LK',
                'Sudan': 'SD',
                'Suriname': 'SR',
                'Svalbard and Jan Mayen': 'SJ',
                'Swaziland': 'SZ',
                'Sweden': 'SE',
                'Switzerland': 'CH',
                'Syrian Arab Republic': 'SY',
                'Taiwan, Province of China': 'TW',
                'Tajikistan': 'TJ',
                'Tanzania, United Republic of': 'TZ',
                'Thailand': 'TH',
                'Timor-Leste': 'TL',
                'Togo': 'TG',
                'Tokelau': 'TK',
                'Tonga': 'TO',
                'Trinidad and Tobago': 'TT',
                'Tunisia': 'TN',
                'Turkey': 'TR',
                'Turkmenistan': 'TM',
                'Turks and Caicos Islands': 'TC',
                'Tuvalu': 'TV',
                'Uganda': 'UG',
                'Ukraine': 'UA',
                'United Arab Emirates': 'AE',
                'United Kingdom': 'GB',
                'United States': 'US',
                'United States Minor Outlying Islands': 'UM',
                'Uruguay': 'UY',
                'Uzbekistan': 'UZ',
                'Vanuatu': 'VU',
                'Venezuela, Bolivarian Republic of': 'VE',
                'Viet Nam': 'VN',
                'Virgin Islands, British': 'VG',
                'Virgin Islands, U.S.': 'VI',
                'Wallis and Futuna': 'WF',
                'Western Sahara': 'EH',
                'Yemen': 'YE',
                'Zambia': 'ZM',
                'Zimbabwe': 'ZW',
                'Åland Islands': 'AX'}

                    

        def __str__(self):
           

            if (self.nameOfCount).capitalize() not in country_dict:
                return("Country does not exists")  


            return ( "{: <15} ({}) num={}".format(self.nameOfCount,self.Count_Code,self.Count_num))
            ###########################################################################################################

#Testing
def main():
    CovData = COVID19(fetchData())
    print(CovData.getCountInfo(CaseByCountry(nameOfCount="Canada")))
if __name__ == '__main__':
    main() 
