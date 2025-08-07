/**
 * Face Swap Live - OPTIMIZED Client JavaScript
 * Minimal logging for maximum performance
 */

// Global application state
const FaceSwapApp = {
    socket: null,
    elements: {},
    contexts: {},
    state: {
        connected: false,
        processingActive: true,
        isProcessing: false,
        webcamReady: false,
        sourceUploaded: false,
        frameCount: 0,
        swapCount: 0,
        errorCount: 0,
        sessionStartTime: null,
        lastFrameTime: 0,
        processingInterval: null,
        statsInterval: null
    },
    config: {
        targetFPS: 15,  // Increased from 12
        processingInterval: 67, // ~15 FPS
        statsUpdateInterval: 1000,
        maxLogEntries: 10,  // Reduced from 30
        webcamConstraints: {
            video: {
                width: { ideal: 640 },
                height: { ideal: 480 },
                frameRate: { ideal: 30 }
            }
        }
    }
};

// DISABLED LOGGING FOR PERFORMANCE
function addLog(message, type = 'info') {
    // Completely disabled for performance
    // Only show critical errors in console
    if (type === 'error') {
        console.error(message);
    }
}

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    initializeElements();
    initializeCanvases();
    initializeSocket();
    initializeWebcam();
    startStatsUpdates();
    setupEventListeners();
});

function initializeElements() {
    const elements = FaceSwapApp.elements;
    
    elements.webcam = document.getElementById('webcam');
    elements.outputCanvas = document.getElementById('outputCanvas');
    elements.sourceCanvas = document.getElementById('sourceCanvas');
    elements.captureCanvas = document.createElement('canvas');
    
    elements.statusDot = document.getElementById('statusDot');
    elements.statusText = document.getElementById('statusText');
    elements.statusBox = document.getElementById('statusBox');
    elements.logs = document.getElementById('logs');
    elements.loadingOverlay = document.getElementById('loadingOverlay');
    
    elements.webcamOverlay = document.getElementById('webcamOverlay');
    elements.outputOverlay = document.getElementById('outputOverlay');
    elements.sourceOverlay = document.getElementById('sourceOverlay');
    
    elements.frameCount = document.getElementById('frameCount');
    elements.swapCount = document.getElementById('swapCount');
    elements.avgTime = document.getElementById('avgTime');
    elements.fpsCount = document.getElementById('fpsCount');
    elements.processingTime = document.getElementById('processingTime');
    elements.successRate = document.getElementById('successRate');
    elements.sessionTime = document.getElementById('sessionTime');
}

function initializeCanvases() {
    const contexts = FaceSwapApp.contexts;
    const elements = FaceSwapApp.elements;
    
    contexts.output = elements.outputCanvas.getContext('2d', { 
        alpha: false,
        desynchronized: true 
    });
    contexts.source = elements.sourceCanvas.getContext('2d', { 
        alpha: false 
    });
    contexts.capture = elements.captureCanvas.getContext('2d', { 
        alpha: false,
        willReadFrequently: true 
    });
    
    // Performance optimizations
    [contexts.output, contexts.source].forEach(ctx => {
        ctx.imageSmoothingEnabled = true;
        ctx.imageSmoothingQuality = 'high';
    });
    
    contexts.capture.imageSmoothingEnabled = false;
}

function initializeSocket() {
    updateConnectionStatus('connecting', 'Connecting...');
    
    FaceSwapApp.socket = io({
        transports: ['websocket', 'polling'],
        timeout: 10000,
        reconnection: true,
        reconnectionAttempts: 5,
        reconnectionDelay: 2000
    });
    
    FaceSwapApp.socket.on('connect', handleSocketConnect);
    FaceSwapApp.socket.on('disconnect', handleSocketDisconnect);
    FaceSwapApp.socket.on('connect_error', handleSocketError);
    FaceSwapApp.socket.on('reconnect', handleSocketReconnect);
    FaceSwapApp.socket.on('processed_frame', handleProcessedFrame);
    FaceSwapApp.socket.on('status_update', handleStatusUpdate);
    FaceSwapApp.socket.on('connection_rejected', handleConnectionRejected);
    FaceSwapApp.socket.on('stats_update', handleStatsUpdate);
}

async function initializeWebcam() {
    const elements = FaceSwapApp.elements;
    const state = FaceSwapApp.state;
    
    try {
        const configs = [
            FaceSwapApp.config.webcamConstraints,
            { video: { width: 640, height: 480 } },
            { video: true }
        ];
        
        let stream = null;
        for (const config of configs) {
            try {
                stream = await navigator.mediaDevices.getUserMedia(config);
                break;
            } catch (configError) {
                continue;
            }
        }
        
        if (!stream) {
            throw new Error('Failed to access camera');
        }
        
        elements.webcam.srcObject = stream;
        
        elements.webcam.onloadedmetadata = () => {
            elements.webcamOverlay.classList.add('hidden');
            document.getElementById('webcamIndicator').classList.add('active');
            state.webcamReady = true;
            
            setTimeout(() => {
                startProcessingLoop();
                hideLoadingOverlay();
            }, 1000);
        };
        
        elements.webcam.onerror = (error) => {
            addLog('Webcam error', 'error');
            updateStatus('Webcam error occurred', 'error');
        };
        
    } catch (error) {
        addLog('Webcam initialization failed', 'error');
        updateStatus('Camera access denied. Please allow camera access and refresh.', 'error');
        hideLoadingOverlay();
        showWebcamError(error);
    }
}

function startProcessingLoop() {
    const state = FaceSwapApp.state;
    const config = FaceSwapApp.config;
    
    if (state.processingInterval) {
        clearInterval(state.processingInterval);
    }
    
    state.sessionStartTime = Date.now();
    
    state.processingInterval = setInterval(() => {
        if (!state.processingActive || state.isProcessing || !state.webcamReady) {
            return;
        }
        processFrame();
    }, config.processingInterval);
}

function processFrame() {
    const elements = FaceSwapApp.elements;
    const contexts = FaceSwapApp.contexts;
    const state = FaceSwapApp.state;
    
    if (!elements.webcam.videoWidth || !elements.webcam.videoHeight) {
        return;
    }
    
    state.isProcessing = true;
    state.frameCount++;
    
    try {
        const width = elements.webcam.videoWidth;
        const height = elements.webcam.videoHeight;
        
        if (elements.captureCanvas.width !== width) {
            elements.captureCanvas.width = width;
        }
        if (elements.captureCanvas.height !== height) {
            elements.captureCanvas.height = height;
        }
        
        contexts.capture.drawImage(elements.webcam, 0, 0);
        
        if (state.sourceUploaded && state.connected) {
            const frameData = elements.captureCanvas.toDataURL('image/jpeg', 0.8);
            FaceSwapApp.socket.emit('process_frame', { frame: frameData });
        }
        
        elements.frameCount.textContent = state.frameCount;
        
    } catch (error) {
        addLog('Frame processing error', 'error');
    } finally {
        state.isProcessing = false;
    }
}

function updateOutputCanvas(sourceCanvas) {
    const elements = FaceSwapApp.elements;
    const contexts = FaceSwapApp.contexts;
    
    try {
        if (elements.outputCanvas.width !== sourceCanvas.width) {
            elements.outputCanvas.width = sourceCanvas.width;
        }
        if (elements.outputCanvas.height !== sourceCanvas.height) {
            elements.outputCanvas.height = sourceCanvas.height;
        }
        
        contexts.output.drawImage(sourceCanvas, 0, 0);
        document.getElementById('outputIndicator').classList.add('active');
        
    } catch (error) {
        console.error('Error updating output canvas:', error);
    }
}

function handleProcessedFrame(data) {
    const state = FaceSwapApp.state;
    const elements = FaceSwapApp.elements;
    
    try {
        if (data.processed) {
            const img = new Image();
            img.onload = () => {
                updateOutputCanvas(img);
                
                if (elements.outputOverlay && !elements.outputOverlay.classList.contains('hidden')) {
                    elements.outputOverlay.classList.add('hidden');
                }
                
                if (data.success) {
                    state.swapCount++;
                } else {
                    state.errorCount++;
                }
            };
            img.onerror = () => {
                state.errorCount++;
            };
            img.src = data.processed;
        }
        
        if (data.stats) {
            updateStatsFromServer(data.stats);
        }
        
    } catch (error) {
        addLog('Response handling error', 'error');
        state.errorCount++;
    }
}

function updateStatsFromServer(stats) {
    const elements = FaceSwapApp.elements;
    
    if (stats.swap_count !== undefined) {
        elements.swapCount.textContent = stats.swap_count;
    }
    
    if (stats.avg_processing_time !== undefined) {
        elements.avgTime.textContent = stats.avg_processing_time + 'ms';
    }
    
    if (stats.processing_time !== undefined) {
        elements.processingTime.textContent = stats.processing_time + 'ms';
    }
    
    if (stats.fps !== undefined) {
        elements.fpsCount.textContent = stats.fps.toFixed(1);
    }
    
    const totalFrames = stats.frame_count || FaceSwapApp.state.frameCount;
    const successfulSwaps = stats.swap_count || FaceSwapApp.state.swapCount;
    
    if (totalFrames > 0) {
        const successRate = (successfulSwaps / totalFrames * 100).toFixed(1);
        elements.successRate.textContent = successRate + '%';
    }
}

function startStatsUpdates() {
    const state = FaceSwapApp.state;
    const config = FaceSwapApp.config;
    
    state.statsInterval = setInterval(() => {
        updateSessionTime();
    }, config.statsUpdateInterval);
}

function updateSessionTime() {
    const elements = FaceSwapApp.elements;
    const state = FaceSwapApp.state;
    
    if (state.sessionStartTime) {
        const elapsed = Math.floor((Date.now() - state.sessionStartTime) / 1000);
        const minutes = Math.floor(elapsed / 60);
        const seconds = elapsed % 60;
        
        elements.sessionTime.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
    }
}

async function uploadSource() {
    const fileInput = document.getElementById('sourceFile');
    const uploadBtn = document.getElementById('uploadBtn');
    
    if (!fileInput.files[0]) {
        alert('Please select an image first');
        return;
    }
    
    const file = fileInput.files[0];
    
    if (!file.type.startsWith('image/')) {
        alert('Please select a valid image file');
        return;
    }
    
    if (file.size > 10 * 1024 * 1024) {
        alert('File size must be less than 10MB');
        return;
    }
    
    updateStatus('Processing uploaded image...', 'info');
    
    uploadBtn.disabled = true;
    uploadBtn.innerHTML = '<span class="btn-icon">⏳</span> Processing...';
    
    const formData = new FormData();
    formData.append('image', file);
    
    try {
        const response = await fetch('/upload_source', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        updateStatus(result.message, result.success ? 'success' : 'error');
        
        if (result.success) {
            const img = new Image();
            img.onload = () => {
                const elements = FaceSwapApp.elements;
                const contexts = FaceSwapApp.contexts;
                
                elements.sourceCanvas.width = img.width;
                elements.sourceCanvas.height = img.height;
                contexts.source.drawImage(img, 0, 0);
                
                elements.sourceOverlay.classList.add('hidden');
                document.getElementById('sourceIndicator').classList.add('active');
                
                FaceSwapApp.state.sourceUploaded = true;
                updateStatus('✅ Source face ready! Real-time swapping is now ACTIVE!', 'success');
            };
            img.src = URL.createObjectURL(file);
        } 
        
    } catch (error) {
        addLog('Upload failed', 'error');
        updateStatus('Upload failed', 'error');
    } finally {
        uploadBtn.disabled = false;
        uploadBtn.innerHTML = '<span class="btn-icon">📸</span> Upload & Start';
    }
}

function clearSource() {
    const elements = FaceSwapApp.elements;
    const contexts = FaceSwapApp.contexts;
    const state = FaceSwapApp.state;
    
    if (FaceSwapApp.socket && state.connected) {
        FaceSwapApp.socket.emit('clear_source');
    }
    
    contexts.source.clearRect(0, 0, elements.sourceCanvas.width, elements.sourceCanvas.height);
    elements.sourceOverlay.classList.remove('hidden');
    document.getElementById('sourceIndicator').classList.remove('active');
    
    contexts.output.clearRect(0, 0, elements.outputCanvas.width, elements.outputCanvas.height);
    elements.outputOverlay.classList.remove('hidden');
    document.getElementById('outputIndicator').classList.remove('active');
    
    state.sourceUploaded = false;
    updateStatus('Source face cleared - upload a new face to start swapping', 'info');
}

function toggleProcessing() {
    const state = FaceSwapApp.state;
    const toggleBtn = document.getElementById('toggleBtn');
    
    state.processingActive = !state.processingActive;
    
    if (state.processingActive) {
        toggleBtn.innerHTML = '<span class="btn-icon">⏸️</span> Pause';
    } else {
        toggleBtn.innerHTML = '<span class="btn-icon">▶️</span> Resume';
    }
}

function clearLogs() {
    FaceSwapApp.elements.logs.innerHTML = '';
}

function updateStatus(message, type = 'info') {
    const elements = FaceSwapApp.elements;
    
    document.getElementById('status').textContent = message;
    elements.statusBox.className = `status-box ${type === 'error' ? 'error' : type === 'warning' ? 'warning' : ''}`;
}

function updateConnectionStatus(status, message) {
    const elements = FaceSwapApp.elements;
    
    elements.statusDot.className = `status-dot ${status}`;
    elements.statusText.textContent = message;
}

function showLoadingOverlay(message = 'Loading...') {
    const overlay = FaceSwapApp.elements.loadingOverlay;
    overlay.querySelector('.loading-text').textContent = message;
    overlay.classList.remove('hidden');
}

function hideLoadingOverlay() {
    FaceSwapApp.elements.loadingOverlay.classList.add('hidden');
}

function showWebcamError(error) {
    let helpMessage = 'Camera access failed. ';
    
    if (error.name === 'NotAllowedError') {
        helpMessage += 'Please allow camera access and refresh the page.';
    } else if (error.name === 'NotFoundError') {
        helpMessage += 'No camera found. Please connect a camera and refresh.';
    } else if (error.name === 'NotReadableError') {
        helpMessage += 'Camera is being used by another application. Please close other apps and refresh.';
    } else {
        helpMessage += 'Please check your camera and refresh the page.';
    }
    
    updateStatus(helpMessage, 'error');
}

function setupEventListeners() {
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            FaceSwapApp.state.processingActive = false;
        } else {
            FaceSwapApp.state.processingActive = true;
        }
    });
    
    window.addEventListener('beforeunload', () => {
        if (FaceSwapApp.state.processingInterval) {
            clearInterval(FaceSwapApp.state.processingInterval);
        }
        if (FaceSwapApp.state.statsInterval) {
            clearInterval(FaceSwapApp.state.statsInterval);
        }
        
        if (FaceSwapApp.socket) {
            FaceSwapApp.socket.disconnect();
        }
    });
    
    document.getElementById('sourceFile').addEventListener('change', (event) => {
        const file = event.target.files[0];
        // No logging for file selection
    });
}

// Socket event handlers
function handleSocketConnect() {
    const state = FaceSwapApp.state;
    
    state.connected = true;
    updateConnectionStatus('connected', 'Connected to server');
    updateStatus('Connected to real-time face swap server', 'success');
}

function handleSocketDisconnect() {
    const state = FaceSwapApp.state;
    
    state.connected = false;
    updateConnectionStatus('disconnected', 'Disconnected from server');
    updateStatus('Disconnected from server', 'error');
}

function handleSocketError(error) {
    updateStatus('Failed to connect to server', 'error');
    updateConnectionStatus('disconnected', 'Connection failed');
}

function handleSocketReconnect() {
    updateStatus('Reconnected to server', 'success');
    updateConnectionStatus('connected', 'Reconnected');
}

function handleStatusUpdate(data) {
    // Minimal status updates only
}

function handleConnectionRejected(data) {
    updateStatus(data.message, 'error');
    alert('Server is currently serving another user. Please try again later.');
}

function handleStatsUpdate(data) {
    updateStatsFromServer(data);
}

// Make functions globally available
window.uploadSource = uploadSource;
window.clearSource = clearSource;
window.toggleProcessing = toggleProcessing;
window.clearLogs = clearLogs;