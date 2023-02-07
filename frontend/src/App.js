/*
    This app.js contains the front end that is going to be loaded in the web.
*/


import React from 'react'
import './App.css';

// importing pages
import Home from './Home'
// import Record from './components/Record'

function App() {
    // return only one html elements in this case
    return (
        <Home />
    )
}

export default App