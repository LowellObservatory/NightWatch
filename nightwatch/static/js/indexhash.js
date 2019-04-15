// external js: isotope.pkgd.js

// // filter functions
// var filterFns = {
//   // show if number is greater than 50
//   numberGreaterThan50: function() {
//     var number = $(this).find('.number').text();
//     return parseInt( number, 10 ) > 50;
//   },
//   // show if name ends with -ium
//   ium: function() {
//     var name = $(this).find('.name').text();
//     return name.match( /ium$/ );
//   }
// };

function getHashFilter() {
  // get filter=filterName
  var matches = location.hash.match( /filter=([^&]+)/i );
  var hashFilter = matches && matches[1];
  return hashFilter && decodeURIComponent( hashFilter );
}

// init Isotope
var $grid = $('.grid');

// bind filter button click
var $filterButtonGroup = $('.filter-button-group');
$filterButtonGroup.on( 'click', 'button', function() {
  var filterAttr = $( this ).attr('data-filter');
  // set filter in hash
  location.hash = 'filter=' + encodeURIComponent( filterAttr );
});

var isIsotopeInit = false;

function onHashchange() {
  var hashFilter = getHashFilter();

  // Check to see if we've already inited Isotope; if so, just return
  if ( !hashFilter && isIsotopeInit ) {
    return;
  }

  // If we haven't, say that we have and then set the options
  isIsotopeInit = true;

  // filter isotope
  $grid.isotope({
    // allow dynamic resizing of sizes and positions on window change
    // resize: true,

    // Animation time; 15 ms
    stagger: 15,

    // div class to actually act upon and arrange
    itemSelector: '.element-item',

    stamp: '.stamp',

    layoutMode: 'masonry',
    masonry: {
      // columnWidth: '.element-item',
      columnWidth: 10,
      // horizontalOrder: true,
      fitWidth: true,
      gutter: 0
    },

    // use filterFns
    filter: hashFilter
    // filter: filterFns[ hashFilter ] || hashFilter

  });
  // set selected class on button
  if ( hashFilter ) {
    $filterButtonGroup.find('.is-checked').removeClass('is-checked');
    $filterButtonGroup.find('[data-filter="' + hashFilter + '"]').addClass('is-checked');
  }
}

$(window).on( 'hashchange', onHashchange );

// trigger event handler to init Isotope; but wait for the images
onHashchange();
