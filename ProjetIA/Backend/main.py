from experta import *


class CarMaintenanceFact(Fact):
    pass


class CarMaintenanceExpert(KnowledgeEngine):
    @Rule(CarMaintenanceFact(mileage=P(lambda x: x >= 5000)))
    def rule_engine_oil_change(self):
        print("Rule 1: Schedule an engine oil change.")

    @Rule(CarMaintenanceFact(dirty_air_filter=True))
    def rule_air_filter_replace(self):
        print("Rule 2: Replace the air filter.")

    @Rule(CarMaintenanceFact(tire_pressure=P(lambda x: x < 30 or x > 40)))
    def rule_adjust_tire_pressure(self):
        print("Rule 3: Adjust the tire pressure.")

    @Rule(CarMaintenanceFact(rotate_tires=True))
    def rule_rotate_tires(self):
        print("Rule 4: Rotate the tires.")

    @Rule(CarMaintenanceFact(worn_brake_pads=True))
    def rule_replace_brake_pads(self):
        print("Rule 5: Replace the brake pads.")

    @Rule(CarMaintenanceFact(worn_wiper_blades=True))
    def rule_replace_wiper_blades(self):
        print("Rule 6: Replace the wiper blades.")

    @Rule(CarMaintenanceFact(corroded_battery=True))
    def rule_clean_battery(self):
        print("Rule 7: Clean the battery terminals.")

    @Rule(CarMaintenanceFact(flush_coolant=True))
    def rule_flush_coolant(self):
        print("Rule 8: Flush and replace the coolant.")

    @Rule(CarMaintenanceFact(worn_spark_plugs=True))
    def rule_replace_spark_plugs(self):
        print("Rule 9: Replace the spark plugs.")

    @Rule(CarMaintenanceFact(worn_belts_hoses=True))
    def rule_inspect_belts_hoses(self):
        print("Rule 10: Inspect belts and hoses.")


# Usage Example:
engine = CarMaintenanceExpert()

# Set the facts based on the car's condition
engine.declare(CarMaintenanceFact(mileage=6000))
engine.declare(CarMaintenanceFact(dirty_air_filter=True))
engine.declare(CarMaintenanceFact(tire_pressure=35))
engine.declare(CarMaintenanceFact(rotate_tires=True))
engine.declare(CarMaintenanceFact(worn_brake_pads=True))
engine.declare(CarMaintenanceFact(worn_wiper_blades=True))
engine.declare(CarMaintenanceFact(corroded_battery=True))
engine.declare(CarMaintenanceFact(flush_coolant=True))
engine.declare(CarMaintenanceFact(worn_spark_plugs=True))
engine.declare(CarMaintenanceFact(worn_belts_hoses=True))

# Run the expert system
engine.run()
