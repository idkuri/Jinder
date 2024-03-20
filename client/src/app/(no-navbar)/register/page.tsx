"use client"
import React, {useState} from "react"
import "../../styles/register.css"
import Image from 'next/image'
export default function Register() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [mode, setMode] = useState(-1)

  async function sendRegisterRequest() {
    let accountType = ""
    if (mode === 0) {
      accountType = "applicant"
    }
    else if (mode === 1) {
      accountType = "company"
    }
    const response = await fetch("/api/register", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: username,
        password: password,
        confirmPassword: confirmPassword,
        accountType: accountType
      })
    })

  }
  function renderForm() {
    if (mode == -1) {
      return (
        <div id="grid">
          <div className="left" onClick={() => setMode(0)}>
            <Image src="https://www.svgrepo.com/show/347900/person.svg" width={300} height={300} alt="Create Company Account"></Image>
            <h1 className="text-2xl">Create an Applicant Account</h1>
          </div>
          <div className="right" onClick={() => setMode(1)}>
            <Image src="https://www.svgrepo.com/show/490660/company.svg" width={300} height={300} alt="Create Company Account"></Image>
            <h1 className="text-2xl">Create a Company Account</h1>
          </div>
        </div>
      )
    }
    else if (mode == 0) {
      return(
        <div className="homepage">
          <h1 className="text-3xl pb-5">Register Applicant Account</h1>
          <div className="formContainer">
            <label className="input input-bordered flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" className="w-4 h-4 opacity-70"><path d="M2.5 3A1.5 1.5 0 0 0 1 4.5v.793c.026.009.051.02.076.032L7.674 8.51c.206.1.446.1.652 0l6.598-3.185A.755.755 0 0 1 15 5.293V4.5A1.5 1.5 0 0 0 13.5 3h-11Z" /><path d="M15 6.954 8.978 9.86a2.25 2.25 0 0 1-1.956 0L1 6.954V11.5A1.5 1.5 0 0 0 2.5 13h11a1.5 1.5 0 0 0 1.5-1.5V6.954Z" /></svg>
              <input type="text" className="grow" onChange={(e : React.ChangeEvent<HTMLInputElement>) => {setUsername(e.target.value)}} placeholder="Username" />
            </label>
            <label className="input input-bordered flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" className="w-4 h-4 opacity-70"><path fill-rule="evenodd" d="M14 6a4 4 0 0 1-4.899 3.899l-1.955 1.955a.5.5 0 0 1-.353.146H5v1.5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-2.293a.5.5 0 0 1 .146-.353l3.955-3.955A4 4 0 1 1 14 6Zm-4-2a.75.75 0 0 0 0 1.5.5.5 0 0 1 .5.5.75.75 0 0 0 1.5 0 2 2 0 0 0-2-2Z" clip-rule="evenodd" /></svg>
              <input type="password" className="grow" onChange={(e : React.ChangeEvent<HTMLInputElement>) => {setPassword(e.target.value)}} value={password} placeholder="Enter Password"/>
            </label>
            <label className="input input-bordered flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" className="w-4 h-4 opacity-70"><path fill-rule="evenodd" d="M14 6a4 4 0 0 1-4.899 3.899l-1.955 1.955a.5.5 0 0 1-.353.146H5v1.5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-2.293a.5.5 0 0 1 .146-.353l3.955-3.955A4 4 0 1 1 14 6Zm-4-2a.75.75 0 0 0 0 1.5.5.5 0 0 1 .5.5.75.75 0 0 0 1.5 0 2 2 0 0 0-2-2Z" clip-rule="evenodd" /></svg>
              <input type="password" className="grow" onChange={(e : React.ChangeEvent<HTMLInputElement>) => {setConfirmPassword(e.target.value)}} value={confirmPassword} placeholder="Confirm Password"/>
            </label>
            <button className="btn text-xl" onClick={() => {sendRegisterRequest()}}>Register</button>
          </div>
      </div>
      )
    }
    else if (mode == 1) {
      return (
        <div className="homepage">
          <h1 className="text-3xl pb-5">Register Company Account</h1>
          <div className="formContainer">
            <label className="input input-bordered flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" className="w-4 h-4 opacity-70"><path d="M2.5 3A1.5 1.5 0 0 0 1 4.5v.793c.026.009.051.02.076.032L7.674 8.51c.206.1.446.1.652 0l6.598-3.185A.755.755 0 0 1 15 5.293V4.5A1.5 1.5 0 0 0 13.5 3h-11Z" /><path d="M15 6.954 8.978 9.86a2.25 2.25 0 0 1-1.956 0L1 6.954V11.5A1.5 1.5 0 0 0 2.5 13h11a1.5 1.5 0 0 0 1.5-1.5V6.954Z" /></svg>
              <input type="text" className="grow" onChange={(e : React.ChangeEvent<HTMLInputElement>) => {setUsername(e.target.value)}} placeholder="Username" />
            </label>
            <label className="input input-bordered flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" className="w-4 h-4 opacity-70"><path fill-rule="evenodd" d="M14 6a4 4 0 0 1-4.899 3.899l-1.955 1.955a.5.5 0 0 1-.353.146H5v1.5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-2.293a.5.5 0 0 1 .146-.353l3.955-3.955A4 4 0 1 1 14 6Zm-4-2a.75.75 0 0 0 0 1.5.5.5 0 0 1 .5.5.75.75 0 0 0 1.5 0 2 2 0 0 0-2-2Z" clip-rule="evenodd" /></svg>
              <input type="password" className="grow" onChange={(e : React.ChangeEvent<HTMLInputElement>) => {setPassword(e.target.value)}} value={password} placeholder="Enter Password"/>
            </label>
            <label className="input input-bordered flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" className="w-4 h-4 opacity-70"><path fill-rule="evenodd" d="M14 6a4 4 0 0 1-4.899 3.899l-1.955 1.955a.5.5 0 0 1-.353.146H5v1.5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-2.293a.5.5 0 0 1 .146-.353l3.955-3.955A4 4 0 1 1 14 6Zm-4-2a.75.75 0 0 0 0 1.5.5.5 0 0 1 .5.5.75.75 0 0 0 1.5 0 2 2 0 0 0-2-2Z" clip-rule="evenodd" /></svg>
              <input type="password" className="grow" onChange={(e : React.ChangeEvent<HTMLInputElement>) => {setConfirmPassword(e.target.value)}} value={confirmPassword} placeholder="Confirm Password"/>
            </label>
            <button className="btn text-xl" onClick={() => {window.location.href = "/"}}>Register</button>
          </div>
      </div>
      )
    }
  }

  return (
    <main>
      {renderForm()}
    </main>
  );
}
