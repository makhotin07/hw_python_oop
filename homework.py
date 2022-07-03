from dataclasses import dataclass, asdict
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self, message_data: dict):
        message = """Тип тренировки: {training_type};
                Длительность: {duration:.3f} ч.;
                Дистанция: {distance:.3f} км;
                Ср. скорость: {speed:.3f} км/ч;
                Потрачено ккал: {calories:.3f}."""
        message = message.format(**message_data)
        return message


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float
    M_IN_KM: ClassVar[int] = 1000
    LEN_STEP: ClassVar[float] = 0.65
    MIN_IN_H: ClassVar = 60

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
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""

    C_1: ClassVar = 18
    C_2: ClassVar = 20

    def get_spent_calories(self):
        mean_speed = self.get_mean_speed()
        spent_calories = (
            self.C_1 * mean_speed - self.C_2
        ) * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_H
        return spent_calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: float
    STEPEN_2: ClassVar = 2
    C_3: ClassVar = 0.035
    C_4: ClassVar = 0.029

    def __post_init__(self):
        super().__init__(self.action, self.duration, self.weight)

    def get_spent_calories(self):
        mean_speed = self.get_mean_speed()

        spent_calories = (
            self.C_3 * self.weight + (
                mean_speed ** self.STEPEN_2 // self.height
            ) * self.C_4 * self.weight
        ) * self.duration * self.MIN_IN_H
        return spent_calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: int
    count_pool: int
    M_IN_KM: ClassVar[int] = 1000
    LEN_STEP: ClassVar[float] = 1.38
    C_4: ClassVar[float] = 1.1
    C_5: ClassVar[int] = 2

    def __post_init__(self):
        super().__init__(self.action, self.duration, self.weight)

    def get_mean_speed(self):
        mean_spead = (
            self.length_pool * self.count_pool / self.M_IN_KM
        ) / self.duration
        return mean_spead

    def get_spent_calories(self):
        mean_speed = self.get_mean_speed()
        spent_calories = (mean_speed + self.C_4) * self.C_5 * self.weight
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    package_mapping = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking
    }
    instance = package_mapping[workout_type](*data)
    return instance


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    message = info.get_message(asdict(info))
    print(message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
