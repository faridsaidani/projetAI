const express = require('express');
const bodyParser = require('body-parser');
const nools = require('nools');

// Create an instance of Express
const app = express();

// Configure body-parser middleware to parse request bodies
app.use(bodyParser.json());

// Define the CarMaintenanceFact class
const CarMaintenanceFact = function (mileage, dirty_air_filter, tire_pressure, rotate_tires,
  worn_brake_pads, worn_wiper_blades, corroded_battery, flush_coolant, worn_spark_plugs,
  worn_belts_hoses, message) {
  this.mileage = mileage;
  this.dirty_air_filter = dirty_air_filter;
  this.tire_pressure = tire_pressure;
  this.rotate_tires = rotate_tires;
  this.worn_brake_pads = worn_brake_pads;
  this.worn_wiper_blades = worn_wiper_blades;
  this.corroded_battery = corroded_battery;
  this.flush_coolant = flush_coolant;
  this.worn_spark_plugs = worn_spark_plugs;
  this.worn_belts_hoses = worn_belts_hoses;
  this.message = message;
};

// Define the POST endpoint for car maintenance
app.post('/api/car-maintenance', (req, res) => {
  const { mileage, dirty_air_filter, tire_pressure, rotate_tires, worn_brake_pads,
    worn_wiper_blades, corroded_battery, flush_coolant, worn_spark_plugs,
    worn_belts_hoses } = req.body;

  // Define the Nools rules script
  const ruleScript = `
    define CarMaintenanceFact {
      mileage: 0,
      dirty_air_filter: false,
      tire_pressure: 0,
      rotate_tires: false,
      worn_brake_pads: false,
      worn_wiper_blades: false,
      corroded_battery: false,
      flush_coolant: false,
      worn_spark_plugs: false,
      worn_belts_hoses: false,
      message: ""
    }

    rule RegularMaintenance {
      when
        $c: CarMaintenanceFact { mileage >= 0 }
      then
        $c.message = "Regular maintenance is required.";
    }

    rule ScheduleEngineOilChange {
      when
        $c: CarMaintenanceFact { mileage >= 5000 }
      then
        $c.message = "Schedule an engine oil change.";
    }

    rule ReplaceAirFilter {
      when
        $c: CarMaintenanceFact { dirty_air_filter == true, mileage >= 10000 }
      then
        $c.message = "Replace the air filter.";
    }

    rule AdjustTirePressure {
      when
        $c: CarMaintenanceFact { tire_pressure < 30 || tire_pressure > 40 }
      then
        $c.message = "Adjust the tire pressure.";
    }

    rule RotateTires {
      when
        $c: CarMaintenanceFact { rotate_tires == true, mileage >= 15000 }
      then
        $c.message = "Rotate the tires.";
    }

    rule ReplaceBrakePads {
      when
        $c: CarMaintenanceFact { worn_brake_pads == true }
      then
        $c.message = "Replace the brake pads.";
    }

    rule ReplaceWiperBlades {
      when
        $c: CarMaintenanceFact { worn_wiper_blades == true }
      then
        $c.message = "Replace the wiper blades.";
    }

    rule CleanBatteryTerminals {
      when
        $c: CarMaintenanceFact { corroded_battery == true }
      then
        $c.message = "Clean the battery terminals.";
    }

    rule FlushAndReplaceCoolant {
      when
        $c: CarMaintenanceFact { flush_coolant == true, mileage >= 50000 }
      then
        $c.message = "Flush and replace the coolant.";
    }

    rule ReplaceSparkPlugs {
      when
        $c: CarMaintenanceFact { worn_spark_plugs == true, mileage >= 60000 }
      then
        $c.message = "Replace the spark plugs.";
    }

    rule InspectBeltsAndHoses {
      when
        $c: CarMaintenanceFact { worn_belts_hoses == true }
      then
        $c.message = "Inspect belts and hoses.";
    }
  `;

  // Create a Nools flow and define the rules
  const flow = nools.compile(ruleScript);
  const CarMaintenanceRule = flow.getDefined('CarMaintenanceFact');

  // Create an instance of CarMaintenanceFact
  const carMaintenanceFact = new CarMaintenanceRule(
    mileage, dirty_air_filter, tire_pressure, rotate_tires, worn_brake_pads,
    worn_wiper_blades, corroded_battery, flush_coolant, worn_spark_plugs,
    worn_belts_hoses, ""
  );

  // Run the Nools flow
  flow.getSession(carMaintenanceFact).match(() => {
    res.json({ message: carMaintenanceFact.message });
  });
});

// Start the server
const port = 3000;
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
