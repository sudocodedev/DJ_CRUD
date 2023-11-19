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
      console.log(comments);
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
// }

// for opening the modal
document.querySelector(".delete").addEventListener("click", function () {
  document.querySelector(".bg-modal").style.display = "flex";
});

// for closing the modal
document.querySelector(".close").addEventListener("click", function () {
  document.querySelector(".bg-modal").style.display = "none";
});
