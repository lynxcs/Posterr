
document.querySelector("button").addEventListener('click', async _ => {
    try {
        const base_url = document.querySelector('input').value;
        chrome.runtime.sendMessage({
            message: "set_url",
            payload: base_url
        }, response => {
            if (response.message === "success") {
                console.log("Successfully set URL to " + base_url);
            }
        });
    } catch (err) {
        console.error(`Error: ${err}`);
    }
});
