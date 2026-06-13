class CameraCapture {
    constructor() {
        this.video = document.getElementById('video');
        this.canvas = document.getElementById('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.resultDiv = document.getElementById('result');
        this.isRunning = false;
        this.recognitionInterval = null;
        
        this.setupEventListeners();
    }
    
    // Initialize camera access
    async initializeCamera() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { 
                    width: { ideal: 640 },
                    height: { ideal: 480 }
                },
                audio: false
            });
            
            this.video.srcObject = stream;
            
            // Wait for video to load
            this.video.onloadedmetadata = () => {
                this.canvas.width = this.video.videoWidth;
                this.canvas.height = this.video.videoHeight;
            };
            
            console.log('Camera initialized successfully');
        } catch (error) {
            console.error('Camera access denied:', error);
            this.showError('Please allow camera access to use this feature');
        }
    }
    
    // Capture current frame from video
    captureFrame() {
        this.ctx.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
        return this.canvas.toDataURL('image/jpeg', 0.8); // 80% quality
    }
    
    // Send frame to Flask backend for recognition
    async sendFrameToServer(base64Image) {
        try {
            const response = await fetch('/recognize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    image: base64Image
                })
            });
            
            const result = await response.json();
            this.displayResult(result);
            return result;
        } catch (error) {
            console.error('Error sending frame:', error);
            this.showError('Connection error');
        }
    }
    
    // Display recognition results
    displayResult(result) {
        const div = this.resultDiv;
        div.style.display = 'block';
        
        if (result.status === 'recognized') {
            div.className = 'result recognized';
            div.innerHTML = `
                <h2>✓ Hello! This is ${result.name}</h2>
                <p>Confidence: ${(result.confidence * 100).toFixed(1)}%</p>
                <p>Relationship: ${result.relationship || 'Unknown'}</p>
                <p>Last visit: ${result.last_visit || 'First visit'}</p>
            `;
        } else {
            div.className = 'result unknown';
            div.innerHTML = `
                <h2>? Unknown Visitor</h2>
                <p>Confidence: ${(result.confidence * 100).toFixed(1)}%</p>
                <p>This person hasn't been registered yet.</p>
            `;
        }
    }
    
    showError(message) {
        const div = this.resultDiv;
        div.style.display = 'block';
        div.className = 'result unknown';
        div.innerHTML = `<p>${message}</p>`;
    }
    
    // Manual capture button
    setupEventListeners() {
        document.getElementById('captureBtn').addEventListener('click', () => {
            const frameData = this.captureFrame();
            this.sendFrameToServer(frameData);
        });
        
        document.getElementById('autoBtn').addEventListener('click', () => {
            this.toggleAutoRecognition();
        });
    }
    
    // Auto-recognition every 2 seconds
    toggleAutoRecognition() {
        if (this.isRunning) {
            clearInterval(this.recognitionInterval);
            this.isRunning = false;
            document.getElementById('autoBtn').textContent = 'Start Auto-Recognition';
        } else {
            this.isRunning = true;
            document.getElementById('autoBtn').textContent = 'Stop Auto-Recognition';
            
            this.recognitionInterval = setInterval(() => {
                const frameData = this.captureFrame();
                this.sendFrameToServer(frameData);
            }, 2000); // Recognize every 2 seconds
        }
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', async () => {
    const camera = new CameraCapture();
    await camera.initializeCamera();
});


class WebSocketCamera {
    constructor() {
        this.ws = new WebSocket('ws://localhost:5000/recognize-stream');
        this.ws.onopen = () => console.log('Connected');
        this.ws.onmessage = (event) => {
            const result = JSON.parse(event.data);
            this.displayResult(result);
        };
    }
    
    sendFrame(base64Image) {
        if (this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(base64Image);
        }
    }
}