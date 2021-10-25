OLED.init(128, 64)
ESP8266_IoT.init_wifi(SerialPin.P8, SerialPin.P12, BaudRate.BAUD_RATE115200)
radio.set_group(10)

def on_forever():
    OLED.clear()
    if ESP8266_IoT.wifi_state(True):
        OLED.write_string("Wifi: Connected")
    else:
        OLED.write_string("Wifi: Not connected")
    OLED.new_line()
    OLED.write_string("Time:")
    OLED.write_num(RTC_DS1307.get_time(RTC_DS1307.TimeType.HOUR))
    OLED.write_string(":")
    OLED.write_num(RTC_DS1307.get_time(RTC_DS1307.TimeType.MINUTE))
    OLED.write_string(":")
    OLED.write_num(RTC_DS1307.get_time(RTC_DS1307.TimeType.SECOND))
    OLED.new_line()
    OLED.write_string("Light:")
    OLED.write_num(Environment.read_light_intensity(AnalogPin.P1))
    OLED.new_line()
    OLED.write_string("Temperature: ")
    OLED.write_num(Environment.octopus_BME280(Environment.BME280_state.BME280_TEMPERATURE_C))
    OLED.write_string("" + String.from_char_code(248) + "C")
    OLED.new_line()
    OLED.write_string("Humidity:    ")
    OLED.write_num(Environment.octopus_BME280(Environment.BME280_state.BME280_HUMIDITY))
    OLED.write_string(" %")
    OLED.new_line()
    OLED.write_string("Atm presure: ")
    OLED.write_num(Environment.octopus_BME280(Environment.BME280_state.BME280_PRESSURE))
    OLED.write_string(" hPa")
    basic.pause(6000)
basic.forever(on_forever)

def on_forever2():
    if ESP8266_IoT.wifi_state(False):
        ESP8266_IoT.connect_wifi("H369A80DD29", "6E7F635F3F62")
    else:
        ESP8266_IoT.connect_thing_speak()
        ESP8266_IoT.set_data("0R0TS6I5YJPRTDIL",
            Environment.read_light_intensity(AnalogPin.P1),
            Environment.octopus_BME280(Environment.BME280_state.BME280_TEMPERATURE_C),
            Environment.octopus_BME280(Environment.BME280_state.BME280_HUMIDITY),
            Environment.octopus_BME280(Environment.BME280_state.BME280_PRESSURE))
        ESP8266_IoT.upload_data()
        radio.send_string("" + str(Environment.octopus_BME280(Environment.BME280_state.BME280_TEMPERATURE_C)) + "|" + str(Environment.octopus_BME280(Environment.BME280_state.BME280_PRESSURE)) + "|" + str(Environment.octopus_BME280(Environment.BME280_state.BME280_PRESSURE)))
    basic.pause(300000)
basic.forever(on_forever2)
