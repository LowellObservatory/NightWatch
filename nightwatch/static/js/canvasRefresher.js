var uradict = {
    gate: "http://dctsleeperservice:9876/webcams/dct/thumb_gate.jpg",
    genset: "http://dctsleeperservice:9876/webcams/dct/thumb_genset.jpg",
    heliumcomp: "http://dctsleeperservice:9876/webcams/dct/thumb_heliumcomp.jpg",
    mezzanine: "http://dctsleeperservice:9876/webcams/dct/thumb_mezzanine.jpg",
    obslevel: "http://dctsleeperservice:9876/webcams/dct/thumb_obs_level.jpg",
    obsrot: "http://dctsleeperservice:9876/webcams/dct/thumb_obs_level_rot.jpg",
    telbldg: "http://dctsleeperservice:9876/webcams/dct/thumb_tel_bldg.jpg",
    domeroof: "http://dctsleeperservice:9876/webcams/dct/thumb_dome_roof.jpg",
    utilyard: "http://dctsleeperservice:9876/webcams/dct/thumb_util_yard.jpg",
    allsky: "http://dctsleeperservice:9876/webcams/dct/allsky.jpg",
}

var refreshInterval = 30000;
var drawDate = false;
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

function drawImageScaled(img, canvas, ctx) {
    // Props to https://stackoverflow.com/a/23105310
    //   GameAlchemist https://stackoverflow.com/users/856501/gamealchemist

    // Actually draw the image, scaling it down and centering it if necessary
    var hRatio = canvas.width/img.width;
    var vRatio =  canvas.height/img.height;
    var ratio  = Math.min(hRatio, vRatio);

    var centerShift_x = (canvas.width - img.width*ratio)/2;
    var centerShift_y = (canvas.height - img.height*ratio)/2;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // This will center the image in whatever padded area is now in the canvas
    ctx.drawImage(img, 0,0, img.width, img.height,
                       centerShift_x, centerShift_y,
                       img.width*ratio, img.height*ratio);

    if(drawDate) {
        var now = new Date();
        var text = now.toLocaleDateString() + " "
                    + now.toLocaleTimeString();

        // 0, 0 is the upper left coord
        var x = centerShift_x;
        var y = centerShift_y + 3*canvas.height/4;

        ctx.font = "20px Courier New";

        // Text outline
        ctx.strokeStyle = 'black';
        ctx.lineWidth = 2;
        ctx.strokeText(text, x, y);

        // Actual text
        ctx.fillStyle = 'white';
        ctx.fillText(text, x, y);
    }
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

            // Update the image/canvas stuff now and set up the onload func.
            //   Can only do this *after* the canvas is actually found
             newElem.img.onload = drawImageScaled.bind(null, newElem.img,
                                                             newElem.canvas,
                                                             newElem.ctx);
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
    console.log("Updated all webcam images! Timer reset.");
}

// Actually start the update process
init();
