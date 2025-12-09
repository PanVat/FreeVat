// Handle 3D model file selection
        const modelFileInput = document.getElementById('modelFile');
        const selectedModelFileDiv = document.getElementById('selectedModelFile');
        const modelFileNameSpan = document.getElementById('modelFileName');
        const modelFileUploadArea = document.getElementById('modelFileUploadArea');

        modelFileInput.addEventListener('change', function () {
            if (this.files.length > 0) {
                const file = this.files[0];
                modelFileNameSpan.textContent = file.name + ' (' + formatFileSize(file.size) + ')';
                selectedModelFileDiv.classList.remove('hidden');
                modelFileUploadArea.classList.add('border-teal-400');
                modelFileUploadArea.classList.remove('border-gray-700');
            } else {
                selectedModelFileDiv.classList.add('hidden');
                modelFileUploadArea.classList.remove('border-teal-400');
                modelFileUploadArea.classList.add('border-gray-700');
            }
        });

        // Handle preview image file selection
        const previewFileInput = document.getElementById('previewFile');
        const selectedPreviewFileDiv = document.getElementById('selectedPreviewFile');
        const previewFileNameSpan = document.getElementById('previewFileName');
        const previewFileUploadArea = document.getElementById('previewFileUploadArea');
        const imagePreviewContainer = document.getElementById('imagePreviewContainer');
        const imagePreview = document.getElementById('imagePreview');
        const removePreviewBtn = document.getElementById('removePreview');

        previewFileInput.addEventListener('change', function () {
            if (this.files.length > 0) {
                const file = this.files[0];
                previewFileNameSpan.textContent = file.name + ' (' + formatFileSize(file.size) + ')';

                // Show preview
                const reader = new FileReader();
                reader.onload = function (e) {
                    imagePreview.src = e.target.result;
                    imagePreviewContainer.classList.remove('hidden');
                    selectedPreviewFileDiv.classList.add('hidden');
                }
                reader.readAsDataURL(file);

                previewFileUploadArea.classList.add('border-blue-400');
                previewFileUploadArea.classList.remove('border-gray-700');
            } else {
                imagePreviewContainer.classList.add('hidden');
                selectedPreviewFileDiv.classList.add('hidden');
                previewFileUploadArea.classList.remove('border-blue-400');
                previewFileUploadArea.classList.add('border-gray-700');
            }
        });

        // Remove preview image
        removePreviewBtn.addEventListener('click', function () {
            previewFileInput.value = '';
            imagePreviewContainer.classList.add('hidden');
            selectedPreviewFileDiv.classList.add('hidden');
            previewFileUploadArea.classList.remove('border-blue-400');
            previewFileUploadArea.classList.add('border-gray-700');
        });

        // Format file size
        function formatFileSize(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        }

        // Form submission handler
        const uploadForm = document.getElementById('uploadForm');

        uploadForm.addEventListener('submit', function (e) {
            // Basic form validation
            const modelName = document.getElementById('id_model_name').value;
            const category = document.getElementById('id_category').value;
            const description = document.getElementById('id_description').value;

            if (!modelName || !category || !description) {
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
            const maxSize = 500 * 1024 * 1024;
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
                selectedModelFileDiv.classList.add('hidden');
                modelFileUploadArea.classList.remove('border-teal-400', 'dragover', 'bg-teal-400/10');
                modelFileUploadArea.classList.add('border-gray-700');

                imagePreviewContainer.classList.add('hidden');
                selectedPreviewFileDiv.classList.add('hidden');
                previewFileUploadArea.classList.remove('border-blue-400', 'dragover', 'bg-blue-400/10');
                previewFileUploadArea.classList.add('border-gray-700');

                // Reset preview file input
                previewFileInput.value = '';
            }, 10);
        });

        // Initialize
        document.addEventListener('DOMContentLoaded', function () {
            modelFileUploadArea.title = "Drag and drop 3D files here or click to browse";
            previewFileUploadArea.title = "Drag and drop image files here or click to browse";

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