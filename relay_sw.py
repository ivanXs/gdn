import RPi.GPIO as GPIO  # Use for Raspberry Pi GPIO
# import testRPiGPIO as GPIO  # Use for Debugging GPIO
import time
import Adafruit_CharLCD as LCD
from datetime import datetime

# Raspberry Pi BMC pinout configuration:

LedPin = 17  # pin11 --- Control Led Indicator
RelayPumpPin = 18  # pin12 --- Relay module x1
BtnPin = 27  # pin13 --- Float Sensor Switch
# LCD pinout
lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 5
lcd_d6 = 6
lcd_d7 = 22
lcd_backlight = 1
lcd_columns = 16
lcd_rows = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)


def setup():
    GPIO.setmode(GPIO.BCM)  # Numbers pins by BMC
    GPIO.setup(RelayPumpPin, GPIO.OUT)  # Set pump relay pin mode as output
    GPIO.output(RelayPumpPin, GPIO.HIGH)  # Set pump relay OFF
    GPIO.setup(LedPin, GPIO.OUT)  # Set control LED pin mode as output
    GPIO.output(LedPin, GPIO.LOW)  # Set control LED OFF
    GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set BtnPin's mode is input, and pull up to high level(3.3V)
    message = 'Demo x01'
    lcd.message(message)
    for i in range(lcd_columns - len(message)):
        time.sleep(0.5)
        lcd.move_right()
    for i in range(lcd_columns - len(message)):
        time.sleep(0.5)
        lcd.move_left()


def loop():
    #   count = 1
    lcd.set_backlight(0)
    while True:
        if GPIO.input(BtnPin) == GPIO.LOW:  # Check level sw.
            if pokreni_punjenje():
                print('SYS OK')
                lcd.message('Ciklus zavrsen\nSYS OK')
                time.sleep(5)
            else:
                print('SYS NOT OK')
                destroy()


def pokreni_punjenje():
    """
    Pokretanje faze punjenja
    :return:
    Vraca True ako je ciklus ispravno avrsen
    Vraca False ako ciklus nije ispravno zavrsen
    """
    print('Pokrecem punjenje...')
    GPIO.output(LedPin, GPIO.HIGH)  # led on
    GPIO.output(RelayPumpPin, GPIO.LOW)  # rel on
    if status_punjenja():
        print('...Signal punjenja prisutan')
        try:
            scroll_msg = 'Punim...'
            lcd.clear()
            while GPIO.input(BtnPin) == GPIO.LOW:
                print('Punim...')
                lcd.message(scroll_msg + '\n')
                lcd.message(datetime.now().strftime('%b %d  %H:%M:%S'))
                time.sleep(2)
            if zavrsi_punjenje():
                print('...Ciklus punjenja zavrsen')
                lcd.clear()
                return True
            else:
                print('Greska kod Ciklusa punjenja')
                return False
        except:
            print("Greska u kodu kod pracenja i zavrsetka punjenja")
            destroy()
    else:
        print('Pokretanje punjenja nije uspjelo')
        return False


def zavrsi_punjenje():
    print('Punjenje zavrseno, zatvaram ventil...')
    GPIO.output(LedPin, GPIO.LOW)  # led off
    GPIO.output(RelayPumpPin, GPIO.HIGH)  # rel off
    if not (status_punjenja()):
        print('...Signal zatvaranja predan')
        return True
    else:
        return False


def status_punjenja():
    try:
        if (GPIO.input(18) == GPIO.LOW):
            return True
        else:
            return False
    except:
        print("Pogreska kod statusa punjenja")
        print("Provjeri kod !!")
        destroy()


def display():
    pass


def destroy():
    GPIO.output(RelayPumpPin, GPIO.HIGH)
    lcd.clear()
    GPIO.cleanup()  # Release resource


if __name__ == '__main__':  # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be executed.
        destroy()
