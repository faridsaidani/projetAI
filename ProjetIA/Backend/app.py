from flask import Flask, request, jsonify
from experta import *

app = Flask(__name__)

class CarMaintenanceFact(Fact):
    pass

class CarMaintenanceEngine(KnowledgeEngine):
    @Rule(CarMaintenanceFact(mileage=MATCH.mileage & (MATCH.mileage >= 0)))
    def regular_maintenance(self, mileage):
        self.declare(CarMaintenanceFact(message='Regular maintenance is required.'))

    @Rule(CarMaintenanceFact(mileage=MATCH.mileage & (MATCH.mileage >= 5000)))
    def schedule_engine_oil_change(self, mileage):
        self.declare(CarMaintenanceFact(message='Schedule an engine oil change.'))

    @Rule(CarMaintenanceFact(dirty_air_filter=True, mileage=MATCH.mileage & (MATCH.mileage >= 10000)))
    def replace_air_filter(self, mileage):
        self.declare(CarMaintenanceFact(message='Replace the air filter.'))

    @Rule(CarMaintenanceFact(tire_pressure=MATCH.tire_pressure & (MATCH.tire_pressure < 30 or MATCH.tire_pressure > 40)))
    def adjust_tire_pressure(self, tire_pressure):
        self.declare(CarMaintenanceFact(message='Adjust the tire pressure.'))

    @Rule(CarMaintenanceFact(rotate_tires=True, mileage=MATCH.mileage & (MATCH.mileage >= 15000)))
    def rotate_tires(self, mileage):
        self.declare(CarMaintenanceFact(message='Rotate the tires.'))

    @Rule(CarMaintenanceFact(worn_brake_pads=True))
    def replace_brake_pads(self):
        self.declare(CarMaintenanceFact(message='Replace the brake pads.'))

    @Rule(CarMaintenanceFact(worn_wiper_blades=True))
    def replace_wiper_blades(self):
        self.declare(CarMaintenanceFact(message='Replace the wiper blades.'))

    @Rule(CarMaintenanceFact(corroded_battery=True))
    def clean_battery_terminals(self):
        self.declare(CarMaintenanceFact(message='Clean the battery terminals.'))

    @Rule(CarMaintenanceFact(flush_coolant=True, mileage=MATCH.mileage & (MATCH.mileage >= 50000)))
    def flush_and_replace_coolant(self, mileage):
        self.declare(CarMaintenanceFact(message='Flush and replace the coolant.'))

    @Rule(CarMaintenanceFact(worn_spark_plugs=True, mileage=MATCH.mileage & (MATCH.mileage >= 60000)))
    def replace_spark_plugs(self, mileage):
        self.declare(CarMaintenanceFact(message='Replace the spark plugs.'))

    @Rule(CarMaintenanceFact(worn_belts_hoses=True))
    def inspect_belts_and_hoses(self):
        self.declare(CarMaintenanceFact(message='Inspect belts and hoses.'))

@app.route('/api/car-maintenance', methods=['POST'])
def car_maintenance():
    data = request.get_json()
    
    engine = CarMaintenanceEngine()
    engine.reset()
    
    # Extract the mileage from the request payload
    mileage = data.get('mileage', 0)
    
    # Create the initial fact with the mileage
    fact = CarMaintenanceFact(mileage=mileage, **data)
    
    # Run the rules engine
    engine.declare(fact)
    engine.run()
    
    # Retrieve the resulting message from the fact
    message = fact.message
    
    return jsonify({'message': message})

if __name__ == '__main__':
    app.run()
