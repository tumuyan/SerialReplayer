import serial
import time
import csv
import threading

def send_data_to_serial(port_name, baud_rate, file_name, delay, start_time):
    # 等待指定的延迟时间
    time.sleep(delay)

    # 打开串口
    with serial.Serial(port_name, baud_rate) as ser:
        with open(file_name, mode='r') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # 跳过表头

            for row in csv_reader:
                # 提取时间和数据
                time_ms, hex_data = row
                # 将16进制字符串转换为字节
                byte_data = bytes.fromhex(hex_data)

                # 计算当前时间与上一个发送时间的间隔
                elapsed_time = time.time() - start_time
                print(f"Sending to {port_name}: {byte_data} at {elapsed_time:.2f} seconds")
                
                # 发送数据到串口
                ser.write(byte_data)

                # 根据CSV文件中的时间间隔进行等待
                time.sleep(float(time_ms) / 1000.0)  # 将毫秒转换为秒

def main():
    # 串口参数配置
    serial_configs = [
        {'port_name': 'COM15', 'baud_rate': 38400, 'file_name': 'serial_data_20250109_020738_COM15_38400.csv', 'delay': 5},
        {'port_name': 'COM17', 'baud_rate': 38400, 'file_name': 'serial_data_20250109_021033_COM15_38400.csv', 'delay': 5},
        # 可以继续添加其他串口配置
    ]

    threads = []
    start_time = time.time()  # 获取程序开始运行的时间

    # 创建并启动线程
    for config in serial_configs:
        thread = threading.Thread(target=send_data_to_serial, args=(config['port_name'], config['baud_rate'], config['file_name'], config['delay'], start_time))
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
