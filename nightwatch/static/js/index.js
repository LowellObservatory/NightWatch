// init Isotope
var $grid = $('.grid').isotope({
  // disables initial layout
  isInitLayout: false,

  itemSelector: '.element-item',

  layoutMode: 'masonry',
  masonry: {
    columnWidth: 50,
  },

  // If filter is set to a function, that function checks each
  //   item (specified by itemSelector) and returns
  //   true or false if the item should be shown or hidden.
  filter: filtFunc,
});

function filtFunc() {
  // Find the active filter
  var $activeButt;
  $('.btn-group').each( function( i, buttonGroup ) {
    var $buttonGroup = $( buttonGroup );
    $activeButt = $buttonGroup.find('.active').attr('data-filter');
  });

  // Loop over each relevant element and see if it matches the active filter
  const groups = JSON.parse($(this).attr('data-groups'));
  const isElementInCurrentGroup = groups.indexOf($activeButt) !== -1;
  // Only search elements in the current group
  if (!isElementInCurrentGroup) {
    return false;
  } else {
    return true;
  }
}

// jQuery loop over all elements that have the 'filters-group' class.
//   This binds a click on a 'button' inside that group to an actual call
//   to Isotope to filter based on the value/group specified in the 'button'
//   that was clicked on, via the "data-filter" attribute on the button itself
$('.filters-group').on( 'click', 'button', function() {
  $grid.isotope();
});

// jQuery loop over all elements inside the 'btn-group' class.
//   This will change the "active" class on the button that was clicked on
//   and remove it from all the rest to show indication for navigation.
$('.btn-group').each( function( i, buttonGroup ) {
  var $buttonGroup = $( buttonGroup );
  $buttonGroup.on( 'click', 'button', function() {
    $buttonGroup.find('.active').removeClass('active');
    $( this ).addClass('active');
  });
});

// Calling isotope() with no arguments triggers arrange(),
//   which applies both filtering and sorting.
//   isotope('layout') does neither of those, but can handle size changes.
$grid.isotope();
