import React, { useState, useEffect } from 'react'


function App() {
    document.title = 'Feedback'

    const [data, setData] = useState([{}])

    // use USE-EFFECT to fetch the route from our app/server.py 
    useEffect(() => {
        fetch('/feedback').then(
            res => res.json()
        ).then(
            data => { setData(data) }
        )
    }, [])

    return (
        <div>
            {/* {(typeof data.members === 'undefined' ?
                (
                    <p>Loading...</p>
                )
                :
                (
                    data.members.map((member, i) =>
                        <p key={i}> {member} </p>
                    )
                )
            )} */}

            {/* RATE */}
            {(typeof data.rate === 'undefined' ?
                (
                    <p> 0 </p>
                )
                :
                (
                    <p> Rate: {data.rate} </p>
                )
            )}

            {/* GRAMMAR */}
            {(typeof data.grammar === 'undefined' ?
                (
                    <p> 0 </p>
                )
                :
                (
                    <p> Grammar: {data.grammar} </p>
                )
            )}

            {/* GRAMMAR */}
            {(typeof data.fluency === 'undefined' ?
                (
                    <p> 0 </p>
                )
                :
                (
                    <p> Fluency: {data.fluency} </p>
                )
            )}

            {/* Emotion */}
            {(typeof data.emotion === 'undefined' ?
                (
                    <p> No emotion </p>
                )
                :
                (
                    <p> Emotion: {data.emotion} </p>
                )
            )}

            {/* Feedback */}
            {(typeof data.feedback === 'undefined' ?
                (
                    <p> 0 </p>
                )
                :
                (
                    <p> Feedback: {data.feedback} </p>
                )
            )}

        </div >
    )
}

export default App