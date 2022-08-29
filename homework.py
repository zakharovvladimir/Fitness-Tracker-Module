from typing import Dict, Type, ClassVar
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    """Информационное сообщение о тренировке."""
    MESSAGE: ClassVar[str] = ('Тип тренировки: {training_type}; '
                              'Длительность: {duration:.3f} ч.; '
                              'Дистанция: {distance:.3f} км; '
                              'Ср. скорость: {speed:.3f} км/ч; '
                              'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    M_IN_KM: ClassVar[int] = 1000
    LEN_STEP: ClassVar[float] = 0.65  # For the purpose of converting to meters
    MINUTES_IN_HOUR: ClassVar[int] = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""

    MEAN_SPEED_RUN_MULTIPLIER_1: ClassVar[int] = 18
    MEAN_SPEED_RUN_MULTIPLIER_2: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        running_calories = ((self.MEAN_SPEED_RUN_MULTIPLIER_1
                            * self.get_mean_speed()
                            - self.MEAN_SPEED_RUN_MULTIPLIER_2)
                            * self.weight / self.M_IN_KM
                            * (self.duration * self.MINUTES_IN_HOUR))
        return running_calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    MEAN_SPEED_WALK_MULTIPLIER_1: ClassVar[float] = 0.035
    MEAN_SPEED_WALK_MULTIPLIER_2: ClassVar[float] = 0.029

    action: int
    duration: float
    weight: float
    height: float

    def get_spent_calories(self) -> float:
        sw_calories = ((self.MEAN_SPEED_WALK_MULTIPLIER_1 * self.weight
                        + (self.get_mean_speed() ** 2
                           // self.height) * self.MEAN_SPEED_WALK_MULTIPLIER_2
                       * self.weight) * (self.duration * self.MINUTES_IN_HOUR))
        return sw_calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: ClassVar[float] = 1.38  # For the purpose of converting to meters
    MEAN_SPEED_SWIM_MULTIPLIER_1: ClassVar[float] = 1.1
    MEAN_SPEED_SWIM_MULTIPLIER_2: ClassVar[int] = 2

    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: float

    def get_spent_calories(self) -> float:
        self.swimming_calories = ((self.get_mean_speed()
                                  + self.MEAN_SPEED_SWIM_MULTIPLIER_1)
                                  * self.MEAN_SPEED_SWIM_MULTIPLIER_2
                                  * self.weight)
        return self.swimming_calories

    def get_mean_speed(self) -> float:
        self.speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return self.speed


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict: Dict[str, Type[Training]] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }
    if workout_type not in training_dict:
        raise KeyError(f'{workout_type} неизвестна')
    return training_dict[workout_type](*data)


def main(training: Training) -> InfoMessage:
    """Главная функция."""
    print(InfoMessage.get_message(Training.show_training_info(training)))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
