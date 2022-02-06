from dataclasses import dataclass
from typing import Union


@dataclass()
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        text = (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )
        return str(text)


@dataclass()
class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    LEN_STEP = 0.65

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Не переопределён метод ' + self.__class__.__name__
            + '.get_spent_calories'
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        info = InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )
        return info


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        COEFF_CALORIES_1 = 18
        COEFF_CALORIES_2 = 20

        duration_in_min = self.duration * 60

        calories = (
            (COEFF_CALORIES_1 * self.get_mean_speed() - COEFF_CALORIES_2)
            * self.weight / self.M_IN_KM * duration_in_min
        )
        return calories


@dataclass()
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    action: int
    duration: float
    weight: float
    height: int

    def __post_init__(self) -> None:
        super().__init__(self.action, self.duration, self.weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        COEFF_CALORIES_1 = 0.035
        COEFF_CALORIES_2 = 0.029

        duration_in_min = self.duration * 60

        calories = (COEFF_CALORIES_1 * self.weight
                    + (self.get_mean_speed() ** 2 // self.height)
                    * COEFF_CALORIES_2 * self.weight) * duration_in_min
        return calories


@dataclass()
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: int

    def __post_init__(self) -> None:
        super().__init__(self.action, self.duration, self.weight)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        speed = (
            self.length_pool * self.count_pool / self.M_IN_KM
            / self.duration
        )
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        COEFF_CALORIES = 1.1

        calories = (self.get_mean_speed() + COEFF_CALORIES) * 2 * self.weight
        return calories


def read_package(workout_type: str, data: list) -> Union[Training, str]:
    """Прочитать данные полученные от датчиков."""

    """
    Словрь состоит из:
    Имя тренировки: Класс тренировки, кол-во принимаемых свойств классом.
    """
    workout_dict = {
        'SWM': [Swimming, 5],
        'RUN': [Running, 3],
        'WLK': [SportsWalking, 4],
    }
    workout_value = workout_dict.get(workout_type)

    """
    Проверка на корректность принимаемых данных.
    """
    if workout_value is None:
        return(f'Неизвестная тренировка: {workout_type}')
    if workout_value[1] != len(data):
        return (f'Для тренировки {workout_type} переданы неверные данные')
    for num in data:
        if not str(num).replace('.', '', 1).isdigit():
            return ('Переданы нечисловые данные')

    workout = workout_value[0](*data)
    return workout


def main(training: Training) -> None:
    """Главная функция."""

    """
    Если аргумент функции строка, значит была ошибка в данных.
    """
    try:
        info = training.show_training_info()
        print(info.get_message())
    except AttributeError:
        print(f'Найдена ошибка в переданных данных: {training}')


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('SWM', [720, 1, 80, 25]),
        ('RUN', [15000, 1, 75]),
        ('RUN', [15000, '1a', 75]),
        ('WLK', [9000, 1, 75, 180]),
        ('WLKM', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
