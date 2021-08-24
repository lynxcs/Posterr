
chrome.runtime.onInstalled.addListener(() => {
    chrome.storage.local.set({
        base_url: "http://127.0.0.1:57272"
    });
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    // TODO: Switch to using declarative content api
    if (changeInfo.status === "complete" && /^https:\/\/theposterdb.com\/poster\/.*/.test(tab.url))
    {
        chrome.scripting.executeScript({
            target: { tabId: tabId },
            files: ["foreground.js"]
        }).then(() => {
            console.log("Injected foreground script!");
        }).catch(err => console.log(err));
    }
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.message === "get_url") {
        chrome.storage.local.get('base_url', data => {
            if (chrome.runtime.lastError) {
                sendResponse({
                    message: "fail"
                });
            }
            else {
                sendResponse({
                    message: "success",
                    payload: data.base_url
                });
            }
        });

        return true;
    }
    else if (request.message === "set_url") {
        if (request.payload != undefined) {
            console.log("Setting base url to " + request.payload)
            chrome.storage.local.set({
                base_url: request.payload
            });
            sendResponse({
                message: "success"
            });
        }
        return true;
    }
    if (request.message == "upload") {
        chrome.storage.local.get('base_url', data => {
            if (chrome.runtime.lastError) {
                sendResponse({
                    message: "fail"
                });
            }
            else {
                let formData = new FormData();
                formData.append("url", request.url);
                formData.append("name", request.name);
                formData.append("type", request.type);
                fetch(data.base_url + "/upload", {
                    method: 'post',
                    body: formData,
                    mode: "no-cors"
                }).then((response) => {
                    console.log('Completed!', response);
                    sendResponse({
                        message: "success",
                    });
                }).catch((err) => {
                    console.error(`Error: ${err}`);
                    sendResponse({
                        message: "fail",
                    });
                });
            }
        });

        return true;
    }
});