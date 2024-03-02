//page up & down detection
let content=document.querySelector(".post-layout-main");
let lastScrollTop=0;

function scrollTopPage(){
  let navigator=document.querySelector(".post-layout-navigator");
  let currentScrollTop=content.scrollTop;
  if(currentScrollTop>=150){
    navigator.classList.remove("hide-display");
  } else {
    navigator.classList.add("hide-display");
  }
  lastScrollTop= currentScrollTop<=0 ? 0: currentScrollTop;
}

content.addEventListener('scroll',scrollTopPage);

//scroll to top of the page
const moveToTop=document.querySelector(".post-layout-navigator");
moveToTop.addEventListener('click', (e) => {
  const main_view=document.getElementById('main-view');
  main_view.scrollTo({top: 0, behaviour:"smooth"});
});

//scroll to comment section
const comment_button = document.querySelector('.fa-comment');
comment_button.addEventListener('click',(e) => {
  const target_view=document.getElementById('target-view');
  target_view.scrollIntoView({behaviour:"smooth", block:"start"});
});

function LoadComments() {
  // load all the comments in desc order for the selected post
  let comment_section = document.querySelector(".load-comments");
  let postid = getPostID();
  let URL = `/comments/${postid}/`;

  fetch(URL)
    .then((res) => res.json())
    .then((data) => {
      let comments = JSON.parse(data);
      let info = `<h3 style="font-weight:bold; font-size: 2rem; padding: 5px;">Comments (${comments.length})</h3>`;
      comments.forEach((comment) => {
        info += `
            <div class="comment-block">
                <span class="user">${comment["fields"]["user"]}</span> • <span class="timestamp">${comment["fields"]["str_comment_posted"]}</span>
                <br>
                <p>${comment["fields"]["body"]}</p>
                <div class="comment-reply">
                    <div><i class="fa-regular fa-heart like-button" data-post-id=""></i><span>0</span></div>
                    <div><i class="fa-regular fa-comment"></i><span>0</span></div>                    
                    <div>Reply</div>
                </div>
            </div>
        `;
      });
      comment_section.innerHTML = info;
    })
    .catch((error) => {
      console.log(error);
    });
}

//get corresponding post id
function getPostID() {
  return document.querySelector(".content").dataset.postId;
}

LoadComments();

// function PostComment() {
if(document.querySelector("#post-comment")) {
  const form = document.querySelector("#post-comment");
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const comment_text = document.getElementById("comment-text").value;
    let postid = getPostID();
    let URL = `/post-comment/${postid}/`;
    const csrftoken = document.querySelector(
      "input[name=csrfmiddlewaretoken]",
    ).value;
    let fetch_details = {
      method: "POST",
      headers: new Headers({
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": csrftoken,
      }),
      body: `text=${comment_text}`,
    };
    fetch(URL, fetch_details)
      .then((res) => res.json())
      .then((data) => {
        if (data.status === "success") {
          document.getElementById("comment-text").value = "";
          LoadComments();
        } else {
          console.error("comment submission failed!");
        }
      })
      .catch((error) => {
        console.error("Fetch Error: ", error);
      });
  });
}

// for opening the modal
document.querySelector(".delete").addEventListener("click", function () {
  document.querySelector(".bg-modal").style.display = "flex";
});

// for closing the modal
document.querySelector(".close").addEventListener("click", function () {
  document.querySelector(".bg-modal").style.display = "none";
});
