from main import Ui_MainWindow

def getMetarChange(old_metar: dict, new_metar):
    change = []
    for i in old_metar:
        if old_metar[i] != new_metar[i] and i not in ['meta', 'remarks_info', 'remarks', 'other', 'density_altitude', 'pressure_altitude', 'wx_codes']:
            change.append(i)
    return change

def changeColor(Ui_MainWindow: Ui_MainWindow, key):
    def atisChange():
        Ui_MainWindow.currAtisLetter.setStyleSheet('color:red')
    def altimeterChange():
        Ui_MainWindow.GcurrInch.setStyleSheet('color:red')
        Ui_MainWindow.GcurrQNH.setStyleSheet('color:red')
    def cloudsChange():
        Ui_MainWindow.cloudInfo.setStyleSheet('color:green')
    def visibilityChange():
        Ui_MainWindow.visibility.setStyleSheet('color:green')
    def windDirChange():
        Ui_MainWindow.currWindDir.setStyleSheet('color:red')
        Ui_MainWindow.currWindDir2.setStyleSheet('color:red')
    def windSpdChange():
        Ui_MainWindow.currWindSpd.setStyleSheet('color:red')
        Ui_MainWindow.currWindSpd2.setStyleSheet('color:red')
    def dewpointChange():
        Ui_MainWindow.currDewPoint.setStyleSheet('color:green')
    def flightrulesChange():
        Ui_MainWindow.currCond.setStyleSheet('color:red')
    def windgustChange():
        Ui_MainWindow.currGust.setStyleSheet('color:green')
        Ui_MainWindow.currGust2.setStyleSheet('color:green')
    def tempChange():
        Ui_MainWindow.currTemp.setStyleSheet('color:green')
    def varWindDirChange():
        Ui_MainWindow.lowWindDir.setStyleSheet('color:green')
        Ui_MainWindow.highWindDir.setStyleSheet('color:green')
        Ui_MainWindow.lowWindDir2.setStyleSheet('color:green')
        Ui_MainWindow.highWindDir2.setStyleSheet('color:green')
    switcher = {
        'atis': atisChange(),
        'altimeter': altimeterChange(),
        'clouds': cloudsChange(),
        'visibility': visibilityChange(),
        'wind_direction': windDirChange(),
        'wind_speed': windSpdChange(),
        'dewpoint': dewpointChange(),
        'temperature': tempChange(),
        'wind_gust': windgustChange(),
        'wind_variable_direction': varWindDirChange(),
        'flight_rules': flightrulesChange()
    }
    switcher.setdefault(None)
    switcher.get(key)

def rechangeColor(Ui_MainWindow: Ui_MainWindow, change):
    if 'atis' not in change:
        Ui_MainWindow.currAtisLetter.setStyleSheet('color:black')
    if 'altimeter' not in change:
        Ui_MainWindow.GcurrInch.setStyleSheet('color:black')
        Ui_MainWindow.GcurrQNH.setStyleSheet('color:black')
    if 'clouds' not in change:
        Ui_MainWindow.cloudInfo.setStyleSheet('color:black')
    if 'visibility' not in change:
        Ui_MainWindow.visibility.setStyleSheet('color:black')
    if 'wind_direction' not in change:
        Ui_MainWindow.currWindDir.setStyleSheet('color:black')
        Ui_MainWindow.currWindDir2.setStyleSheet('color:black')
    if 'wind_speed' not in change:
        Ui_MainWindow.currWindSpd.setStyleSheet('color:black')
        Ui_MainWindow.currWindSpd2.setStyleSheet('color:black')
    if 'dewpoint' not in change:
        Ui_MainWindow.currDewPoint.setStyleSheet('color:black')
    if 'flight_rules' not in change:
        Ui_MainWindow.currCond.setStyleSheet('color:black')
    if 'wind_gust' not in change:
        Ui_MainWindow.currGust.setStyleSheet('color:black')
        Ui_MainWindow.currGust2.setStyleSheet('color:black')
    if 'temperature' not in change:
        Ui_MainWindow.currTemp.setStyleSheet('color:black')
    if 'variable_wind_direction' not in change:
        Ui_MainWindow.lowWindDir.setStyleSheet('color:black')
        Ui_MainWindow.highWindDir.setStyleSheet('color:black')
        Ui_MainWindow.lowWindDir2.setStyleSheet('color:black')
        Ui_MainWindow.highWindDir2.setStyleSheet('color:black')

