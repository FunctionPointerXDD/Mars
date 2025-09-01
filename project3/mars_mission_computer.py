### Codyssey Mars project3 ###
### Edit by Mariner_정찬수 ###


import random
import datetime
import json
import time
import platform
import os
import psutil
import threading
from multiprocessing import Process
import multiprocessing as mp
from typing import List, Dict

MARS_ENV = {
   0: "mars_base_internal_temperature",
   1: "mars_base_external_temperature",
   2: "mars_base_internal_humidity",
   3: "mars_base_external_illuminance",
   4: "mars_base_internal_co2",
   5: "mars_base_internal_oxygen"
}

# 스레드 이벤트 객체 (STOP signal 관리용도)
#STOP = threading.Event()

# 프로세스 이벤트 객체 
STOP = mp.Event()

# 0.1초 씩 깨면서 자기..
def light_sleep(sec: int) -> str:
    for _ in range(sec * 10):
        if STOP.is_set():
            return 'STOP'
        time.sleep(0.1)
    return ''

def burn_cpu(sec: int = 2):
    end = time.time() + sec
    x = 0
    while time.time() < end and not STOP.is_set():
        x += sum(i * i for i in range(10000))

class DummySensor:
    def __init__(self):
        self.env_values :dict = {MARS_ENV[i]: 0.0 for i in range(6)}
    
    def set_env(self):
        self.env_values[MARS_ENV[0]] = round(random.uniform(18, 30), 0)
        self.env_values[MARS_ENV[1]] = round(random.uniform(0, 21), 0)
        self.env_values[MARS_ENV[2]] = round(random.uniform(50, 60), 0)
        self.env_values[MARS_ENV[3]] = round(random.uniform(500, 715), 0)
        self.env_values[MARS_ENV[4]] = round(random.uniform(0.02, 0.1), 3)
        self.env_values[MARS_ENV[5]] = round(random.uniform(4, 7), 0)

    def get_env(self):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_fmt = (
            f"{now}, "
            f"내부 온도: {self.env_values[MARS_ENV[0]]}도, "
            f"외부 온도: {self.env_values[MARS_ENV[1]]}도, "
            f"내부 습도: {self.env_values[MARS_ENV[2]]}%, "
            f"외부 광량: {self.env_values[MARS_ENV[3]]}W/m2, "
            f"내부 이산화탄소 농도: {self.env_values[MARS_ENV[4]]}%, "
            f"내부 산소 농도: {self.env_values[MARS_ENV[5]]}%"
        )

        with open('mars_env.log', 'a', encoding='utf-8') as f:
            f.write(log_fmt + '\n')

        return self.env_values


class MissionComputer:
    def __init__(self):
        self.env_values: Dict[str, float] = {}

    def get_sensor_data(self):
        try:
            saved_log :List[Dict[str, float]] = []
            sec = 0
            while not STOP.is_set():
                ds = DummySensor()
                ds.set_env()
                self.env_values = ds.get_env()
                saved_log.append(dict(self.env_values))
                print(json.dumps(self.env_values, indent=4, ensure_ascii=False))

                if light_sleep(5) == 'STOP':
                    break
                sec += 5
                if sec == 300:
                    recs = len(saved_log)
                    avg_fmt = [0.0] * len(MARS_ENV)
                    for i in range(recs):
                        for j in range(len(MARS_ENV)):
                            avg_fmt[j] += saved_log[i][MARS_ENV[j]]

                    avg_env: dict = {}
                    for i in range(len(MARS_ENV)):
                        avg_fmt[i] /= recs
                        avg_env[MARS_ENV[i]] = round(avg_fmt[i], 3)

                    print('\n### AVERAGE ENV INFO IN FIVE MINIUTES ###')
                    print(json.dumps(avg_env, indent=4, ensure_ascii=False))
                    print('#########################################\n')
                    sec = 0
                    saved_log.clear()

        except KeyboardInterrupt:
            print('\nSystem stoped….')
        except Exception as e:
            print(f"[sensor] Error: {e}")
        finally:
            print('[sensor] stop')
    
    def get_mission_computer_info(self):
        try:
            while True:
                info :dict = {}
                info['운영체계'] = platform.system()
                info['운영체계 버전'] = platform.version()
                info['CPU의 타입'] = platform.processor()
                info['CPU의 코어 수'] = os.cpu_count()
                info['메모리의 크기'] = psutil.virtual_memory().total

                print(json.dumps(info, indent=4, ensure_ascii=False))
                if light_sleep(20) == 'STOP':
                    break

        except KeyboardInterrupt:
            print('\nSystem stoped….')
        except Exception as e:
            print(f"Error: {e}")
        finally:
            print('[info] stop')

    def get_mission_computer_load(self):
        try:
            while True:
                load :dict = {}

                _tmp = bytearray(100 * 1024 * 1024) # 100MB
                load['메모리 실시간 사용량'] = psutil.virtual_memory().percent

                psutil.cpu_percent(interval=None)
                t = threading.Thread(target=burn_cpu, args=(2,), daemon=True)
                t.start()
                time.sleep(0.05) # 살짝 지연
                load['CPU 실시간 사용량'] = psutil.cpu_percent(interval=1.0)

                print(json.dumps(load, indent=4, ensure_ascii=False))
                if light_sleep(20) == 'STOP':
                    break

        except KeyboardInterrupt:
            print('\nSystem stoped….')
        except Exception as e:
            print(f"Error: {e}")
        finally:
            print('[load] stop')


# multi-thread simulation ##
def multi_thread():
    try:
        runComputer = MissionComputer()
        t1 = threading.Thread(target=runComputer.get_mission_computer_info)
        t2 = threading.Thread(target=runComputer.get_mission_computer_load)
        t3 = threading.Thread(target=runComputer.get_sensor_data)
        for t in (t1, t2, t3):
            t.start()

        for t in (t1, t2, t3):
            t.join()

    except KeyboardInterrupt:
        print('\nMain Thread stoped by Ctrl + C')
        STOP.set()
        for t in (t1, t2, t3):
            t.join()
    except Exception as e:
        print(f"Error: {e}")
        STOP.set()
        for t in (t1, t2, t3):
            t.join()


## multi-processing simulation ##
def multi_process():
    try:
        runComputer1 = MissionComputer()
        runComputer2 = MissionComputer()
        runComputer3 = MissionComputer()
        p1 = Process(target=runComputer1.get_mission_computer_info)
        p2 = Process(target=runComputer2.get_mission_computer_load)
        p3 = Process(target=runComputer3.get_sensor_data)

        for p in (p1, p2, p3):
            p.start()

        for p in (p1, p2, p3):
            p.join()

    except KeyboardInterrupt:
        print('\nMain Process stoped by Ctrl + C')
        STOP.set()
        for p in (p1, p2, p3):
            p.join()
        for p in (p1, p2, p3):
            if p.is_alive():
                p.terminate()
    except Exception as e:
        print(f"Error: {e}")
        STOP.set()
        for p in (p1, p2, p3):
            p.join()
        for p in (p1, p2, p3):
            if p.is_alive():
                p.terminate()

if __name__ == '__main__':
    # multi_thread()
    multi_process()


## TEST ##
# def main():
#     ds = DummySensor()
#     ds.set_env()
#     print(ds.get_env())
#     RunComputer = MissionComputer()
#     RunComputer.get_sensor_data()
#     runComputer = MissionComputer()
#     runComputer.get_mission_computer_info()
#     runComputer.get_mission_computer_load()
#     runComputer.get_sensor_data()