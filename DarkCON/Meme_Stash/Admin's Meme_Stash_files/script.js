var slides = document.querySelectorAll(".slide");
var dots = document.querySelectorAll(".dot");
var index = 0;


function prevSlide(n){
  index+=n;
  console.log("prevSlide is called");
  changeSlide();
}

function nextSlide(n){
  index+=n;
  changeSlide();
}

changeSlide();

function changeSlide(){
    
  if(index>slides.length-1)
    index=0;
  
  if(index<0)
    index=slides.length-1;
 
  
      for(let i=0;i<slides.length;i++){
      slides[i].style.display = "none";    
      dots[i].classList.remove("active");
    }
    
    slides[index].style.display = "block";
    dots[index].classList.add("active");
}