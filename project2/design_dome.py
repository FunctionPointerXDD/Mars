# 반구체 돔의 표면적과 무게를 계산하는 함수 sphere_area()를 정의한다.
# 함수는 다음 파라미터를 가진다:
# diameter (단위: m)
# material: 유리(glass), 알루미늄(aluminum), 탄소강(carbon_steel)
# thickness: 기본값 1cm
# 지름과 재질은 input()을 통해 사용자로부터 입력받는다.
# 재질의 밀도 (g/cm³)
# 유리: 2.4
# 알루미늄: 2.7
# 탄소강: 7.85
# 결과 출력 시:
# 면적은 소수점 3자리까지
# 무게는 **화성 중력(지구 중력의 약 0.38배)**을 반영하여 출력
# 전역 변수 저장 및 다음 형식으로 출력:
# 재질 ⇒ 유리, 지름 ⇒ 10, 두께 ⇒ 1, 면적 ⇒ 314.159, 무게 ⇒ 500.987 kg
# 프로그램은 반복 실행되어야 하며, 종료 조건도 구현되어야 한다.
# 잘못된 입력(예: 지름이 0이거나 숫자가 아님)에 대해 예외 처리가 되어 있어야 한다.

import math


# g/cm³ → kg/m³
g_density: dict = {'glass': 2.4 * 1000, 'aluminum': 2.7 * 1000, 'carbon_steel': 7.85 * 1000}
g_gravitation: float = 0.38
g_surface_area: float = 0
g_weight: float = 0

def sphere_area(diameter: float, material: str, thickness: float = 1.0):
    global g_surface_area, g_weight

    r = diameter / 2
    ri = r - (thickness / 100)
    if ri <= 0:
        raise ValueError("두께가 내부 반지름보다 큽니다!")

    #반구 표면적
    g_surface_area = 3 * math.pi * r * r

    #반구 무게
    g_weight = (2 / 3) * math.pi * (r**3 - ri**3) * g_density[material] * g_gravitation


def main():
    while True:
        try:
            params = input('지름(m)과 재질(glass/aluminum/carbon_steel)을 입력하세요: ').split()
            if params[0].lower() == 'exit':
                return
            diameter = float(params[0])
            if diameter <= 0:
                raise ValueError("지름은 양수여야 합니다.")
            material = params[1].lower()
            if material not in g_density:
                raise ValueError("지원하지 않는 재질입니다.")

            sphere_area(diameter, material)

            print(f'재질 ⇒ {material}, 지름 ⇒ {diameter:.3f}, 두께 ⇒ 1 cm, 면적 ⇒ {g_surface_area:.3f}, 무게 ⇒ {g_weight:.3f} kg')

        except ValueError as e:
            print("입력 오류:", e)
        except IndexError:
            print("입력 형식: <지름> <재질>")

if __name__ == '__main__':
    main()
