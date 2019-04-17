// init Isotope
var $grid = $('.grid').isotope({
    itemSelector: '.element-item',
    layoutMode: 'masonry',
    masonry: {
      columnWidth: 50,
    },
});

// bind filter button click
$('.filters-group').on( 'click', 'button', function() {
  var filterValue = $( this ).attr('data-filter');
  $grid.isotope({ filter: filterValue });
});

// change is-checked class on buttons
$('.btn-group').each( function( i, buttonGroup ) {
  var $buttonGroup = $( buttonGroup );
  $buttonGroup.on( 'click', 'button', function() {
    $buttonGroup.find('.active').removeClass('active');
    $( this ).addClass('active');
  });
});

// For the first run thru, sort by the default/home/active button
//   ... but first we have to find which one that is.
var $activeButt;

$('.btn-group').each( function( i, buttonGroup ) {
  var $buttonGroup = $( buttonGroup );
  $activeButt = $buttonGroup.find('.active');
});

var filterValue = $activeButt.attr('data-filter');
$grid.isotope({ filter: filterValue });
