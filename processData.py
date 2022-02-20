from logging import error
from random import randint
import requests
from fetchData import *
from configparser import ConfigParser


def check_station(station):
    data = fetch_whazzup()
    res = ""
    for i in range(0, len(data) - 1):
        if str(data[i]['lines'][0]).find(station) != -1:
            res = "Station online"
            break
    if res == "":
        res = "Station offline"
        logging.warning(f"Station {station} offline")
        return res, -1
    if station.find("CTR") != -1:
        logging.warning(f"No METAR for station {station}")
        return "Make sure you choose a facility featuring a METAR!", -1
    logging.info(f"Station {station} online and has METAR")
    return res, 0


class Atis:
    data, station = "", ""

    def __init__(self, station):
        self.station = station
        data = fetch_whazzup()
        for i in range(0, len(data) - 1):
            if str(data[i]['lines'][0]).find(station) != -1:
                self.data = data[i]['lines']
                break

        if not self.data:
            logging.critical("Station seems to be offline.")

        try:
            self.data[3]
            logging.info("METAR available")
        except IndexError:
            logging.error("Make sure you choose a facility featuring a METAR!")

    def get_runways(self):
        logging.debug("Fetching runways...")
        runways = []
        rwy = None
        for i in range(0, len(self.data) - 1):
            if self.data[i].find("ARR") != -1:
                rwy = self.data[i]
        rwy = rwy.replace("ARR RWY ", "").replace(
            "DEP RWY ", "").split(" / TRL ")[0]
        rwy = rwy.strip().split("/")
        for i in range(0, len(rwy)):
            for j in range(0, len(rwy[i].split(" "))):
                if rwy[i].split(" ")[j] not in runways:
                    if not "LRC" in rwy[i].split(" ")[j]:
                        runways.append(str(rwy[i].split(" ")[j]))
                    else:
                        if rwy[i].split(" ")[j][0:2] not in runways:
                            runways.append(
                                str(rwy[i].split(" ")[j]))
        ret1, ret2 = 0, 0
        logging.debug(f"Runways list created, is: {runways}")
        for i in range(0, len(runways)):
            if runways[i][:2] == ret1:
                pass
            else:
                if ret1:
                    ret2 = runways[i][:2]
                else:
                    ret1 = runways[i][:2]
        if ret1 and ret2:
            if 180 - (360 - int(ret1)) < 180 - (360 - int(ret2)):
                logging.info("Returning runways")
                return str(ret1), str(ret2)
            else:
                logging.info("Returning runways")
                return str(ret2), str(ret1)
        else:
            logging.info("Returning runways")
            return str(ret1), str(ret1)

    def get_metar(self):
        if self.data[3].find(self.station[:4]) != -1:
            metar = self.data[3]
        elif self.data[2].find(self.station[:4]) != -1:
            metar = self.data[2]
        if metar:
            logging.info("Returned metar")
            return metar
        else:
            logging.error(f"Error while parsing, check data: {self.data}")

    def get_atisLetter(self):
        if 'information' in self.data[2]:
            logging.info(f"Returned ATIS letter, is: {self.data[2].split('information ')[1][0]}")
            return self.data[2].split('information ')[1][0]
        else:
            logging.info(f"Returned ATIS letter, is: {self.data[1].split('information ')[1][0]}")
            return self.data[1].split('information ')[1][0]


class Metar():
    metar = ""

    def get_metar(self, metar):
        config = ConfigParser()
        config.read('config.ini')
        headers = {
            'Content-Type': 'text/plain',
            'Authorization': config['DEFAULT']['TOKEN']
        }
        response = requests.post('https://avwx.rest/api/parse/metar', headers=headers, data=str(metar))
        logging.info("METAR request sent")
        self.metar = json.loads(response.content)
        logging.info("METAR response received")

    def get_inch(self, *qnh):
        inch = 0.0
        if not qnh:
            qnh = self.metar['altimeter']['value']
            inch = qnh / 33.86
        else:
            inch = qnh[0] / 33.86
        logging.info("Returning inches")
        return str(round(inch, 2))

    def get_qnh(self, *inch):
        if not inch:
            qnh = self.metar['altimeter']['value']
        else:
            qnh = inch[0] * 33.86
        logging.info("Returning QNH")
        return str(round(qnh))

    def is_vmc(self):
        logging.info("Returning flight rules")
        return self.metar['flight_rules']

    def get_clouds(self):
        cloudsstr = ""
        clouds = self.metar.get('clouds')
        for i in range(0, len(clouds)):
            cloudsstr += " " + str(clouds[i]['repr'])
        logging.info("Returning clouds")
        return "No clouds reported" if cloudsstr == "" else cloudsstr.replace(" ", "", 1)

    def get_visibility(self):
        logging.info("Returning visibility")
        return str(self.metar['visibility']['value'])

    def get_dewpoint(self):
        logging.info("Returning dewpoint")
        return self.metar['dewpoint']['repr']

    def get_temp(self):
        logging.info("Returning temperature")
        return self.metar['temperature']['repr']

    def get_winddir(self, *op):
        if not op:
            try:
                logging.info("Returning normal winddir")
                return str(self.metar['wind_direction']['repr'])
            except ValueError:
                logging.warning("ValueError while parsing str")
                return str("")
        elif op[0] == "max":
            if self.metar['wind_variable_direction'] == []:
                rand = randint(1, 10)
                try:
                    logging.info("Returning random max wind values")
                    return str(int(self.metar['wind_direction']['repr']) + rand if int(self.metar['wind_direction'][
                                                                                           'repr']) <= 360 - rand else f"0{str(int(self.metar['wind_direction']['repr']) - 360 + rand)}")
                except ValueError:
                    logging.warning("ValueError while parsing str")
                    return str("")
            else:
                logging.info("Returning max winddeg specified")
                return str(self.metar['wind_variable_direction'][1]['repr'])
        elif op[0] == "min":
            if self.metar['wind_variable_direction'] == []:
                rand = randint(1, 10)
                try:
                    logging.info("Returning random min winddeg values")
                    return str(int(self.metar['wind_direction']['repr']) - rand) if int(
                        self.metar['wind_direction']['repr']) >= rand else int(
                        self.metar['wind_direction']['repr']) + 360 - rand
                except ValueError:
                    logging.warning("ValueError while parsing str")
                    return str("")
            else:
                logging.info("Returning min winddeg specified")
                return str(self.metar['wind_variable_direction'][0]['repr'])

    def get_windspd(self, *op):
        if not op:
            try:
                logging.info("Returning normal windspd")
                return str(self.metar['wind_speed']['value'])
            except ValueError:
                logging.warning("ValueError while parsing str")
                return str("")
        elif op[0] == "max":
            rand = randint(1, 5)
            try:
                logging.info("Returning random max windspd")
                return str(int(self.metar['wind_speed']['value']) + rand)
            except ValueError:
                logging.warning("ValueError while parsing str")
                return str("")
        elif op[0] == "min":
            rand = randint(1, 5)
            try:
                logging.info("Returning random min windspd")
                return str(int(self.metar['wind_speed']['value']) - rand) if int(
                    self.metar['wind_speed']['value']) >= rand else str(0)
            except ValueError:
                logging.warning("ValueError while parsing str")
                return str("")

    def get_gust(self):
        if self.metar['wind_gust'] != None:
            logging.info("Returning gusts")
            return str(self.metar['wind_gust']['repr'])
        logging.info("No gusts")

    def return_metar(self):
        return self.metar

