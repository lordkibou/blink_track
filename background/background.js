let mediaRecorder;
//  I need a function to record webcam video capture, and this one which sends every minute 1 a video to the AWS
//----------------------------------------------------------------
//    Video Source Webcam----> startRecording()------------->   responseData : JSON{count: Integer}  || error: String
//----------------------------------------------------------------
async function startRecording() {
    try {
      const userMediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
      
      const videoElement = document.createElement('video');
      document.body.appendChild(videoElement);
      videoElement.srcObject = userMediaStream;
      videoElement.play();
  
      mediaRecorder = new MediaRecorder(userMediaStream);
    
    //--------------------------------------------------------------------
    // Client side call to API server
      mediaRecorder.ondataavailable = async (event) => {
        if (event.data.size > 0) {
          const formData = new FormData();
          formData.append('video', event.data);
  
          try {
            const response = await fetch('https://your-api-endpoint.com/upload', {
              method: 'POST',
              body: formData,
            });
  
            const responseData = await response.json();
            console.log('API response:', responseData);

            return responseData // Return the data that will help us show the count inside of the popup
          } catch (error) {
            console.error('Error sending video:', error);
          }
        }
      };
    //--------------------------------------------------------------------
        
      mediaRecorder.start();
  
      mediaRecorder.onstop = () => {
        userMediaStream.getTracks().forEach(track => track.stop());
      };
    } catch (error) {
      console.error('Error accessing webcam:', error);
      return error
    }
}