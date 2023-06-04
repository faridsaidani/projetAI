from experta import *

class CarMaintenanceFact(Fact):
    """Car maintenance fact."""
    pass

class RegularMaintenance(KnowledgeEngine):
    @Rule(CarMaintenanceFact(mileage='mileage' & (mileage >= 0)))
    def regular_maintenance(self):
        self.declare(CarMaintenanceFact(message="Regular maintenance is required."))

class ScheduleEngineOilChange(KnowledgeEngine):
    @Rule(CarMaintenanceFact(mileage='mileage' & (mileage >= 5000)))
    def schedule_engine_oil_change(self):
        self.declare(CarMaintenanceFact(message="Schedule an engine oil change."))

class ReplaceAirFilter(KnowledgeEngine):
    @Rule(CarMaintenanceFact(dirty_air_filter=True, mileage='mileage' & (mileage >= 10000)))
    def replace_air_filter(self):
        self.declare(CarMaintenanceFact(message="Replace the air filter."))

class AdjustTirePressure(KnowledgeEngine):
    @Rule(CarMaintenanceFact(tire_pressure='tire_pressure' & (tire_pressure < 30 or tire_pressure > 40)))
    def adjust_tire_pressure(self):
        self.declare(CarMaintenanceFact(message="Adjust the tire pressure."))

class RotateTires(KnowledgeEngine):
    @Rule(CarMaintenanceFact(rotate_tires=True, mileage='mileage' & (mileage >= 15000)))
    def rotate_tires(self):
        self.declare(CarMaintenanceFact(message="Rotate the tires."))

# Add more rules for other maintenance tasks

engine = KnowledgeEngine()
engine.reset()

engine.declare(CarMaintenanceFact(mileage=8000, dirty_air_filter=True, tire_pressure=35, rotate_tires=True))

engine.run()

# Access the result message
result = engine.facts[-1].message
print(result)