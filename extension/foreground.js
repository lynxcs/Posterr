const SITE_QUERY_INJECT = "body > main > div.mt-4.mt-md-5 > header > div > div > div > section > div.dark-pop.rounded.p-3.mt-2 > div.align-self-start.d-flex.flex-column.flex-md-row.justify-content-between.mt-2 > div.mt-2.btn-group.d-flex.d-md-inline-flex.flex-wrap";
const MOVIE_NAME_QUERY = "body > main > div.mt-4.mt-md-5 > header > div > div > div > section > div.w-100 > p > a";
const MEDIA_TYPE_QUERY = "body > main > div.mt-4.mt-md-5 > header > div > div > div > section > div.dark-pop.rounded.p-3.mt-2 > div:nth-child(3) > p";

const DOWNLOAD_LINK = document.querySelector(SITE_QUERY_INJECT + ":first-child > a").href;
const MOVIE_NAME = document.querySelector(MOVIE_NAME_QUERY).textContent;
const MEDIA_TYPE = document.querySelector(MEDIA_TYPE_QUERY).textContent.split(" ")[1];

let spanInfo = document.createElement('span');
spanInfo.className = "d-none";
spanInfo.innerHTML = "Upload to Posterr";

let iInfo = document.createElement('i');
iInfo.className = "fas fa-upload";

let aInfo = document.createElement('a');
aInfo.className="btn btn-outline-warning";
aInfo.setAttribute("data-toggle", "tooltip");
aInfo.setAttribute("data-placement", "top");
aInfo.setAttribute("title", "");
aInfo.setAttribute("data-original-title", "Upload to Posterr");

aInfo.appendChild(spanInfo);
aInfo.appendChild(iInfo);

document.querySelector(SITE_QUERY_INJECT).appendChild(aInfo);

aInfo.addEventListener('click', async _ => {
    chrome.runtime.sendMessage({
        message: "upload",
        url: DOWNLOAD_LINK,
        name: MOVIE_NAME,
        type: MEDIA_TYPE
    }, response => {
        if (response.message === "success") {
            console.log("Uploaded poster!");
        } else {
            console.log("Failed to upload poster!");
        }
    });
});

