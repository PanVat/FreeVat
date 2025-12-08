// Handle file selection display
const modelFileInput = document.getElementById('modelFile');
const selectedFileDiv = document.getElementById('selectedFile');
const fileNameSpan = document.getElementById('fileName');
const fileUploadArea = document.getElementById('fileUploadArea');

modelFileInput.addEventListener('change', function () {
    if (this.files.length > 0) {
        const file = this.files[0];
        fileNameSpan.textContent = file.name + ' (' + formatFileSize(file.size) + ')';
        selectedFileDiv.classList.remove('hidden');
        selectedFileDiv.classList.add('block');
        fileUploadArea.classList.add('border-teal-400');
        fileUploadArea.classList.remove('border-gray-700');
    } else {
        selectedFileDiv.classList.remove('block');
        selectedFileDiv.classList.add('hidden');
        fileUploadArea.classList.remove('border-teal-400');
        fileUploadArea.classList.add('border-gray-700');
    }
});

// Drag and drop functionality
fileUploadArea.addEventListener('dragover', function (e) {
    e.preventDefault();
    this.classList.add('dragover', 'border-teal-400', 'bg-teal-400/10');
});

fileUploadArea.addEventListener('dragleave', function (e) {
    e.preventDefault();
    this.classList.remove('dragover', 'border-teal-400', 'bg-teal-400/10');
    if (!modelFileInput.files.length) {
        this.classList.add('border-gray-700');
    }
});

fileUploadArea.addEventListener('drop', function (e) {
    e.preventDefault();
    this.classList.remove('dragover', 'bg-teal-400/10');

    if (e.dataTransfer.files.length) {
        modelFileInput.files = e.dataTransfer.files;
        const event = new Event('change', {bubbles: true});
        modelFileInput.dispatchEvent(event);
    }
});

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Form submission handler - client-side validation
const uploadForm = document.getElementById('uploadForm');

uploadForm.addEventListener('submit', function (e) {
    // Basic form validation
    const modelName = document.getElementById('modelName').value;
    const authorName = document.getElementById('authorName').value;
    const category = document.getElementById('category').value;
    const description = document.getElementById('description').value;
    const license = document.getElementById('license').value;

    if (!modelName || !authorName || !category || !description || !license) {
        alert('Please fill in all required fields (marked with *)');
        e.preventDefault();
        return;
    }

    // Check if file is selected
    if (modelFileInput.files.length === 0) {
        alert('Please select a 3D model file to upload');
        e.preventDefault();
        return;
    }

    // Check file size (max 500MB)
    const maxSize = 500 * 1024 * 1024; // 500MB in bytes
    if (modelFileInput.files[0].size > maxSize) {
        alert('File size exceeds the maximum limit of 500MB');
        e.preventDefault();
        return;
    }

    // Check file extension
    const allowedExtensions = ['.obj', '.fbx', '.blend', '.stl', '.gltf', '.glb'];
    const fileName = modelFileInput.files[0].name.toLowerCase();
    const isValidExtension = allowedExtensions.some(ext => fileName.endsWith(ext));

    if (!isValidExtension) {
        alert('Please upload a file with one of the supported formats: .obj, .fbx, .blend, .stl, .gltf, .glb');
        e.preventDefault();
        return;
    }

    // Show loading state
    const submitBtn = document.querySelector('.submit-btn');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Uploading...';
    submitBtn.disabled = true;
    submitBtn.classList.remove('hover:-translate-y-1', 'hover:shadow-lg', 'hover:shadow-teal-400/20');
    submitBtn.classList.add('opacity-75', 'cursor-not-allowed');
});

// Reset form handler
uploadForm.addEventListener('reset', function () {
    setTimeout(() => {
        selectedFileDiv.classList.remove('block');
        selectedFileDiv.classList.add('hidden');
        fileUploadArea.classList.remove('border-teal-400', 'dragover', 'bg-teal-400/10');
        fileUploadArea.classList.add('border-gray-700');
    }, 10);
});

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function () {
    fileUploadArea.title = "Drag and drop files here or click to browse";

    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.success-message');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            message.style.transition = 'opacity 0.5s';
            setTimeout(() => {
                if (message.parentNode) {
                    message.parentNode.removeChild(message);
                }
            }, 500);
        }, 5000);
    });
});