document.getElementById('imageInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('inputImage').src = e.target.result;
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

        fetch('/process', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                document.getElementById('outputImage').src = data.output_image + '?t=' + new Date().getTime();
                alert(data.message);
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    }
});
