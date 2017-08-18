#import RPi.GPIO as GPIO #Use for Raspberry Pi GPIO
import testRPiGPIO as GPIO #Use for Debugging GPIO

LedPin = 11      # pin11 --- Control Led Indicator
RelayPin = 12    # pin12 --- Relay module x1
BtnPin = 13      # pin13 --- float Sensor Switch


def setup():
    GPIO.setmode(GPIO.BOARD)  # Numbers pins by physical location
    GPIO.setup(RelayPin, GPIO.OUT)  # Set pin mode as output
    GPIO.output(RelayPin, GPIO.HIGH)
    GPIO.setup(LedPin, GPIO.OUT)
    GPIO.output(LedPin, GPIO.HIGH)  # Set LedPin high(+3.3V) to make led off
    GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set BtnPin's mode is input, and pull up to high level(3.3V)


def loop():
    #   count = 1
    while True:
        if GPIO.input(BtnPin) == GPIO.HIGH:  # Check level sw.
            if pokreni_punjenje():
                print ('SYS OK')


"""
        print(count)
        print '...Rel on...led on'
        GPIO.output(LedPin, GPIO.HIGH)
        GPIO.output(RelayPin, GPIO.LOW)
        time.sleep(3.5)
        print 'Rel off...led off...'
        GPIO.output(LedPin, GPIO.LOW)
        GPIO.output(RelayPin, GPIO.HIGH)
        time.sleep(3.5)
        count += 1
"""


def pokreni_punjenje():
    print ('Pokrecem punjenje...')
    GPIO.output(LedPin, GPIO.LOW)  # led on
    GPIO.output(RelayPin, GPIO.LOW)# rel on
    if (status_punjenja()):
        print ('...Signal punjenja prisutan')
        try:
            while (GPIO.input(BtnPin) == GPIO.HIGH):
                print ('...Punim')
            if (zavrsi_punjenje()):
                print ('Ciklus punjenja zavrsen')
                return True
            else:
                print ('Greska kod Ciklusa punjenja')
                return False
        except:
            print ("Greska u kodu kod pracenja i zavrsetka punjenja")
            destroy()
    else:
        print ('Pokretanje punjenja nije uspjelo')
        destroy()



def zavrsi_punjenje():
    print ('Punjenje zavrseno, zatvaram ventil...')
    GPIO.output(LedPin, GPIO.LOW)  # led on
    GPIO.output(RelayPin, GPIO.LOW)  # rel on
    if not (status_punjenja()):
        print ('Signal zatvaranja predan')
        return True
    else:
        return False


def status_punjenja():
    try:
        if (GPIO.input(12)== True):
            return True
        else:
            return False
    except:
        print ("Pogreska kod statusa punjenja")
        print ("Provjeri kod !!")
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
