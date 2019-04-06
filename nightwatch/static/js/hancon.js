var hancon = {
    dwell : "200",
    pause : "2000",
    auto_refresh : "1",

    image_base : "http://nightwatch.lowell.edu/goes16/nows/",
    basename : "goes_latest_???.png",
    num_frames : "24",
    base_starting_number: "23",

    // filenames: "goes_latest_023.png, goes_latest_024.png, goes_latest_025.png, goes_latest_026.png, goes_latest_027.png, goes_latest_028.png, goes_latest_029.png, goes_latest_030.png, goes_latest_031.png, goes_latest_032.png, goes_latest_033.png, goes_latest_034.png, goes_latest_035.png, goes_latest_036.png, goes_latest_037.png, goes_latest_038.png, goes_latest_039.png, goes_latest_040.png, goes_latest_041.png, goes_latest_042.png, goes_latest_043.png, goes_latest_044.png, goes_latest_045.png, goes_latest_046.png, goes_latest_047.png",
    // NOTE: For background images that are changing on the server, but
    //   have the same filename, you may specify the parameter
    background_static : "n",

    controls : "startstop,speed,step,refresh,looprock,toggle",
    controls_style : "padding:5px;background-color:green;",
    // controls_tooltip : "Start/Stop the animation, Step one frame, Refresh images",
  };