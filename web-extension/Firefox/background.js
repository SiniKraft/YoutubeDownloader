function openPage() {
  browser.tabs.query({active:true,currentWindow:true}).then(function(tabs){
    var currentTabUrl = tabs[0].url;
    if (currentTabUrl.includes("youtube.com/watch?v=")) {
      window.location.replace("nickloryoutubedl://" + currentTabUrl + "/");
    };
  });
}

browser.browserAction.onClicked.addListener(openPage);