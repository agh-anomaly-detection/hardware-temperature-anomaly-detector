from cpu_load_generator import load_all_cores
import argparse
import RPi.GPIO as GPIO
import time

def generate_load_in_period(time, step):
    for load in range(0, 101, step):
        print("Generating load: {}% for {} seconds".format(load, time))
        load_all_cores(duration_s=time, target_load=(load/100.0))
    for load in range(100, -1, -step):
        print("Generating load: {}% for {} seconds".format(load, time))
        load_all_cores(duration_s=time, target_load=(load/100.0))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate CPU load')
    parser.add_argument('--step', type=int, default=10, help='Step of load generation [CPU]')
    parser.add_argument('--time', type=int, default=300, help='Time per step')
    parser.add_argument('--count', type=int, default=-1, help='Number of periods to generate')
    parser.add_argument('--fan', type=int, default=100, help='Fan speed [0-100]')
    parser.add_argument('--delay', type=int, default=0, help='Delay before measuring')
    args = parser.parse_args()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    fan = GPIO.PWM(18,50)
    fan.start(args.fan)
    time.sleep(args.delay)
    if(args.count == -1):
        while True:
            generate_load_in_period(args.time, args.step)
    for i in range(args.count):
        generate_load_in_period(args.time, args.step)
