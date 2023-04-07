import json
import typing


def get_config() -> dict[str, typing.Any]:
    with open("./config.json", mode="r", encoding="utf-8") as file:
        return json.load(file)
