let mediaRecorder, stream, chunks = [];

async function startRecording() {
    try {
        // get user media
        stream = await navigator.mediaDevices.getUserMedia({ audio: true });

        // create media recorder
        mediaRecorder = new MediaRecorder(stream, {
            mimeType: "audio/webm;codecs=opus",
        });

        // handle data and stop events
        mediaRecorder.addEventListener("dataavailable", ({ data }) => {
            chunks.push(data);
        });

        // Set up timer
        const startTime = Date.now();
        const timerElement = document.getElementById("timer");
        timerElement.classList.remove("hidden");

        const updateTimer = () => {
            const elapsedTime = new Date(Date.now() - startTime);
            const minutes = elapsedTime.getUTCMinutes().toString().padStart(2, "0");
            const seconds = elapsedTime.getUTCSeconds().toString().padStart(2, "0");
            timerElement.textContent = `${minutes}:${seconds}`;
        };

        const timerInterval = setInterval(updateTimer, 1000);

        mediaRecorder.addEventListener("stop", async () => {

            // clear time
            clearInterval(timerInterval);

            // create audio blob and form data
            const audioBlob = new Blob(chunks, { type: chunks[0].type });
            const timestamp = Date.now();
            const formData = new FormData();
            formData.append("audio", audioBlob, `${timestamp}.wav`);

            // show loading animation
            const loadingContainer = document.getElementById("loading-container");
            loadingContainer.classList.add("show");

            try {
                // send audio to server
                const response = await fetch("/upload", {
                    method: "POST",
                    body: formData,
                });

                // handle response
                if (response.ok) {
                    // redirect to success page
                    window.location.href = "/process_audio";
                } else {
                    // show error message
                    console.error(
                        "Error sending audio recording to server:",
                        response.statusText
                    );
                    window.location.href = "/process_audio_fail";
                }
            } catch (error) {
                console.error("Error sending audio recording to server:", error);
                window.location.href = "/process_audio_fail";
            }

            // hide loading animation
            loadingContainer.classList.remove("show");
        });

        // Set recording time limit
        const recordingTimeLimit = 5 * 60 * 1000; // 5 minutes in milliseconds
        setTimeout(() => {
            stopRecording();
        }, recordingTimeLimit);

        // start recording
        mediaRecorder.start();
    } catch (error) {
        console.error(error);
        window.location.href = "/process_audio_fail";
    }
}


function stopRecording() {

    // Stop recording and release resources
    mediaRecorder.stop();
    stream.getTracks().forEach(track => track.stop());

    // Remove loading
    const loadingContainer = document.getElementById("loading-container");
    loadingContainer.classList.remove("show");

    // Disable record button
    const recordBtn = document.getElementById("record-btn");
    recordBtn.value = "Record";
    recordBtn.disabled = true;

    // Disable hover effects
    const style = document.createElement("style");
    style.innerHTML = `* { pointer-events: none; }`;
    document.head.appendChild(style);
}

const recordBtn = document.getElementById("record-btn");
if (recordBtn) {
    recordBtn.addEventListener("click", function () {
        if (mediaRecorder && mediaRecorder.state === "recording") {
            stopRecording();
        } else {
            startRecording();
            this.value = "Stop";
        }
    });
}
