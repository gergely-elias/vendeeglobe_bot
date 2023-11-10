# SPDX-License-Identifier: BSD-3-Clause

# flake8: noqa F401

import numpy as np

from vendeeglobe import (
    Checkpoint,
    Heading,
    Instructions,
    Location,
    MapProxy,
    Vector,
    WeatherForecast,
    config,
)
from vendeeglobe.utils import distance_on_surface

CREATOR = "GhostOfMagellan"  # This is your team name


class Bot:
    """
    This is the ship-controlling bot that will be instantiated for the competition.
    """

    def __init__(self):
        self.team = CREATOR  # Mandatory attribute
        self.avatar = 7  # Optional attribute
        self.course = [
            Checkpoint(latitude=18.37741, longitude=-67.93669, radius=50), # Puerto Rico W
            Checkpoint(latitude=9.37652, longitude=-80.26767, radius=50), # Panama N
            Checkpoint(latitude=5.61982, longitude=-78.74151, radius=50), # Panama S
            Checkpoint(latitude=-15.306318, longitude=-173.943864, radius=50.0), # touching CP1
            Checkpoint(latitude=-45.052286, longitude=160.214572, radius=50.0), # Tasman Sea
            Checkpoint(latitude=13.534129, longitude=50.536723, radius=50.0), # Aden bay E
            Checkpoint(latitude=11.095481, longitude=43.908339, radius=50.0), # Aden bay W
            Checkpoint(latitude=29.566223, longitude=32.553761, radius=5.0), # Suez canal S
            Checkpoint(latitude=32.110623, longitude=32.414745, radius=5.0), # Suez canal N
            Checkpoint(latitude=37.205814, longitude=10.934190, radius=20.0), # Tunisia NE
            Checkpoint(latitude=38.234707, longitude=6.115484, radius=20.0), # Sardinia SW
            Checkpoint(latitude=35.927345, longitude=-5.169988, radius=5.0), # Gibraltar E
            Checkpoint(latitude=37.033570, longitude=-10.109006, radius=50.0), # Portugal SW
            Checkpoint(latitude=43.786129, longitude=-9.513288, radius=50.0), # Spain NW
            Checkpoint(
                latitude=config.start.latitude,
                longitude=config.start.longitude,
                radius=5,
            ),
        ]

    def run(
        self,
        t: float,
        dt: float,
        longitude: float,
        latitude: float,
        heading: float,
        speed: float,
        vector: np.ndarray,
        forecast: WeatherForecast,
        world_map: MapProxy,
    ):
        """
        This is the method that will be called at every time step to get the
        instructions for the ship.

        Parameters
        ----------
        t:
            The current time in hours.
        dt:
            The time step in hours.
        longitude:
            The current longitude of the ship.
        latitude:
            The current latitude of the ship.
        heading:
            The current heading of the ship.
        speed:
            The current speed of the ship.
        vector:
            The current heading of the ship, expressed as a vector.
        forecast:
            The weather forecast for the next 5 days.
        world_map:
            The map of the world: 1 for sea, 0 for land.
        """
        instructions = Instructions()
        for ch in self.course:
            dist = distance_on_surface(
                longitude1=longitude,
                latitude1=latitude,
                longitude2=ch.longitude,
                latitude2=ch.latitude,
            )
            jump = dt * np.linalg.norm(speed)
            if dist < 2.0 * ch.radius + jump:
                instructions.sail = min(ch.radius / jump, 1)
            else:
                instructions.sail = 1.0
            if dist < ch.radius:
                ch.reached = True
            if not ch.reached:
                instructions.location = Location(
                    longitude=ch.longitude, latitude=ch.latitude
                )
                break

        return instructions
