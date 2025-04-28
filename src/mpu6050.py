from machine import I2C

class accel():
    def __init__(self, i2c, addr=0x68):
        self.iic = i2c
        self.addr = addr
        # Wake up the MPU6050 from sleep mode
        self.iic.writeto(self.addr, bytearray([107, 0]))

    def get_raw_values(self):
        # Read 14 bytes starting from register 0x3B
        return self.iic.readfrom_mem(self.addr, 0x3B, 14)

    def bytes_toint(self, firstbyte, secondbyte):
        # Convert two bytes into a signed integer
        if not firstbyte & 0x80:
            return (firstbyte << 8) | secondbyte
        return -(((firstbyte ^ 0xFF) << 8) | (secondbyte ^ 0xFF) + 1)

    def get_values(self):
        raw_data = self.get_raw_values()
        vals = {
            "AcX": self.bytes_toint(raw_data[0], raw_data[1]),
            "AcY": self.bytes_toint(raw_data[2], raw_data[3]),
            "AcZ": self.bytes_toint(raw_data[4], raw_data[5]),
            "Tmp": self.bytes_toint(raw_data[6], raw_data[7]) / 340.0 + 36.53,  # Temp in °C
            "GyX": self.bytes_toint(raw_data[8], raw_data[9]),
            "GyY": self.bytes_toint(raw_data[10], raw_data[11]),
            "GyZ": self.bytes_toint(raw_data[12], raw_data[13]),
        }
        return vals
