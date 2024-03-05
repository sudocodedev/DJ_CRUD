//top 3 trending posts based on likes
function top3Posts(){
  const URL='/trending-posts/';
  fetch(URL)
  .then(res => res.json())
  .then(data => {
    let top_posts = data.picks;
    console.log(top_posts);
    let holder=document.querySelector('.controls .trending');
    holder.innerHTML += `
      <div style="width: 100%; padding: 10px 5px 10px 16px; margin:1px 0 3px 0; border-radius: 15px; background-color: rgb(229, 228, 226); font-weight: bold;"><span style="font-size: 1.5rem;">🥇</span> <a style="text-decoration:none; color: #000;" href="/detailed-post/${Number(top_posts[0].id)}">${top_posts[0].title}</a></div>
      <div style="width: 100%; padding: 10px 5px 10px 16px; margin:1px 0 3px 0; border-radius: 15px; background-color: rgb(229, 228, 226); font-weight: bold;"><span style="font-size: 1.5rem;">🥈</span> <a style="text-decoration:none; color: #000;" href="/detailed-post/${Number(top_posts[1].id)}">${top_posts[1].title}</a></div>
      <div style="width: 100%; padding: 10px 5px 10px 16px; margin:1px 0 3px 0; border-radius: 15px; background-color: rgb(229, 228, 226); font-weight: bold;"><span style="font-size: 1.5rem;">🥉</span> <a style="text-decoration:none; color: #000;" href="/detailed-post/${Number(top_posts[2].id)}">${top_posts[2].title}</a></div>
    `;
    
  })
}

top3Posts();

//like, bookmark status check during initial page load for new user
function statusCheck(id){
  const URL = `/post-status/${id}/`;
  fetch(URL)
  .then(res => res.json())
  .then(data => {
    let post_like_button = document.querySelector('.post-like-button');
    let post_bookmark_button = document.querySelector('.post-bookmark-button');

    //initial like status
    if(data.like_check){
      if(post_like_button.classList.contains('fa-regular')){
        post_like_button.classList.remove('fa-regular');
      }
      post_like_button.classList.add('fa-solid');
      post_like_button.style.color="rgb(255, 3, 62)";
    } 
    else {
      if(post_like_button.classList.contains('fa-solid')){
        post_like_button.classList.remove('fa-solid');
      }
      post_like_button.classList.add('fa-regular');
      post_like_button.style.color="rgb(230, 230, 230)";
    }

    //initial bookmark status
    if(data.bookmark_check){
      if(post_bookmark_button.classList.contains('fa-regular')){
        post_bookmark_button.classList.remove('fa-regular');
      }
      post_bookmark_button.classList.add('fa-solid');
      post_bookmark_button.style.color="rgb(255, 192, 0)";
    } 
    else {
      if(post_bookmark_button.classList.contains('fa-solid')){
        post_bookmark_button.classList.remove('fa-solid');
      }
      post_bookmark_button.classList.add('fa-regular');
      post_bookmark_button.style.color="rgb(230, 230, 230)";
    }
  })
}

function clearNotification(){
  let popup=document.querySelector('.toast-notification');
  setTimeout(()=>{
    popup.style.display='none';
  }, 2000);
}

//action notification
function actionNotification(msg) {
  let message=document.querySelector('.post-layout-main');
  message.insertAdjacentHTML('afterbegin', msg);
  clearNotification();
} 

//like & unlike a post
function likedPost(id, holder) {
  const URL=`/like-post/${id}/`;
  fetch(URL)
  .then(res => res.json())
  .then(data => {
    let l_color=''; //color to be applied if user liked the post
    let temp=''; //style to applied if user liked the post
    let b_style=''; //style to removed if user liked the post
    let message='';

    //Deciding which color & style to pick for like or unlike
    if(data.liked){
      l_color="rgb(255, 3, 62)"; 
      b_style="fa-solid"; 
      temp="fa-regular"; 
      message = `
        <div class="toast-notification alert alert-primary alert-dismissible fade show" role="alert"  style="position: absolute; z-index:12; margin-left: 80%; margin-top: 20px;">
          <strong>Wow!</strong>,  you liked this post 👍🏻.
          <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>  
        </div>`;
        actionNotification(message);
    } else {
      l_color="rgb(230, 230, 230)";
      b_style="fa-regular";
      temp="fa-solid";
    }

    localStorage.setItem("side_bar_icon_style",b_style);
    localStorage.setItem('liked_color',l_color);
    holder.classList.remove(temp);
    holder.classList.add(b_style);
    holder.style.color = l_color;
    document.querySelector('.post-likes-count').textContent=data.like_count;
  })
}

let post_like_button = document.querySelector('.post-like-button');

post_like_button.addEventListener('click', ()=>{
  const post_id=getPostID();
  likedPost(post_id,post_like_button)
});


//bookmark a post for future reference
function bookmarkPost(id, holder){
  const URL = `/bookmark-post/${id}/`;
  fetch(URL)
  .then(res => res.json())
  .then(data => {
    let b_color=''; //color to be applied if user liked the post
    let temp=''; //style to applied if user liked the post
    let b_style=''; //style to removed if user liked the post
    let message='';

    //Deciding which color & style to be applied if user bookmarked the post or not
    if(data.bookmarked){
      b_color="rgb(255, 192, 0)";
      temp="fa-regular";
      b_style="fa-solid";
      message = `
        <div class="toast-notification alert alert-success alert-dismissible fade show" role="alert"  style="position: absolute; z-index:12; margin-left: 80%; margin-top: 20px;">
          <strong>Great!!</strong>,  you liked this post 📑.
          <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>  
        </div> `;
        actionNotification(message);
    } else {
      b_color="rgb(230, 230, 230)";
      temp="fa-solid";
      b_style="fa-regular";
    }
    localStorage.setItem("bookmarked_color",b_color);
    localStorage.setItem("side_bar_icon_style",b_style);
    holder.style.color=b_color;
    holder.classList.remove(temp);
    holder.classList.add(b_style);
    document.querySelector('.post-bookmark-count').textContent=data.bookmark_counts;
  })
}

// let b_color = localStorage.getItem('bookmarked_color') || "rgb(230,230,230)";
let post_bookmark_button = document.querySelector('.post-bookmark-button');

// post_bookmark_button.style.color = b_color;
// post_bookmark_button.classList.add(icon_style);

post_bookmark_button.addEventListener('click', ()=> {
  const post_id=getPostID();
  bookmarkPost(post_id, post_bookmark_button);
});

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
statusCheck(getPostID());

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
