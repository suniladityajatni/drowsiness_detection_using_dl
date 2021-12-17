let canvas=document.querySelector("#canvas");
let context=canvas.getContext("2d");
let video=document.querySelector("#video")
let result=document.getElementById("txt");

if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia)
{
  navigator.mediaDevices.getUserMedia({video: true}).then(function (stream) {
    video.srcObject = stream;
    video.play();
  });
}

document.getElementById("snap").addEventListener("click",()=>{
  context.drawImage(video,0,0,640,480);
  $.post("http://localhost:5000/api",
  {
      label:"video capture",
      content :canvas.toDataURL("image/png")
    },
    function(data,status){
        result.value=status + ":" +data;
    });
});




// var video = document.querySelector("#videoElement");

// if (navigator.mediaDevices.getUserMedia) {
//   navigator.mediaDevices.getUserMedia({ video: true })
//     .then(function (stream) {
//       video.srcObject = stream;
//       video.play();
//     })
//     .catch(function (err0r) {
//       console.log("Something went wrong!");
//     });
// }


// let canvas=document.querySelector("#canvas");
// let context=document.getContext("2d");

// document.getElementById("snap").addEventListener("click",function(){
//       context.drawImage(video,0,0,640,480);
//     });