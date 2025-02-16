import React from "react";
import { useState,useEffect } from "react";
import {useNavigate} from "react-router-dom";


function HospitalLogin(){

    const [hospitalID,setID]=useState('')
    const [IdErrors,setErrors]=useState('')
    const navigate = useNavigate();


    function isNumeric(str){
        return /^[0-9]+$/.test(str);
    }

    useEffect(()=>{
        console.log(hospitalID)
        if(hospitalID===''){
            setErrors(('Hospital ID s required'))
        }else if(!isNumeric(hospitalID)){
            setErrors('Please enter a valid numeric hospital ID.')
        }else(
            setErrors('')
        )
    },[hospitalID])

    function redirectDashboard(){
        if(isNumeric(hospitalID)){
            navigate(`/dashboard/${hospitalID}`)
        }else{
            window.alert("The ID can only consist of numeric characters")
        }
    }


    return(
        <div className="hospital-login">
            <div className="heading">
                <h1>Login to hospital dashboard</h1>
            </div>
            <div className="main-login-form">
                <h3>Please enter your ID</h3>
                <input
                    className="id-box"
                    type="text"
                    id="hospital-id"
                    value={hospitalID}
                    onChange={(e)=>setID(e.target.value)}
                    placeholder=" Enter hospital ID"
                />
                <br/>
                <div className="textbox-error">
                    {IdErrors!=''?(
                        <div>{IdErrors}</div>
                    ):(
                        <div></div>
                    )}
                </div>
                <button className="submit" onClick={redirectDashboard}>Go to Dashboard</button>
            </div>
        </div>
    )
}

export default HospitalLogin;