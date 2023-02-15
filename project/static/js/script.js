// ===================================== Script For Close alert ======================================

var alert_del = document.querySelectorAll(".alert-del");
alert_del.forEach((x) =>
    x.addEventListener("click", function () {
        x.parentElement.classList.add("hidden");
    })
);

// ========================================== Record Audio ==========================================

//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream; //stream from getUserMedia()
var rec; //Recorder.js object
var input; //MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb.
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext; //audio context to help us record

var recordButton = document.getElementById("rec_start");
var stopButton = document.getElementById("rec_stop");

//add events to those 2 buttons
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);

function startRecording() {
    // console.log("recordButton clicked");

    /*
          Simple constraints object, for more advanced audio features see
          https://addpipe.com/blog/audio-constraints-getusermedia/
      */

    var constraints = { audio: true, video: false };

    /*
          Disable the record button until we get a success or fail from getUserMedia() 
      */

    recordButton.disabled = true;
    stopButton.disabled = false;

    /*
    We're using the standard promise based getUserMedia() 
    https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
    */

    navigator.mediaDevices
        .getUserMedia(constraints)
        .then(function (stream) {
            // console.log(
            //     "getUserMedia() success, stream created, initializing Recorder.js ..."
            // );

            /*
                  create an audio context after getUserMedia is called
                  sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
                  the sampleRate defaults to the one set in your OS for your playback device
                  */
            audioContext = new AudioContext();

            //update the format
            document.getElementById("formats").innerHTML =
                "Format: 1 channel pcm @ " + audioContext.sampleRate / 1000 + "kHz";

            /*  assign to gumStream for later use  */
            gumStream = stream;

            /* use the stream */
            input = audioContext.createMediaStreamSource(stream);

            /* 
                  Create the Recorder object and configure to record mono sound (1 channel)
                  Recording 2 channels  will double the file size
              */
            rec = new Recorder(input, { numChannels: 1 });

            //start the recording process
            rec.record();

            // console.log("Recording started");
        })
        .catch(function (err) {
            //enable the record button if getUserMedia() fails
            recordButton.disabled = false;
            stopButton.disabled = true;
        });
}

function stopRecording() {
    // console.log("stopButton clicked");

    //disable the stop button, enable the record too allow for new recordings
    stopButton.disabled = true;
    recordButton.disabled = false;

    //tell the recorder to stop the recording
    rec.stop();

    //stop microphone access
    gumStream.getAudioTracks()[0].stop();

    //create the wav blob and pass it on to recordSave
    // rec.exportWAV(recordSave);

    recordSave();
}

function recordSave() {
    const path = ""


    // TODO: SAVE the audio path and pass the path to the backend

    // send data to rec handler in the backend
    $.ajax({
        type: "POST",
        url: "/rec_handler",
        data: {
            "status": "finished",
            "rec_audio_path": path,
        },
    })
}

// ============================================== End ===============================================