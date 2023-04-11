from re import compile
from typing import Any, Optional

from crenata.discord.embed import parse_br_tag
from discord import SelectOption

ALLERGY_CODES = {  # 1자릿수를 먼저 하면 1n을 파싱할 때 1로 인식함
    "10": "돼지고기",
    "11": "복숭아",
    "12": "토마토",
    "13": "아황산류",
    "14": "호두",
    "15": "닭고기",
    "16": "쇠고기",
    "17": "오징어",
    "18": "조개류",
    "19": "잣",
    "1": "난류",
    "2": "우유",
    "3": "메밀",
    "4": "땅콩",
    "5": "대두",
    "6": "밀",
    "7": "고등어",
    "8": "게",
    "9": "새우",
}
ALLERGY_REGEX = compile(r"(\((\d{1,2}\.)+\))$")


def allergic_select_option(data: Optional[list[Any]]) -> list[SelectOption]:
    """
    알러지 정보 표시를 위한 SelectOption을 만듭니다.
    """
    if not data:
        return []

    r = data[0]
    options: list[SelectOption] = []
    dishes = parse_br_tag(r.DDISH_NM).splitlines()

    for dish in dishes:
        if matches := ALLERGY_REGEX.search(dish):
            allergies = matches[0].replace("(", "").replace(")", "")

            for k, v in ALLERGY_CODES.items():
                allergies = allergies.replace(k + ".", v + ", ")

            allergies = allergies[:-2]
        else:
            allergies = "정보 없음"

        options.append(
            SelectOption(label=ALLERGY_REGEX.sub("", dish), description=allergies)
        )

    return options
