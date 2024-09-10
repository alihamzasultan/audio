function startRecording() {
    let chunks = [];
    const mediaRecorder = new MediaRecorder(window.stream);

    mediaRecorder.ondataavailable = function(event) {
        chunks.push(event.data);
    };

    mediaRecorder.onstop = function() {
        const blob = new Blob(chunks, { type: 'audio/wav' });
        const url = URL.createObjectURL(blob);
        document.getElementById('audio-preview').src = url;
        document.getElementById('audio-data').value = url;
    };

    mediaRecorder.start();
    document.getElementById('record-button').disabled = true;
    document.getElementById('stop-button').disabled = false;

    document.getElementById('stop-button').onclick = function() {
        mediaRecorder.stop();
        document.getElementById('record-button').disabled = false;
        document.getElementById('stop-button').disabled = true;
    };
}

async function setupStream() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    window.stream = stream;
}

setupStream();
