### Codyssey Mars project2 ###
### Edit by Mariner_정찬수 ###

import math

_density: dict = {
    "glass": 2.4 * 1000,
    "aluminum": 2.7 * 1000,
    "carbon_steel": 7.85 * 1000,
}  # g/cm³ → kg/m³
_gravitation: float = 0.38
_surface_area: float = 0
_weight: float = 0


def sphere_area(diameter: float, material: str, thickness: float = 1.0):
    global _surface_area, _weight

    r = diameter / 2
    ri = r - (thickness / 100)
    if ri <= 0:
        raise ValueError("두께가 내부 반지름보다 큽니다!")

    # 반구 표면적
    _surface_area = 3 * math.pi * r * r

    # 반구 무게
    _weight = (2 / 3) * math.pi * (r**3 - ri**3) * _density[material] * _gravitation


def main():
    while True:
        try:
            params = input(
                "지름(m)과 재질(glass/aluminum/carbon_steel)을 입력하세요: "
            ).split()
            if params[0].lower() == "exit":
                return
            diameter = float(params[0])
            if diameter <= 0:
                raise ValueError("지름은 양수여야 합니다.")
            material = params[1].lower()
            if material not in _density:
                raise ValueError("지원하지 않는 재질입니다.")

            sphere_area(diameter, material)

            print(
                f"재질 ⇒ {material}, 지름 ⇒ {diameter:.3f}, 두께 ⇒ 1 cm, 면적 ⇒ {_surface_area:.3f}, 무게 ⇒ {_weight:.3f} kg"
            )

        except ValueError as e:
            print("입력 오류:", e)
        except IndexError:
            print("입력 형식: <지름> <재질>")


if __name__ == "__main__":
    main()
