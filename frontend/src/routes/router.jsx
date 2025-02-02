import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Register from '../pages/RegisterForm.jsx';
import HospitalLogin from '../pages/hospitalLogin.jsx';
import Dashboard from '../pages/dashboard.jsx';
import UpdatePatientInfo from '../pages/registerPatient.jsx';

function AppRouter(){
    return(
        <Routes>
            <Route path="/register" element={<Register/>}/>
            <Route path='/dashboardLogin' element={<HospitalLogin/>}/>
            <Route path='/dashboard/:hospitalID'  element={<Dashboard/>}/>
            <Route path='/patients/:patientID' element={<UpdatePatientInfo/>}/>
        </Routes>
    )
}

export default AppRouter;