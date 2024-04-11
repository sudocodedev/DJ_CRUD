if(document.getElementById('div_id_isDraft')){
    document.getElementById('div_id_isDraft').classList.add('form-switch');
}

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

//user follow
//get corresponding profile id
function getProfileID() {
    return document.querySelector(".screen").dataset.profileId;
}

function userFollow(id, holder) {
    const URL= `/followers/${id}/`;
    fetch(URL)
    .then(res => res.json())
    .then(data => {
      if(data.followed) {
        holder.textContent="Unfollow";
      } else {
        holder.textContent="Follow"
      }
    })
}
  
if(document.querySelector('.user-follow')) {
    let follow=document.querySelector('.user-follow');
    follow.addEventListener('click',() => {
        userFollow(getProfileID(), follow);
});
}