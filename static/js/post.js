const img_input = document.getElementById("post-pic-input");

img_input.addEventListener('change',(e) => {
    const file=e.target.files[0];
    if(file){
        const reader = new FileReader();
        reader.onload = function(event) {
            const nextSibling = e.target.nextElementSibling;
            const img = nextSibling && nextSibling.querySelector('img');
            if(img){
                img.src = event.target.result;
            } else {
                console.log("Img elt not found");
            }
        }
        reader.readAsDataURL(file);
    }
});