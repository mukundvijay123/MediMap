import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

function Dashboard() {
  const { hospitalId } = useParams();
  const navigate = useNavigate();
  const [hospitalData, setHospitalData] = useState({
    registered_patients: [],
    unregistered_patients: [],
  });
  const [error, setError] = useState('');
  const [selectedPatient, setSelectedPatient] = useState(null); // To store the patient data for the summary
  const [isSummaryVisible, setSummaryVisible] = useState(false); // To control the visibility of the summary

  // Fetch the hospital data when the component mounts
  useEffect(() => {
    const fetchHospitalData = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/hospital/getDashboardInfo/94/`);
        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }
        const data = await response.json();
        setHospitalData({
          registered_patients: data.registered_patients || [],
          unregistered_patients: data.unregistered_patients || [],
        });
      } catch (error) {
        setError('Error loading data');
      }
    };

    fetchHospitalData();
  }, []);

  // View Patient Summary
  const viewPatientSummary = async (patientId) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/patients/summary/${patientId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch patient summary');
      }
      const patientData = await response.json();
      setSelectedPatient(patientData);
      setSummaryVisible(true); // Show the summary pane
    } catch (error) {
      setError('Error loading patient summary');
    }
  };

  // Close the patient summary modal
  const closeSummary = () => {
    setSummaryVisible(false);
    setSelectedPatient(null); // Reset selected patient data
  };

  // Discharge Patient
  function dischargePatient(patientId) {
    const url = `http://127.0.0.1:8000/api/patients/${patientId}/discharge/`;

    fetch(url, {
      method: 'DELETE', // Use DELETE method to discharge the patient
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
    })
      .then((response) => response.json())
      .then((data) => {
        alert(data.message || 'Patient discharged successfully');
        window.location.reload(); // Optionally, reload the page or remove the row from the table
      })
      .catch((error) => {
        console.error('Error:', error);
        alert('There was an error discharging the patient.');
      });
  }

  // Helper function to get CSRF token from cookies (if using Django with CSRF protection)
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + '=') {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // Register Patient
  const registerPatient = (patientId) => {
    navigate(`/patients/${patientId}`);
  };

  return (
    <div className="container">
      <h1>Hospital Dashboard</h1>

      {/* Registered Patients */}
      <div className="table-container">
        <h2>Registered Patients</h2>
        {hospitalData.registered_patients.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>Patient ID</th>
                <th>Accident ID</th>
                <th>Patient Name</th>
                <th>Gender</th>
                <th>Contact</th>
                <th>Action</th>
                <th>Update</th>
                <th>View</th>
              </tr>
            </thead>
            <tbody>
              {hospitalData.registered_patients.map((patient) => (
                <tr key={patient[0]}>
                  <td>{patient[0]}</td>
                  <td>{patient[1]}</td>
                  <td>{patient[2]}</td>
                  <td>{patient[3]}</td>
                  <td>{patient[4]}</td>
                  <td>
                    <button
                      className="discharge-btn"
                      onClick={() => dischargePatient(patient[0])}
                    >
                      Discharge
                    </button>
                  </td>
                  <td>
                    <button
                      className="update-btn"
                      onClick={() => registerPatient(patient[0])}
                    >
                      Update
                    </button>
                  </td>
                  <td>
                    <button
                      className="view-btn"
                      onClick={() => viewPatientSummary(patient[0])}
                    >
                      View
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p className="no-data">No registered patients found.</p>
        )}
      </div>

      {/* Unregistered Patients */}
      <div className="table-container">
        <h2>Unregistered Patients</h2>
        {hospitalData.unregistered_patients.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>Patient ID</th>
                <th>Accident ID</th>
                <th>Patient Name</th>
                <th>Gender</th>
                <th>Contact</th>
                <th>Action</th>
                <th>View</th>
              </tr>
            </thead>
            <tbody>
              {hospitalData.unregistered_patients.map((patient) => (
                <tr key={patient[0]}>
                  <td>{patient[0]}</td>
                  <td>{patient[1]}</td>
                  <td>{patient[2]}</td>
                  <td>{patient[3]}</td>
                  <td>{patient[4]}</td>
                  <td>
                    <button
                      className="register-btn"
                      onClick={() => registerPatient(patient[0])}
                    >
                      Register
                    </button>
                  </td>
                  <td>
                    <button
                      className="view-btn"
                      onClick={() => viewPatientSummary(patient[0])}
                    >
                      View
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p className="no-data">No unregistered patients found.</p>
        )}
      </div>

      {/* Patient Summary Modal */}
      {isSummaryVisible && selectedPatient && (
        <div className="patient-summary-modal">
          <div className="summary-content">
            <button className="close-btn" onClick={closeSummary}>
              &times; {/* Close button */}
            </button>
            <h2>Patient Summary</h2>
            <div>
              <p><strong>Patient Name:</strong> {selectedPatient.patient_name}</p>
              <p><strong>Gender:</strong> {selectedPatient.gender}</p>
              <p><strong>Blood Group:</strong> {selectedPatient.blood_group}</p>
              <p><strong>Contact:</strong> {selectedPatient.contact}</p>
              <p><strong>Hospital ID:</strong> {selectedPatient.hospital}</p>
              <p><strong>Accident Latitude:</strong> {selectedPatient.accident.accident_latitude}</p>
              <p><strong>Accident Longitude:</strong> {selectedPatient.accident.accident_longitude}</p>
              <p><strong>Accident Details:</strong> {selectedPatient.accident.accident_details.description}</p>
            </div>
          </div>
        </div>
      )}

      {/* Error handling */}
      {error && <p>{error}</p>}
    </div>
  );
}

export default Dashboard;
