import serial
import time
import csv
from datetime import datetime

def read_serial_to_csv(port_name, baud_rate, timeout_ms, rx_hex_data):
    # 设置超时时间
    timeout = timeout_ms / 1000.0  # 转换为秒
    start_time = None
    last_time = 0

    # 创建CSV文件名
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"serial_data_{current_time}_{port_name.replace('/', '_')}_{baud_rate}"
    

    # 打开串口
    with serial.Serial(port_name, baud_rate, timeout=timeout) as ser, open(filename + ".csv", mode='w', newline='') as csvfile, open(filename + ".bin", mode='wb') as binfile:
        csvfile.write('Time (ms), Data (Hex)')

        byte_data = bytes.fromhex(rx_hex_data)
        print(f"Sending to {port_name}: {rx_hex_data}")
        ser.write(byte_data)

        while True:
            if ser.in_waiting > 0:  # 检查是否有数据可读
                data = ser.read(ser.in_waiting)  # 读取所有可用数据
                binfile.write(data)
                current_time = time.time()  # 获取当前时间

                if start_time is None:
                    start_time = current_time  # 第一次收到数据时初始化开始时间

                # 将时间转换为相对时间
                relative_time = (current_time - start_time) * 1000  # 转换为毫秒
                
                # 转换为16进制字符串并插入空格，使用大写字母
                hex_data = ' '.join(format(byte, '02X') for byte in data)  

                # 如果经过的时间大于超时时间，则保存到新的一行
                if (current_time - last_time) * 1000 > timeout_ms:
                    csvfile.write(f'\r\n{int(relative_time)}, {hex_data}')  # 写入数据
                    last_time = current_time  # 更新最后一次收到数据的时间
                    print(f"\nRecive [{relative_time/1000 :.3f} s]: {hex_data}" ,end='')
                else:
                    csvfile.write(f" {hex_data}")
                    print(f" {hex_data}" ,end='')

if __name__ == "__main__":
    # 示例调用
    # read_serial_to_csv('COM1', 38400, 30, "01 05 00 11 ff 00 DC 3F")  # 根据实际情况修改串口和波特率
    read_serial_to_csv('COM1', 38400, 50, "01 05 00 10 FF 00 8D FF")  # 根据实际情况修改串口和波特率
