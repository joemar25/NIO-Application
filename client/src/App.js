/*
    This app.js contains the front end that is going to be loaded in the web.
*/


import React from 'react'
import './App.css';
// importing record.js
import Home from './Home'

function App() {
    // return only one html elements in this case
    return (
        <Home />
    )
}

export default App