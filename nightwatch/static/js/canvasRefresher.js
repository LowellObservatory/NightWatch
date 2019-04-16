var uradict = {
    gate: "http://dctsleeperservice:8080/webcams/dct/gate.jpg",
    genset: "http://dctsleeperservice:8080/webcams/dct/genset.jpg",
    heliumcomp: "http://dctsleeperservice:8080/webcams/dct/heliumcomp.jpg",
    obslevel: "http://dctsleeperservice:8080/webcams/dct/obs_level.jpg",
    telbldg: "http://dctsleeperservice:8080/webcams/dct/tel_bldg.jpg",
    utilyard: "http://dctsleeperservice:8080/webcams/dct/util_yard.jpg",
    allsky: "http://dct-allsky.lowell.edu/allsky/dct_allsky.jpg",
}

var refreshInterval = 30000;
var drawDate = true;
var validElements = [];

class refreshedImgObj {
    constructor(tag, url) {
        // Essentials; defined in the input dict (uradict)
        this.tag = tag;
        this.url = url;

        // Actual DOM references, to be found/filled elsewhere
        this.canvas = null;
        this.ctx = null;

        // Image stuff
        this.img = new Image();
        this.img.src = this.url;

        // Refresh interval in ms
        //   TODO: Actually implement this (somehow)
        this.interval = 30000;
    }
}

function setImgOnload(newElem){
  // Can only do this *after* the canvas is actually found
  // Set the onload behavior of this particular img block
  newElem.img.onload = function() {
    newElem.canvas.setAttribute("width", newElem.img.width)
    newElem.canvas.setAttribute("height", newElem.img.height)
    newElem.ctx.drawImage(newElem.img, 0, 0);
    if(drawDate) {
        var now = new Date();
        var text = now.toLocaleDateString() + " "
                    + now.toLocaleTimeString();
        var maxWidth = 150;
        var x = newElem.img.width-50-maxWidth;
        var y = newElem.img.height-50;
        newElem.ctx.font = "20px Courier New";
        newElem.ctx.strokeStyle = 'black';
        newElem.ctx.lineWidth = 2;
        newElem.ctx.strokeText(text, x, y, maxWidth);
        newElem.ctx.fillStyle = 'white';
        newElem.ctx.fillText(text, x, y, maxWidth);
    }
  };
  return newElem;
}

function init() {
    // A jQuery style foreach; really an array and a callback but whatevs
    $.each(uradict, function(key, value) {
        // In case you need to see the key/value pairs
        // console.log(key, value);

        // Define the particular canvas for this element/key; will
        //   be saved in a class so it can be properly called later
        var canvas = document.getElementById(key);

        if (canvas == null){
            // console.log("Canvas element", key, "not found!");
        } else {
            // console.log("Canvas element", key, "found!!");
            newElem = new refreshedImgObj(key, value);
            newElem.canvas = canvas;

            // Remember to reference newElem.canvas/newElem.ctx henceforth
            newElem.ctx = newElem.canvas.getContext("2d");

            // Update the image/canvas stuff now and set up the onload func
            newElem = setImgOnload(newElem);
            validElements.push(newElem);
        }
    });
    refreshAllImgs();
}

function refreshAllImgs() {
    $.each(validElements, function(idx, value) {
        // console.log(idx, value.tag)
        value.img.src = value.url + "?t=" + new Date().getTime();
    });
    setTimeout("refreshAllImgs()", refreshInterval);
    console.log("Updated all images! Timer reset.");

}