from dataclasses import dataclass, asdict
from typing import ClassVar, Sequence, Union


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    MESSAGE: ClassVar[str] = ('Тип тренировки: {training_type}; '
                              'Длительность: {duration:.3f} ч.; '
                              'Дистанция: {distance:.3f} км; '
                              'Ср. скорость: {speed:.3f} км/ч; '
                              'Потрачено ккал: {calories:.3f}.')
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(f'В классе {self.__class__.__name__}',
                                  'этот метод не определен')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIES_1: int = 18
    COEFF_CALORIES_2: int = 20

    def get_spent_calories(self) -> float:
        """Получаем количетво затраченных калорий."""
        return((self.COEFF_CALORIES_1 * self.get_mean_speed()
               - self.COEFF_CALORIES_2) * self.weight / self.M_IN_KM
               * (self.MIN_IN_HOUR * self.duration))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_1: float = 0.035
    COEFF_2: int = 2
    COEFF_3: float = 0.029

    def get_spent_calories(self) -> float:
        """Получаем количетво затраченных калорий."""
        return(((self.COEFF_1 * self.weight) + (self.get_mean_speed()
               ** self.COEFF_2 // self.height)
               * (self.COEFF_3 * self.weight))
               * self.MIN_IN_HOUR * self.duration)

    def __init__(self, action: int, duration: float, weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_4: float = 1.1
    COEFF_5: int = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получаем средную скорость плавания."""
        return(self.length_pool * self.count_pool
               / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получаем количетво затраченных калорий."""
        return((self.get_mean_speed() + self.COEFF_4)
               * self.COEFF_5 * self.weight)

    def get_distance(self) -> float:
        """Получаем дистанцию"""
        return self.action * self.LEN_STEP / self.M_IN_KM


def read_package(workout_type: str,
                 data: Sequence[Union[int, float]]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_dict = {
        'SWM': Swimming,
        'WLK': SportsWalking,
        'RUN': Running
    }
    try:
        return workout_type_dict.get(workout_type)(*data)
    except KeyError:
        raise('Такой тренировки нет!')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)