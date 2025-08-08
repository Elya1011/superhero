import requests
from typing import Literal


def get_the_tallest_hero(gender: Literal['Male', 'Female', '-'], work: bool) -> str:
    valid_genders = {'Male', 'Female', '-'}
    if gender not in valid_genders:
        raise ValueError(f"Invalid gender. Use: {', '.join(valid_genders)}")
    if not isinstance(work, bool):
        raise TypeError('work must be a boolean value: True or False')
    max_height = 0
    the_tallest_hero = ''
    url = 'https://akabab.github.io/superhero-api/api/all.json'
    response = requests.get(url)
    heroes = response.json()
    for hero in heroes:
        if (hero['appearance']['gender'] == gender and
                (work == False and hero['work']['occupation'] == '-' or
                 work == True and hero['work']['occupation'] != '-')):

            if 'meters' in hero['appearance']['height'][-1]:
                height_cm = int(float(hero['appearance']['height'][-1].split()[0]) * 100)
            else:
                height_cm = int(hero['appearance']['height'][-1].split()[0])

            if height_cm > max_height:
                max_height = height_cm
                the_tallest_hero = hero['name']
    return the_tallest_hero


# при запуске тестов лучше закомитить строки ниже, т.к. покрытие тестов падает со 100% до 79%
if __name__ == "__main__":
    print(get_the_tallest_hero('Female', False))
    print(get_the_tallest_hero('Male', False))
    print(get_the_tallest_hero('-', False))
    print(get_the_tallest_hero('Female', True))
    print(get_the_tallest_hero('Male', True))
    print(get_the_tallest_hero('-', True))