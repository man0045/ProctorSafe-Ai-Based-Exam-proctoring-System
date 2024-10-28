document.addEventListener("DOMContentLoaded", () => {
 const video = document.getElementById("video");
 const canvas = document.getElementById("canvas");
 const captureBtn = document.getElementById("capture-btn");
 const capturedImage = document.getElementById("captured_image");

 navigator.mediaDevices.getUserMedia({ video: true })
     .then(stream => {
         video.srcObject = stream;
     })
     .catch(error => {
         console.error("Error accessing the camera", error);
     });

 captureBtn.addEventListener("click", () => {
     canvas.style.display = "block";
     canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);
     
     const imageData = canvas.toDataURL("image/png");
     capturedImage.value = imageData;
 });
});
