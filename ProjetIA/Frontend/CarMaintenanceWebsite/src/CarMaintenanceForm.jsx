import React, { useState } from 'react';
import axios from 'axios';

const CarMaintenanceForm = () => {
  const [mileage, setMileage] = useState('');
  const [dirtyAirFilter, setDirtyAirFilter] = useState(false);
  // Add other state variables for the remaining form fields

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Sent submit")

    try {
      const response = await axios.post('http://127.0.0.1:3000/api/car-maintenance', {
        mileage,
        dirtyAirFilter,
        // Include other form field values in the request body
      });

      console.log(response.data);
      // Handle the response data from the server as desired
    } catch (error) {
      console.error(error);
      // Handle any error that occurred during the request
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Add form input fields for mileage, air filter, tire pressure, etc. */}
      {/* Use appropriate HTML input elements and onChange handlers */}

      <button type="submit">Submit</button>
    </form>
  );
};

export default CarMaintenanceForm;
