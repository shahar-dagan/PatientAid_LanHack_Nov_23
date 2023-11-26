import React, { useState } from 'react';
import './App.css';
import { CodeInput, EnterButton, ConfirmationPage } from './code-input';
import axios from 'axios';

function Header() {
  return (
    <div>
      <h1 className="logo">PatientAId</h1>
    </div>
  );
}

function App() {
  const [code, setCode] = useState(Array(6).fill(null));
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [showConfirmationPage, setShowConfirmationPage] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);

  const changeCode = (index, value) => {
    const newCode = [...code];
    newCode[index] = value;
    setCode(newCode);
  };

  const changeFirstName = (event) => {
    setFirstName(event.target.value);
  };

  const changeLastName = (event) => {
    setLastName(event.target.value);
  };

  const submitCode = async () => {
    const patientId = code.join('');

    // Make an API request to the Flask backend to save the entered code, first name, and last name
    try {
      const response = await axios.post('http://localhost:5000/save-to-database', {
        value1: patientId,
        value2: firstName,
        value3: lastName,
      });

      // Assume the response contains the necessary data
      // PUT ACTUAL VALIDATION HERE
      if (response.data.status === 'success') {
        setErrorMessage(null);
        setShowConfirmationPage(true);
      } else {
        setErrorMessage('Error saving data to the database.');
      }
    } catch (error) {
      console.error('Error making API request:', error);
      setErrorMessage('Error validating code. Please try again.');
    }
  };

  const nextPatient = () => {
    setShowConfirmationPage(false);
    setCode(Array(6).fill(null));
    setFirstName('');
    setLastName('');
  };

  return (
    <div className="app-container">
      <Header />
      {showConfirmationPage ? (
        <>
          <ConfirmationPage /> <br />
          <button onClick={nextPatient}>Next Patient</button>
        </>
      ) : (
        <>
          <CodeInput onCodeChange={changeCode} code={code} />
          <div className="name-inputs">
            <label>
              First Name:
              <input type="text" value={firstName} onChange={changeFirstName} />
            </label>
            <label>
              Last Name:
              <input type="text" value={lastName} onChange={changeLastName} />
            </label>
          </div>
          <EnterButton onSubmit={submitCode} />
          {errorMessage && <p>{errorMessage}</p>}
        </>
      )}
    </div>
  );
}

export default App;
