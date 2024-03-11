function imageUpload(e, imgID) {
    const file = e.target.files[0];
    if(file){
        const reader = new FileReader();
        reader.onload = function(event) {
            const img = document.getElementById(imgID);
            if(img) {
                console.log("Img tag found");
                img.src = event.target.result;
                console.log("Img changed");
            } else {
                console.log("Img elt not found")
            }
        }
        reader.readAsDataURL(file);
    }
}

//post form
if(document.getElementById("post-pic-input")) {
    const img_input = document.getElementById("post-pic-input");
    img_input.addEventListener('change', (e) => {
        imageUpload(e,"preview");
    });
}

//user profile pic
if(document.getElementById('profile-pic-input')) {
    const profile_pic = document.getElementById('profile-pic-input');
    profile_pic.addEventListener('change', (e) => {
        imageUpload(e,"profile-pic-preview");
    });
}

// user profile bg pic
if(document.getElementById('bg-pic-input')) {
const bg_pic = document.getElementById('bg-pic-input');
bg_pic.addEventListener('change', (e) => {
    imageUpload(e,"bg-pic-preview");
});
}