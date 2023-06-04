from experta import *


class CarMaintenanceFact(Fact):
    pass


class CarMaintenanceExpert(KnowledgeEngine):
    @Rule(CarMaintenanceFact(mileage=P(lambda x: x >= 5000)))
    def rule_engine_oil_change(self):
        message = "Rule 1: Schedule an engine oil change."
        return message
    @Rule(AND(
        CarMaintenanceFact(dirty_air_filter=True),
        CarMaintenanceFact(mileage=P(lambda x: x >= 10000))
    ))
    def rule_replace_air_filter(self):
        message = "Rule 2: Replace the air filter."
        return message
    @Rule(CarMaintenanceFact(tire_pressure=P(lambda x: x < 30 or x > 40)))
    def rule_adjust_tire_pressure(self):
        message = "Rule 3: Adjust the tire pressure."
        return message
    @Rule(AND(
        CarMaintenanceFact(rotate_tires=True),
        CarMaintenanceFact(mileage=P(lambda x: x >= 15000))
    ))
    def rule_rotate_tires(self):
        message = "Rule 4: Rotate the tires."
        return message
    @Rule(CarMaintenanceFact(worn_brake_pads=True))
    def rule_replace_brake_pads(self):
        message = "Rule 5: Replace the brake pads."
        return message
    @Rule(CarMaintenanceFact(worn_wiper_blades=True))
    def rule_replace_wiper_blades(self):
        message = "Rule 6: Replace the wiper blades."
        return message
    @Rule(CarMaintenanceFact(corroded_battery=True))
    def rule_clean_battery(self):
        message = "Rule 7: Clean the battery terminals."
        return message
    @Rule(AND(
        CarMaintenanceFact(flush_coolant=True),
        CarMaintenanceFact(mileage=P(lambda x: x >= 50000))
    ))
    def rule_flush_coolant(self):
        message = "Rule 8: Flush and replace the coolant."
        return message
    @Rule(AND(
        CarMaintenanceFact(worn_spark_plugs=True),
        CarMaintenanceFact(mileage=P(lambda x: x >= 60000))
    ))
    def rule_replace_spark_plugs(self):
        message = "Rule 9: Replace the spark plugs."
        return message
    @Rule(CarMaintenanceFact(worn_belts_hoses=True))
    def rule_inspect_belts_hoses(self):
        message = "Rule 10: Inspect belts and hoses."
        return message
    @Rule(AND(
        CarMaintenanceFact(mileage=P(lambda x: x >= 100000)),
        CarMaintenanceFact(worn_belts_hoses=True),
        CarMaintenanceFact(worn_brake_pads=True)
    ))
    def rule_replace_timing_belt(self):
        message = "Rule 11: Replace the timing belt."
        return message
    @Rule(AND(
        CarMaintenanceFact(mileage=P(lambda x: x >= 80000)),
        CarMaintenanceFact(worn_belts_hoses=True)
    ))
    def rule_replace_serpentine_belt(self):
        message = "Rule 12: Replace the serpentine belt."
        return message
    @Rule(AND(
        CarMaintenanceFact(mileage=P(lambda x: x >= 40000)),
        CarMaintenanceFact(dirty_air_filter=True)
    ))
    def rule_clean_mass_air_flow_sensor(self):
        message = "Rule 13: Clean the mass air flow sensor."
        return message
    @Rule(AND(
        CarMaintenanceFact(mileage=P(lambda x: x >= 50000)),
        CarMaintenanceFact(worn_spark_plugs=True)
    ))
    def rule_check_ignition_system(self):
        message = "Rule 14: Check the ignition system."
        return message
    @Rule(AND(
        CarMaintenanceFact(mileage=P(lambda x: x >= 60000)),
        CarMaintenanceFact(flush_coolant=True)
    ))
    def rule_replace_radiator_hoses(self):
        message = "Rule 15: Replace the radiator hoses."
        return message


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
for fact in engine.facts:
    message = engine.run(fact)
    if message:
        print(message)
