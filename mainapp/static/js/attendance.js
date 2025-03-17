// Modal functionality
const modal = document.getElementById('cameraModal');
const openModal = document.getElementById('openModal');
const closeModal = document.getElementById('closeModal');

openModal.addEventListener('click', () => {
    modal.style.display = 'flex';
    startCamera();
    
});

closeModal.addEventListener('click', () => {
    modal.style.display = 'none';
    stopCamera();
    console.log("heber");
});

window.addEventListener('click', (event) => {
    if (event.target === modal) {
        modal.style.display = 'none';
        stopCamera();
    }
});

// Camera functionality
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const resultText = document.getElementById('resultText');

function startCamera() {
    navigator.mediaDevices
        .getUserMedia({ video: true })
        .then((stream) => {
            video.srcObject = stream;
        })
        .catch((err) => {
            console.error('Error accessing camera:', err);
        });
}

function stopCamera() {
    const stream = video.srcObject;
    if (stream) {
        stream.getTracks().forEach((track) => track.stop());
    }
    video.srcObject = null;
}

function enableBtnLater(btn){
    btn.setAttribute("disabled", true);
    btn.textContent = "Wait a bit";
    setInterval(()=>btn.setAttribute("disabled", false), 5000)
}
// Take Attendance
document.getElementById('takeAttendance').addEventListener('click', (e) => {
    // Capture snapshot
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0)// canvas.width, canvas.height);
    let imageData = canvas.toDataURL('image/png'); // Base64 string
    imageData = imageData.replace(/^data:image\/?[A-z]*;base64,/, '');
    console.log(imageData)
    e.target.textContent = "CHECKING...";
    // Send snapshot to the backend
    fetch('/attendance/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ 
            image: imageData,
            attId: document.querySelector("#idholder").textContent,
        }),
    })
        .then((response) =>{
            e.target.textContent = "DONE.";
            setInterval(()=>{
                e.target.textContent = "Take Attendance"
            }, 1000);
            return response.json()
        })
        .then((data) => {
            e.target.textContent = "DONE."
            setInterval(()=>{
                e.target.textContent = "Take Attendance"
            }, 1000)
            if (data.status === 'success') {
                resultText.textContent = `Attendance taken: ${data.name}`;
                resultText.style.color = '#1dd1a1';
                e.target.textContent = "Take Attendance"
            } else if (data.status === "unrecognized"){
                e.target.textContent = "Take Attendance"
                resultText.textContent = 'Unrecognized face! Please contact the owner of this attendance if you think this is a mistake.';
                resultText.style.color = '#ff6b6b';
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            resultText.textContent = 'An Error occurred. Check your internet connection';
            resultText.style.color = '#ff6b6b';
        });
        setTimeout(()=>{resultText.textContent = ""}, 2000)
});

function trimall(s){
    s = s.replace(" ", "")
    if (s.search(" ") !== -1){
        return trimall(s)
    }
    return s
}
    
function getCookie(name){
    var cookieValue = null;
    if (document.cookie && document.coookie !== ''){
        var cookies = document.cookie.split(";");
        for (var i=0; i < cookies.length; i++){
            var cookie = trimall(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + "=")){
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
