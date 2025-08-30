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
from typing import List, Dict

MARS_ENV = {
   0: "mars_base_internal_temperature",
   1: "mars_base_external_temperature",
   2: "mars_base_internal_humidity",
   3: "mars_base_external_illuminance",
   4: "mars_base_internal_co2",
   5: "mars_base_internal_oxygen"
}

def burn_cpu(sec: int):
    end = time.time() + sec
    x = 0
    while time.time() < end:
        x += sum(i * i for i in range(10000))

class DummySensor:
    def __init__(self):
        self.env_values = {
            MARS_ENV[0] : 0.0,
            MARS_ENV[1] : 0.0,
            MARS_ENV[2] : 0.0,
            MARS_ENV[3] : 0.0,
            MARS_ENV[4] : 0.0,
            MARS_ENV[5] : 0.0,
        }
    
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
            avg_fmt = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            sec = 0
            while True:
                ds = DummySensor()
                ds.set_env()
                self.env_values = ds.get_env()
                saved_log.append(self.env_values)
                print(json.dumps(self.env_values, indent=4, ensure_ascii=False))

                time.sleep(5.0)
                sec += 5
                if sec == 300:
                    recs = len(saved_log)
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
    
    def get_mission_computer_info(self):
        try:
            info :dict = {}
            info['운영체계'] = platform.system()
            info['운영체계 버전'] = platform.version()
            info['CPU의 타입'] = platform.processor()
            info['CPU의 코어 수'] = os.cpu_count()
            info['메모리의 크기'] = psutil.virtual_memory().total

            print(json.dumps(info, indent=4, ensure_ascii=False))
        except Exception as e:
            print(f"Error: {e}")

    def get_mission_computer_load(self):
        try:
            load :dict = {}

            _tmp = [0] * (10 ** 8) # 메모리 사용량 올리기
            load['메모리 실시간 사용량'] = psutil.virtual_memory().percent

            psutil.cpu_percent(interval=None)
            t = threading.Thread(target=burn_cpu, args=(2,), daemon=True)
            t.start()
            load['CPU 실시간 사용량'] = psutil.cpu_percent(interval=1)
            t.join()

            print(json.dumps(load, indent=4, ensure_ascii=False))
        except Exception as e:
            print(f"Error: {e}")


def main():
    # ds = DummySensor()
    # ds.set_env()
    # print(ds.get_env())
    # RunComputer = MissionComputer()
    # RunComputer.get_sensor_data()
    runComputer = MissionComputer()
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()


if __name__ == '__main__':
    main()
