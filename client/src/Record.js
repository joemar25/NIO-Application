import React, {useState, useEffect} from 'react' 


function App() {
    document.title = 'Home'

    const [data, setData] = useState([{}])

    useEffect(()=> {
        fetch('/record').then(
            res => res.json()
        ).then(
            data => {
                setData(data)
            }
        )
    }, []) 

    return (
        <div>
            {(typeof data.members ==='undefined' ? (
                    <p>Loading...</p>
                ) : (
                    data.members.map((member, i) =>
                        <p key={i}> {member} </p> 
                ))
            )}
        </div>
    )
}

export default App