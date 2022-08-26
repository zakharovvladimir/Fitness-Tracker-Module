from typing import Dict, Type


class InfoMessage:

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:

        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Информационное сообщение о тренировке."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:

    """Базовый класс тренировки."""
    M_IN_KM: int = 1000  # Meters per kilometer
    LEN_STEP: float = 0.65  # One step in meters
    R_COEFF_1: int = 18  # Constant
    R_COEFF_2: int = 20  # Constant
    MINUTES: int = 60  # Minutes per hour

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = ((self.R_COEFF_1 * self.get_mean_speed() - self.R_COEFF_2)
                    * self.weight / self.M_IN_KM * self.duration)
        return calories

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = type(self).__name__
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        message = InfoMessage(training_type, duration, distance, speed,
                              calories)
        return message


class Running(Training):

    """Тренировка: бег."""
    R_COEFF_1: int = 18
    R_COEFF_2: int = 20

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        running_calories = ((self.R_COEFF_1 * self.get_mean_speed()
                            - self.R_COEFF_2) * self.weight / self.M_IN_KM
                            * (self.duration * self.MINUTES))
        return running_calories


class SportsWalking(Training):

    """Тренировка: спортивная ходьба."""
    SW_COEFF_1: float = 0.035
    SW_COEFF_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        sw_calories = ((self.SW_COEFF_1 * self.weight
                        + (self.get_mean_speed() ** 2
                           // self.height) * self.SW_COEFF_2
                       * self.weight) * (self.duration * self.MINUTES))
        return sw_calories


class Swimming(Training):

    """Тренировка: плавание."""
    LEN_STEP = 1.38  # One rowing in meters
    S_COEFF_1 = 1.1  # Constant
    S_COEFF_2 = 2  # Constant

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:

        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        self.swimming_calories = ((self.get_mean_speed() + self.S_COEFF_1)
                                  * self.S_COEFF_2 * self.weight)
        return self.swimming_calories

    def get_mean_speed(self) -> float:
        self.speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return self.speed


def read_package(workout_type: str, data: list) -> Training:

    """Прочитать данные полученные от датчиков."""
    training_dict: Dict[str, Type[Training]]
    training_dict = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }
    if workout_type not in training_dict:
        raise KeyError(f'{workout_type} неизвестна')
    else:
        return training_dict[workout_type](*data)


def main(training: Training) -> InfoMessage:
    """Главная функция."""
    info = Training.show_training_info(training)
    print(InfoMessage.get_message(info))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

