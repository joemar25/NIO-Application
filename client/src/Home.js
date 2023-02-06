import React, { useState, useEffect } from 'react'

function App() {
    document.title = 'Home'

    const [data, setData] = useState([{}])

    // use USE-EFFECT to fetch the route from our app/server.py 
    useEffect(() => {
        fetch('/index').then(
            res => res.json()
        ).then(
            data => { setData(data) }
        )
    }, [])

    return (
        <div>

            <div class="h-20 bg-pink-200">

                <p class="text-center" id="title">NiO - Speech Delivery Improvement App</p>

            </div>

            {/* Display Error Message */}
            {(typeof data.error !== 'undefined' ?
                (
                    <p>  </p>
                )
                :
                (
                    <p> {data.error} </p>
                )
            )}

            <form action="/index" id="inputData" class="relative top-5" method="post" enctype="multipart/form-data">

                <label for="html">What do you want me to call you?</label>
                <br />
                <input
                    class="w-64 h-8 relative left-10 border-2 border-stone-600 rounded"
                    type="text"
                    id="username"
                    name="username"
                    placeholder="Enter your name"
                    minlength="3"
                    maxlength="19"
                />
                <br />


                <div class="flex flex-row column-2 p-10">

                    <input
                        class="p-1 w-1/2 h-48 border-2 border-stone-600 rounded self-center"
                        type="text"
                        id="text_script"
                        name="text_script"
                        placeholder="Input Speech"
                    />

                    <input class="float-left relative left-48 top-16" type="file" id="file_script" name="file_script" accept=".txt" />

                </div>

                <input class="float-right relative right-64 w-24 h-8 border-2 border-stone-600 rounded" type="submit" id="submit" value="Proceed" />


            </form>

        </div >
    )
}

export default App