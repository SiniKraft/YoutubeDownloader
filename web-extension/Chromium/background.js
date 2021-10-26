function openPage() {
  let queryOptions = {
        active: true,
        currentWindow: true
    };
    chrome.tabs.query(queryOptions, function(tabs){
    var currentTabUrl = tabs[0].url;
    if (currentTabUrl.includes("youtube.com/watch?v=")) {
      // var iframe = document.createElement('iframe');
      // iframe.style.display = "none";
      // iframe.src = "nickloryoutubedl://" + currentTabUrl + "/";
      // document.body.appendChild(iframe);
      win = window.open("nickloryoutubedl://" + currentTabUrl + "/", '_blank');
     };
  });
}

chrome.browserAction.onClicked.addListener(openPage);