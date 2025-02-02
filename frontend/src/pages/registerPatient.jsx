import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

function UpdatePatientInfo() {
  const { patientID } = useParams();
  const navigate = useNavigate();

  const [patientData, setPatientData] = useState({
    patient_name: '',
    gender: '',
    blood_group: '',
    contact: '',
    insurance: '',
  });

  const [errors, setErrors] = useState({});

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/patients/details/${patientID}`)
      .then((response) => response.json())
      .then((data) => {
        setPatientData({
          patient_name: data.patient_name || '',
          gender: data.gender || '',
          blood_group: data.blood_group || '',
          contact: data.contact || '',
          insurance: data.insurance?.id || '',
        });
      })
      .catch(() => {
        setErrors((prev) => ({ ...prev, fetchError: 'Error loading patient data' }));
      });
  }, [patientID]);

  // Gender and Blood Group Options
  const genderOptions = ['Male', 'Female', 'Other'];
  const bloodGroupOptions = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'];

  // Validation function
  const validate = () => {
    let validationErrors = {};

    if (!patientData.patient_name.trim()) validationErrors.patient_name = 'Name is required.';
    if (!patientData.gender) validationErrors.gender = 'Gender is required.';
    if (!patientData.blood_group) validationErrors.blood_group = 'Blood Group is required.';
    if (!patientData.contact.match(/^\d{10}$/)) validationErrors.contact = 'Enter a valid 10-digit contact number.';

    setErrors(validationErrors);
    return Object.keys(validationErrors).length === 0;
  };

  const submitPatientUpdate = () => {
    if (!validate()) return;

    const updateData = {
      patient_name: patientData.patient_name,
      gender: patientData.gender,
      blood_group: patientData.blood_group,
      contact: patientData.contact,
      insurance: patientData.insurance ? parseInt(patientData.insurance) : null,
    };

    fetch(`http://127.0.0.1:8000/api/api/patient/${patientID}/complete_registration/`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updateData),
    })
      .then((response) => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
      })
      .then(() => {
        alert('Patient information updated successfully!');
        navigate(-1);
      })
      .catch(() => setErrors((prev) => ({ ...prev, updateError: 'Error updating patient details.' })));
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setPatientData((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <div className="container">
      <h1>Update Patient Information</h1>

      {errors.fetchError && <div className="error-message">{errors.fetchError}</div>}

      <div className="details">
        <label>Patient Name:</label>
        <input type="text" name="patient_name" value={patientData.patient_name} onChange={handleInputChange} />
        {errors.patient_name && <div className="error-message">{errors.patient_name}</div>}

        <label>Gender:</label>
        <select name="gender" value={patientData.gender} onChange={handleInputChange}>
          <option value="">Select Gender</option>
          {genderOptions.map((g) => (
            <option key={g} value={g}>{g}</option>
          ))}
        </select>
        {errors.gender && <div className="error-message">{errors.gender}</div>}

        <label>Blood Group:</label>
        <select name="blood_group" value={patientData.blood_group} onChange={handleInputChange}>
          <option value="">Select Blood Group</option>
          {bloodGroupOptions.map((bg) => (
            <option key={bg} value={bg}>{bg}</option>
          ))}
        </select>
        {errors.blood_group && <div className="error-message">{errors.blood_group}</div>}

        <label>Contact:</label>
        <input type="text" name="contact" value={patientData.contact} onChange={handleInputChange} />
        {errors.contact && <div className="error-message">{errors.contact}</div>}

        <label>Insurance ID:</label>
        <input type="text" name="insurance" value={patientData.insurance} onChange={handleInputChange} />
      </div>

      <button className="submit-button" onClick={submitPatientUpdate}>Update Patient Information</button>
      {errors.updateError && <div className="error-message">{errors.updateError}</div>}
    </div>
  );
}

export default UpdatePatientInfo;
