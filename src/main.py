from machine import Pin

led = Pin(12, Pin.OUT)

def main():
  led.value(0)
  while True:
    pass

if __name__ == "__main__":
  main()