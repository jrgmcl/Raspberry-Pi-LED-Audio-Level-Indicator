import pyaudio
import numpy as np
import RPi.GPIO as GPIO

CHUNK = 64
maxValue = int(2**16)

p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,channels=2,rate=1024,
              input=True, frames_per_buffer=CHUNK)

led_array = [1, 2, 3, 4, 5, 6, 7]
val_array = [1, 15, 35, 50, 65, 80, 100]
    
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_array, GPIO.OUT, initial=GPIO.LOW)

try:
    i=0
    while True:
        data = np.frombuffer(stream.read(14), dtype=np.int16)
        dataL = np.abs(data[0::2])
        dataR = np.abs(data[1::2])
        peakL = ((np.max(dataL)-np.min(dataL)) / maxValue) * 200
        peakR = ((np.max(dataR)-np.min(dataR)) / maxValue) * 200
        PAverage = (peakL + peakR) / 2
        print("L:%.1f R:%.1f"%(peakL, peakR))
        print('Ctrl + C to Exit.')

        if PAverage >= 1:
            
            if PAverage >= val_array[i] :
                GPIO.output(led_array[i], GPIO.HIGH)
                i+=1
                
                if i == 7:
                    i-=1
                    continue
                else:
                    continue
                    
            else:
                GPIO.output(led_array[i], GPIO.LOW)
                i-=1
                continue

        else:
            GPIO.output(led_array[i], GPIO.LOW)
            if i >= 1:
                i-=1
                continue
            else:
                continue

except KeyboardInterrupt:
    GPIO.output(led_array, GPIO.LOW)
    exit()
