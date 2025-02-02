import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';  // Import useParams and useNavigate from react-router-dom

function UpdatePatientInfo() {
  // Extract patientID from the URL using useParams hook
  const { patientID } = useParams();

  // Initialize navigate function
  const navigate = useNavigate();

  // State to hold patient information
  const [patientData, setPatientData] = useState({
    patient_name: '',
    gender: '',
    blood_group: '',
    contact: '',
    insurance: '',
  });

  // State for error message
  const [errorMessage, setErrorMessage] = useState('');

  // Fetch patient details when the component mounts or patientId changes
  useEffect(() => {
    // Fetch patient info based on the provided patientId
    fetch(`http://127.0.0.1:8000/api/patients/details/${patientID}`)
      .then((response) => response.json())
      .then((data) => {
        console.log(data)
        setPatientData({
          patient_name: data.patient_name || '',
          gender: data.gender || '',
          blood_group: data.blood_group || '',
          contact: data.contact || '',
          insurance: data.insurance?.id || '',
        });
      })
      .catch((error) => {
        console.error('Error fetching patient data:', error);
        setErrorMessage('Error loading patient data');
      });
  }, []);

  // Function to handle form submission
  const submitPatientUpdate = () => {
    const updateData = {
      patient_name: patientData.patient_name,
      gender: patientData.gender,
      blood_group: patientData.blood_group,
      contact: patientData.contact,
      insurance: patientData.insurance ? parseInt(patientData.insurance) : null,
    };

    fetch(`http://127.0.0.1:8000/api/api/patient/${patientID}/complete_registration/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updateData),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => {
        // Handle successful response
        console.log('Patient updated successfully', data);

        // Option 1: Navigate back to the previous page
        navigate(-1); // This will navigate back to the previous page

        // Option 2: Show a success prompt
        alert('Patient information updated successfully!');
      })
      .catch((error) => {
        console.error('Error updating patient:', error);
        setErrorMessage('An error occurred while updating the patient details.');
      });
  };

  // Handle input change
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setPatientData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  return (
    <div className="container">
      <h1>Update Patient Information</h1>

      <div className="info">
        <strong>Patient ID:</strong> <span>{patientID}</span>
      </div>

      <div className="details">
        
        <br/>
        <div className="textarea-container">
          <label htmlFor="patient-name">Patient Name:</label>
          <input
            type="text"
            id="patient-name"
            name="patient_name"
            value={patientData.patient_name}
            onChange={handleInputChange}
            placeholder="Enter name"
          />

          <label htmlFor="gender">Gender:</label>
          <input
            type="text"
            id="gender"
            name="gender"
            value={patientData.gender}
            onChange={handleInputChange}
            placeholder="Enter gender (optional)"
          />

          <label htmlFor="blood-group">Blood Group:</label>
          <input
            type="text"
            id="blood-group"
            name="blood_group"
            value={patientData.blood_group}
            onChange={handleInputChange}
            placeholder="Enter blood group (optional)"
          />

          <label htmlFor="contact">Contact:</label>
          <input
            type="text"
            id="contact"
            name="contact"
            value={patientData.contact}
            onChange={handleInputChange}
            placeholder="Enter contact number (optional)"
          />

          <label htmlFor="insurance">Insurance ID:</label>
          <input
            type="text"
            id="insurance"
            name="insurance"
            value={patientData.insurance}
            onChange={handleInputChange}
            placeholder="Enter insurance ID (optional)"
          />
        </div>
      </div>

      <button className="submit-button" onClick={submitPatientUpdate}>
        Update Patient Information
      </button>

      {errorMessage && <div className="error-message">{errorMessage}</div>}
    </div>
  );
}

export default UpdatePatientInfo;