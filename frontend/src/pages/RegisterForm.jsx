import React from "react";
import { useEffect,useState } from "react";
import "./Register.css"

function Register(){
    const [latitude,setLatitude]=useState(0)
    const [longitude,setLongitude]=useState(0)
    const [geolocationError,setGeoError]=useState('')
    const [description, setDescription] = useState('');

    const [registrationDetails,setDetails]=useState('');

    


    //function for getting location
    function getLocation(position){
        const latitude= position.coords.latitude;
        const longitude=position.coords.longitude
        setLongitude(longitude);
        setLatitude(latitude);
    }


    //function for location errors
    function showError(error){
        if (error.code === 1) {
            setGeoError("Location access denied.")
        } else if (error.code === 2) {
            setGeoError("Unable to determine your location.")
        } else if (error.code === 3) {
            setGeoError("Location request timed out.")
        }
    }

    //use effect hook for get location o page load
    useEffect(()=>{
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(getLocation, showError);
        } else {
            setGeoError("Geolocation is not supported by this browser.");
        }
    },[])

    //function for making the request to API
    const requestData = {
        accident_latitude: latitude,
        accident_longitude: longitude,
        accident_details: {
            description: description, // Initial empty description
        }
    };

    function requestClosestHospital(){
        console.log(requestData)
        fetch('http://127.0.0.1:8000/api/getHospital', {
            method: 'POST', // Use POST method
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData) // Convert the request data to JSON
        }).then(response=>response.json())
        .then(data=>{
            //console.log(data)
            setDetails(data)
        })
    }


    return(
        <div className="register-form-container">
            <div className="register-heading">
                <h1>Accident and Patient Details</h1>
                <h2>Fill in the details related to the accident here</h2>
            </div>
            <div className="patient-info-panel">
                {registrationDetails!=''?(
                    <div>
                        Patient ID: {registrationDetails.patient_id}<br/>
                        Accident ID : {registrationDetails.accident_id}<br/>
                        Message : {registrationDetails.message}
                    </div>
                ):(
                    <div></div>
                )}
            </div>

            <div className="hospital-info-panel">
                {registrationDetails!=''?(
                    <div>
                        Name: {registrationDetails.hospital.name}<br/>
                        Address: {registrationDetails.hospital.address}<br/>
                        City: {registrationDetails.hospital.city}<br/>
                        State : {registrationDetails.hospital.state}<br/>
                        Pincode: {registrationDetails.hospital.pincode}<br/>
                    </div>
                ):(
                    <div></div>
                )}
            </div>
            <div className="accident-details-textbox">
                <strong>Accident description:</strong>
                <br/>
                <textarea 
                    id="accident-description" 
                    placeholder="Enter accident description here..." 
                    value={description} 
                    onChange={(e) => setDescription(e.target.value)}
                />
            </div>
            {registrationDetails!=''?(
                    <div>
                        department:{registrationDetails.department}
                        <br/>
                    </div>
                    
            ):(
                <div></div>
            )}
            <div className="submit-button" >
                <br/>
                <button id ="submit" onClick={requestClosestHospital}>Submit Accident Details</button>
            </div>
            <div className="GeoLocation">
                {geolocationError!=''?(
                    <p>{geolocationError}</p>
                ):(
                    <p>Latitude:{latitude}     Longitude:{longitude}</p>
                )}
            </div>

        </div>
    )
}


export default Register;