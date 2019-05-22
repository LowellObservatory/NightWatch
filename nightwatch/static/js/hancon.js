var hansat = {
    // in ms
    dwell: "150",
    pause: "2000",

    // in minutes
    auto_refresh: "5",

    image_base: "http://dctsleeperservice:9876/goes16/nows/",
    basename: "goes_latest_???.png",
    num_frames: "24",
    base_starting_number: "23",

    window_size: "div",

    // NOTE: For background images that are changing on the server, but
    //   have the same filename, you may specify the parameter
    background_static: "n",

    active_zoom: "true",
    maximum_zoom: "2.5",
    image_preserve: "0, 0, 700, 31",
    hide_top: "31, true",
    overlay_zoom: "n",

    controls: "startstop,speed,step,refresh,looprock,toggle",
    controls_style: "padding:10px; display:flex;",
    controls_tooltip: "Start/Stop, Speed Control, Single Step, Refresh, Rock Forwards/Backwards",

    buttons_style: "flex:auto; margin:3px;",

    toggle_size: "15, 10, 5",
    toggle_colors: "#005914, red, orange",
};

var hanrad = {
    // in ms
    dwell: "150",
    pause: "2000",

    // in minutes
    auto_refresh: "5",

    image_base: "http://dctsleeperservice:9876/nexrad/nows/",
    basename: "nexrad_latest_???.png",
    num_frames: "24",
    base_starting_number: "23",

    window_size: "div",

    // NOTE: For background images that are changing on the server, but
    //   have the same filename, you may specify the parameter
    background_static: "n",

    active_zoom: "true",
    maximum_zoom: "2.5",
    image_preserve: "0, 0, 700, 31",
    hide_top: "31, true",
    overlay_zoom: "n",

    controls: "startstop,speed,step,refresh,looprock,toggle",
    controls_style: "padding:10px; display:flex;",
    controls_tooltip: "Start/Stop, Speed Control, Single Step, Refresh, Rock Forwards/Backwards",

    buttons_style: "flex:auto; margin:3px;",

    toggle_size: "15, 10, 5",
    toggle_colors: "#005914, red, orange",
};
