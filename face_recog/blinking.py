# import necessary library 匯入RPi.GPIO與time時間函式庫
import RPi.GPIO as GPIO   
import time   

# to use Raspberry Pi board pin numbers 使用板上定義的腳位號碼
GPIO.setmode(GPIO.BOARD)   

# set up pin 11 as an output  將P1接頭的11腳位設定為輸出 
GPIO.setup(11, GPIO.OUT)


def blink():
    try:
    # enter while loop unitl exit 隨著時間閃爍 迴圈會重複執行，直到強制離開
        while True:

        # Make an LED flash on 讓連接P1的11腳位LED燈會亮
           GPIO.output(11,True)  

        # Set time interval as 1 second delay 間隔一秒鐘
           time.sleep(1)    

        # Make an LED flash off  讓連接P1的11腳位LED燈會熄滅
           GPIO.output(11,False)

        # Set time interval as 1 second delay 間隔一秒鐘
           time.sleep(1)
       
    except KeyboardInterrupt:
        GPIO.cleanup()


def open_led():  #if face is not detected but moving
    try:
        GPIO.output(11,True)
    except KeyboardInterrupt:
        GPIO.cleanup()


    
def close_led():
    try:
        GPIO.output(11,False)
    except KeyboardInterrupt:
        GPIO.cleanup()



#GPIO.cleanup()
#open_led()