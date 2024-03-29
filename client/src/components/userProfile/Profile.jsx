import React from 'react'
import "./profile.css"
import {useFormik} from "formik"
import * as yup from "yup"
import { useGlobalUserContext } from '../../context/authContext'
import { useNavigate } from "react-router-dom";





const Profile = () => {
    const navigate = useNavigate();
    const {currentUser} = useGlobalUserContext();
    const formik = useFormik({
        initialValues: {
            username: "",
            full_name: "",
            email: "", 
            password: "",
        },
        validationSchema: yup.object().shape({
            username:yup.string(),
            full_name: yup.string(),
            email: yup.string().email("Invalid email"),
            password: yup.string().min(8, "Password must be at least 8 characters!"),
        }),
        onSubmit: (values) => {
            fetch(`/users/${currentUser.data.id}`, {
                method: "PATCH",
                headers:{
                    "Content-Type": "application/json",
                    Accept: "application/json",
                    Authorization: `Bearer ${localStorage.getItem("auth_token")}`
                },
                body: JSON.stringify(values),
            })
            .then((response) => {
                if (response.ok) {
                    alert("Account updated successfully");
                    navigate('/profile')
                    return response.json();

                }
            })
            .then((data) => {
                console.log(data)
            })
            .catch((error) => {
                console.log(`Error ${error}`);
            })

        }
    })
  return (
    <div className="user-container">
        
        <form action="" className="user-patch" onSubmit={formik.handleSubmit}>
        <h1>Personal Info</h1>
            <h2>Username</h2>
            <input type="text" onChange={formik.handleChange} value={formik.values.username} id='username' name='username' className="input" />
            <h2>Full Name</h2>
            <input type="text" onChange={formik.handleChange} value={formik.values.full_name} id='full_name' name='full_name' className="input" />
            <h2>Email</h2>
            <input type="text" onChange={formik.handleChange} value={formik.values.email} id='email' name='email' className="input"  />
            <h2>Password</h2>
            <input type="text" onChange={formik.handleChange} value={formik.values.password} id='password' name='password' className="input"  />
            <br />
            <button className="btn" type='submit' >Update</button>
        </form>
    </div>
  )
}

export default Profile