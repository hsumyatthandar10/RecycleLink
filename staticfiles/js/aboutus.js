document.querySelectorAll('.faq-item').forEach((item) => {
    const toggleBtn = item.querySelector('.toggle-btn');
    const answer = item.querySelector('.faq-answer');
  
    toggleBtn.addEventListener('click', () => {
      const isExpanded = answer.style.display === 'block';
  
      // Reset all answers
      document.querySelectorAll('.faq-answer').forEach((ans) => (ans.style.display = 'none'));
      document.querySelectorAll('.toggle-btn').forEach((btn) => (btn.textContent = '+'));
  
      // Expand/Collapse the current answer
      if (!isExpanded) {
        answer.style.display = 'block';
        toggleBtn.textContent = '−';
      } else {
        answer.style.display = 'none';
        toggleBtn.textContent = '+';
      }
    });
  });
  /*numver*/
  const elements=document.querySelectorAll(".project .number")

const animationCounter=(element,target)=>{
    let step=target/100;
    let current=0

    const interval= setInterval(()=>{
        current +=step;
        if(current >=target){
            element.textContent=target
            //console.log("inside if")
            clearInterval(interval);
        }else{
            element.textContent=Math.ceil(current)
            //console.log("inside else")

        }
    },100)
}
const observer =new IntersectionObserver(entries =>{
    entries.forEach(entry=>{
        if(entry.isIntersecting){
            //console.log(entry)
            animationCounter(entry.target,entry.target.dataset.num)
        }
    })
},{threshold:0.5})
elements.forEach((element)=>{
    observer.observe(element)
})
 
