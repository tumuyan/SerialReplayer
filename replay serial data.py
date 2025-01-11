import serial
import time
import csv
import threading

def send_data_to_serial(port_name, baud_rate, file_name, delay):     
    print(f"{port_name} is waiting to start...")

    # 打开串口
    with serial.Serial(port_name, baud_rate) as ser:
        
        print(f"[{float(time.time()-start_time):.3f}] Open {port_name}, {baud_rate}")
        with open(file_name, mode='r') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # 跳过表头

            start_event.wait()  # 等待事件被设置
            # 等待指定的延迟时间(消除打开io耗用的时间差异)
            time.sleep(float(time.time() - start_time)+ delay /1000)

            # 获取输入和输出缓冲区大小
            output_buffer_size = 512

            for row in csv_reader:
                # 提取时间和数据
                time_ms, hex_data = row
                # 将16进制字符串转换为字节
                byte_data = bytes.fromhex(hex_data)
                time_ms = float(time_ms)
                
                # print(f"时刻{float(time.time() - start_time )*1000} ms, 脚本{time_ms} ms, 延迟 {delay} ms")
                sleep_ms =time_ms + delay - float(time.time() - start_time )*1000 
                if (sleep_ms>0) :
                    # 根据CSV文件中的时间间隔进行等待
                    # print(f"延时{float(sleep_ms) / 1000.0:.3f} s, {sleep_ms} ms")
                    time.sleep(float(sleep_ms) / 1000.0)  # 将毫秒转换为秒
                # 计算当前时间与上一个发送时间的间隔
                elapsed_time = time.time() - start_time
                # 发送数据到串口
                send_length = output_buffer_size
                send_progress = 0
                while send_progress!=len(byte_data):
                    ser.flush()
                    # 还需发送的长度
                    send_length = len(byte_data)-send_progress 
                    if output_buffer_size - ser.out_waiting  < send_length:
                        send_length = output_buffer_size - ser.out_waiting

                    ser.write(byte_data[send_progress:(send_progress + send_length)])
                    # print(f"[{elapsed_time:.2f} seconds]\t{port_name}: {hex_data}")
                    print(f"[{elapsed_time:.3f} s]{port_name}:  {send_length} byte (progress {send_progress}/{len(byte_data)})")
                    send_progress = send_progress + send_length
                
# 创建事件
start_event = threading.Event()
start_time = time.time()  # 获取程序开始运行的时间

def main():
    # 串口参数配置
    serial_configs = [
        {'port_name': 'COM19', 'baud_rate': 38400, 'file_name': 'serial_data_20250111_125038_COM1_38400.csv', 'delay': 505},
        {'port_name': 'COM16', 'baud_rate': 38400, 'file_name': 'serial_data_20250111_125038_COM1_38400.csv', 'delay': 515},
        {'port_name': 'COM21', 'baud_rate': 38400, 'file_name': 'serial_data_20250111_125038_COM1_38400.csv', 'delay': 505},
        # 可以继续添加其他串口配置
    ]

    # 创建多个线程
    threads = []
    global start_time 

    # 创建并启动线程
    for config in serial_configs:
        thread = threading.Thread(target=send_data_to_serial, args=( config['port_name'], config['baud_rate'], config['file_name'], config['delay']))
        threads.append(thread)
        thread.start()
        
    start_time = time.time()  # 获取程序开始运行的时间
    start_event.set()  # 设置事件，允许所有线程开始

    # 等待所有线程完成
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
