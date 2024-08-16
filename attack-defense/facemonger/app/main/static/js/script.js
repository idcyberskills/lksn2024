const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureButton = document.getElementById('capture');
const toggleCameraButton = document.getElementById('toggleCamera');
const retakePhotoButton = document.getElementById('retakePhoto');
const submitPhotoButton = document.getElementById('submitPhoto');
const webcamContainer = document.getElementById('webcam');
const capturedImageContainer = document.getElementById('capturedImageContainer');
const capturedImage = document.getElementById('capturedImage');
const loadingOverlay = document.getElementById('loadingOverlay');
const resultText = document.getElementById('detectionResult');
const secretWord = document.getElementById('secretWord');
let stream = null; // Ensure stream is null initially
let imageData; // Store captured image data

function generateRandomFilename() {
    const timestamp = Date.now();
    const randomString = Math.random().toString(36).substring(2, 15); 
    return `image_${timestamp}_${randomString}.png`;
}

function startCamera() {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(videoStream => {
            stream = videoStream;
            video.srcObject = stream;
            captureButton.disabled = false;
            toggleCameraButton.textContent = "Turn Off Camera";
        })
        .catch(err => console.error("Error accessing camera: ", err));
}

function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        video.srcObject = null; 
        stream = null;
        captureButton.disabled = true; 
        toggleCameraButton.textContent = "Turn On Camera";
    }
}

startCamera();

toggleCameraButton.addEventListener('click', () => {
    if (stream) {
        stopCamera();
    } else {
        startCamera();
    }
});

captureButton.addEventListener('click', () => {
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    imageData = canvas.toDataURL('image/png');

    capturedImage.src = imageData;
    webcamContainer.style.display = 'none';
    capturedImageContainer.style.display = 'block';
});

submitPhotoButton.addEventListener('click', () => {
    if (imageData) {
        loadingOverlay.style.display = 'block';

        const filename = generateRandomFilename();

        fetch('/upload', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageData, filename: filename })
        })
        .then(response => response.json())
        .then(data => {
            loadingOverlay.style.display = 'none';

            resultText.textContent = data.message;
            if (data.revealSecret) {
                secretWord.style.display = 'block';
            }
        })
        .catch(err => {
            loadingOverlay.style.display = 'none';
            console.error("Error submitting photo: ", err);
        });
    }
});

retakePhotoButton.addEventListener('click', () => {
    capturedImageContainer.style.display = 'none';
    webcamContainer.style.display = 'block';

    if (!stream) {
        startCamera();
    }
});
