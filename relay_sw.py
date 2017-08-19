import RPi.GPIO as GPIO  #Use for Raspberry Pi GPIO
#import testRPiGPIO as GPIO  # Use for Debugging GPIO
import time

LedPin = 11    # pin11 --- Control Led Indicator
RelayPin = 12  # pin12 --- Relay module x1
BtnPin = 13    # pin13 --- float Sensor Switch


def setup():
    GPIO.setmode(GPIO.BOARD)          # Numbers pins by physical location
    GPIO.setup(RelayPin, GPIO.OUT)    # Set pin mode as output
    GPIO.output(RelayPin, GPIO.HIGH)   # relay off
    GPIO.setup(LedPin, GPIO.OUT)      # Set pin mode as output
    GPIO.output(LedPin, GPIO.LOW)    # Set led off
    GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set BtnPin's mode is input, and pull up to high level(3.3V)


def loop():
    #   count = 1
    while True:
        if GPIO.input(BtnPin) == GPIO.LOW:  # Check level sw.
            if pokreni_punjenje():
                print('SYS OK')
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
    GPIO.output(RelayPin, GPIO.LOW)  # rel on
    if status_punjenja():
        print('...Signal punjenja prisutan')
        try:
            while GPIO.input(BtnPin) == GPIO.LOW:
                print('Punim...')
                time.sleep(3)
            if zavrsi_punjenje():
                print('...Ciklus punjenja zavrsen')
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
    GPIO.output(RelayPin, GPIO.HIGH)  # rel off
    if not (status_punjenja()):
        print('...Signal zatvaranja predan')
        return True
    else:
        return False


def status_punjenja():
    try:
        if (GPIO.input(12) == GPIO.LOW):
            return True
        else:
            return False
    except:
        print("Pogreska kod statusa punjenja")
        print("Provjeri kod !!")
        destroy()


def destroy():
    GPIO.output(RelayPin, GPIO.HIGH)
    GPIO.cleanup()  # Release resource


if __name__ == '__main__':  # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be executed.
        destroy()
