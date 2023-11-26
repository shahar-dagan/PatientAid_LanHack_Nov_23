import React from "react";
import "./App.css";

/* This file contains the components for the code input page.
    the text input boxes, the enter button, and the confirmation page.
    It also contains a function to display an error message if the user
    enters an invalid code. */


export function CodeInput({ onCodeChange, code }) {
    const handleChange = (event, index) => {
        onCodeChange(index, event.target.value);
    };

    return (
        <div className="codeInputBox">
            <h3>Enter the code on the screen</h3>
            {[...Array(6)].map((_, index) => (
                <input
                    key={index}
                    type="text"
                    className="codeInputCell"
                    id={`cell${index + 1}`}
                    maxLength="1"
                    size="1"
                    value={code[index] ?? ""}
                    onChange={(event) => handleChange(event, index)}
                />
            ))}
        </div>
    );
}

export function EnterButton({ onSubmit }) {
    return (
        <div>
            <br />
            <button onClick={onSubmit}>Enter</button>
        </div>
    );
}

export function ConfirmationPage() {
    return <div>
        <p>Thanks for confirming your identity!</p>
    </div>;
}

export function invalidCodeMessage() {
    return <div>
        <p>Invalid code. Please try again.</p>
    </div>;
}
