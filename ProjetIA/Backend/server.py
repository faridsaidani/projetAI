from flask import Flask, jsonify, request
from experta import Rule, Fact, KnowledgeEngine, AS

app = Flask(__name__)

class CarMaintenanceFact(Fact):
    pass

class CarMaintenanceEngine(KnowledgeEngine):
    @Rule(CarMaintenanceFact(mileage=AS.mileage))
    def regular_maintenance(self, mileage):
        if mileage >= 0:
            self.declare(CarMaintenanceFact(message="Regular maintenance is required."))

    @Rule(CarMaintenanceFact(mileage=AS.mileage, dirty_air_filter=True))
    def replace_air_filter(self, mileage):
        if mileage >= 10000:
            self.declare(CarMaintenanceFact(message="Replace the air filter."))

    @Rule(CarMaintenanceFact(mileage=AS.mileage, tire_pressure=(lambda x: x < 30 or x > 40)))
    def adjust_tire_pressure(self, mileage):
        self.declare(CarMaintenanceFact(message="Adjust the tire pressure."))

    @Rule(CarMaintenanceFact(mileage=AS.mileage, rotate_tires=True))
    def rotate_tires(self, mileage):
        if mileage >= 15000:
            self.declare(CarMaintenanceFact(message="Rotate the tires."))

    @Rule(CarMaintenanceFact(worn_brake_pads=True))
    def replace_brake_pads(self):
        self.declare(CarMaintenanceFact(message="Replace the brake pads."))

    @Rule(CarMaintenanceFact(worn_wiper_blades=True))
    def replace_wiper_blades(self):
        self.declare(CarMaintenanceFact(message="Replace the wiper blades."))

    @Rule(CarMaintenanceFact(corroded_battery=True))
    def clean_battery_terminals(self):
        self.declare(CarMaintenanceFact(message="Clean the battery terminals."))

    @Rule(CarMaintenanceFact(mileage=AS.mileage, flush_coolant=True))
    def flush_replace_coolant(self, mileage):
        if mileage >= 50000:
            self.declare(CarMaintenanceFact(message="Flush and replace the coolant."))

    @Rule(CarMaintenanceFact(mileage=AS.mileage, worn_spark_plugs=True))
    def replace_spark_plugs(self, mileage):
        if mileage >= 60000:
            self.declare(CarMaintenanceFact(message="Replace the spark plugs."))

    @Rule(CarMaintenanceFact(worn_belts_hoses=True))
    def inspect_belts_hoses(self):
        self.declare(CarMaintenanceFact(message="Inspect belts and hoses."))

# Create an instance of the knowledge engine
engine = CarMaintenanceEngine()

@app.route('/api/car-maintenance', methods=['POST'])
def car_maintenance():
    data = request.json

    # Extract the parameters from the request body
    mileage = data.get('mileage', 0)
    dirty_air_filter = data.get('dirty_air_filter', False)
    tire_pressure = data.get('tire_pressure', 0)
    rotate_tires = data.get('rotate_tires', False)
    worn_brake_pads = data.get('worn_brake_pads', False)
    worn_wiper_blades = data.get('worn_wiper_blades', False)
    corroded_battery = data.get('corroded_battery', False)
    flush_coolant = data.get('flush_coolant', False)
    worn_spark_plugs = data.get('worn_spark_plugs', False)
    worn_belts_hoses = data.get('worn_belts_hoses', False)

    # Reset the engine's facts
    engine.reset()

    # Add the CarMaintenanceFact to the engine's knowledge base
    engine.declare(CarMaintenanceFact(
        mileage=mileage,
        dirty_air_filter=dirty_air_filter,
        tire_pressure=tire_pressure,
        rotate_tires=rotate_tires,
        worn_brake_pads=worn_brake_pads,
        worn_wiper_blades=worn_wiper_blades,
        corroded_battery=corroded_battery,
        flush_coolant=flush_coolant,
        worn_spark_plugs=worn_spark_plugs,
        worn_belts_hoses=worn_belts_hoses
    ))

    # Run the engine
    engine.run()

    # Retrieve the CarMaintenanceFact with updated message
    fact = next(fact for fact in engine.facts if isinstance(fact, CarMaintenanceFact))

    # Return the message as a JSON response
    response = {'message': fact.message}
    return jsonify(response)

if __name__ == '__main__':
    app.run()
