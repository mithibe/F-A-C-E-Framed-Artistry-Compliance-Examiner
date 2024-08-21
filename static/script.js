let cropper;

document.getElementById('imageInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const inputImage = document.getElementById('inputImage');
            inputImage.src = e.target.result;

            // Initialize Cropper.js
            if (cropper) {
                cropper.destroy();
            }
            cropper = new Cropper(inputImage, {
                aspectRatio: 1, // Force square crop
                viewMode: 2,
            });

            document.getElementById('processButton').disabled = false;
        };
        reader.readAsDataURL(file);
    }
});

document.getElementById('processButton').addEventListener('click', function() {
    const file = document.getElementById('imageInput').files[0];
    if (file) {
        const formData = new FormData();
        formData.append('image', file);

        // Get crop data from Cropper.js
        const cropData = cropper.getData(true);
        formData.append('cropX', cropData.x);
        formData.append('cropY', cropData.y);
        formData.append('cropWidth', cropData.width);
        formData.append('cropHeight', cropData.height);

        fetch('/process', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                document.getElementById('outputImage').src = data.output_image + '?t=' + new Date().getTime();
                alert('Image processing completed!');
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    }
});
