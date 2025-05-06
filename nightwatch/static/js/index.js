// init Isotope
var $grid = $('.grid').isotope({
  // 'false' disables the initial layout
  isInitLayout: false,
  stagger: 30,
  itemSelector: '.element-item',

  layoutMode: 'masonry',
  masonry: {
    columnWidth: 5,
    gutter: 2,
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

  // Handle special case of "*" filter in the laziest way possible
  if ($activeButt == "*") {
    return true
  }

  const isElementInCurrentGroup = groups.indexOf($activeButt) !== -1;
  // Only search elements in the current group
  if (!isElementInCurrentGroup) {
    return false;
  } else {
    return true;
  }
}

// jQuery loop over all elements inside the 'btn-group' class.
//   This will change the "active" class on the button that was clicked on
//   and remove it from all the rest to show indication for navigation.
//
// NOTE: Need to keep this *above* the actual onclick assignment below.
//   Otherwise, the filter event will be fired before changing the 'active'
//   class on the button, which will cause the layout to be filtered based
//   on the *previous* value and not the new one.  Tricksy.
// TODO: Just combine the two into a single deal to avoid this
//   potential order of operations deal.
$('.btn-group').each(function(i, buttonGroup ) {
  var $buttonGroup = $(buttonGroup);
  $buttonGroup.on('click', 'button', function() {
    $buttonGroup.find('.active').removeClass('active');
    $(this).addClass('active');
  });
});

// jQuery loop over all elements that have the 'filters-group' class.
//   This binds a click on a 'button' inside that group to an actual call
//   to Isotope to filter based on the value/group specified in the 'button'
//   that was clicked on, via the "data-filter" attribute on the button itself
$('.filters-group').on('click', 'button', function() {
  $grid.isotope();
});


// Calling isotope() with no arguments triggers arrange(),
//   which applies both filtering and sorting.
//   isotope('layout') does neither of those, but can handle size changes.
$grid.isotope();
