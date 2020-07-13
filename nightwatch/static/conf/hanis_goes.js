var hansat = {
    debug: true,
    objname: "hsatObj",

    // in ms
    dwell: "150",
    pause: "1000",

    // in minutes
    auto_refresh: "2",

    image_base: "http://dctsleeperservice:9876/goes16/nows/",
    basename: "goes16_???.png",
    num_frames: "18",
    base_starting_number: "30",

    start_looping: "false, 18",

    window_size: "div",
    enable_smoothing: "true",

    // NOTE: For background images that are changing on the server, but
    //   have the same filename, you may specify the parameter
    background_static: "n",

    active_zoom: "true",
    maximum_zoom: "2.5",
    zoom_scale: "5",
    image_preserve: "0, 0, 700, 31",
    hide_top: "31, true",
    overlay_zoom: "n",

    controls: "startstop,speed,step,refresh,looprock,toggle",
    controls_style: "padding:5px; display:flex;",
    controls_tooltip: "Start/Stop, Speed Control, Single Step, Refresh, Rock Forwards/Backwards",

    buttons_style: "flex:auto; margin:2px;",

    toggle_size: "15, 10, 5",
    //             loaded    disabled current
    toggle_colors: "#011563, #990000, #3498db",
};
