(function ($) {
  'use strict';
  $(function () {
    var sidebar = $('.mdc-drawer-menu');
    var body = $('body');

    // Initialize the Material Design drawer
    if ($('.mdc-drawer').length) {
      var drawer = mdc.drawer.MDCDrawer.attachTo(document.querySelector('.mdc-drawer'));

      // Toggle drawer on sidebar-toggler click
      $('.sidebar-toggler').on('click', function () {
        drawer.open = !drawer.open;
      });
    }

    // Collapse drawer for smaller screens
    if (window.matchMedia('(max-width: 991px)').matches) {
      $('.mdc-drawer.mdc-drawer--dismissible.mdc-drawer--open').removeClass('mdc-drawer--open');
    }

    // Improved active state handling for navigation items
    function setActiveNavItem() {
      var currentPath = window.location.pathname;
      
      // Remove all active classes first
      $('.mdc-drawer-item .mdc-drawer-link').removeClass('active');
      $('.mdc-drawer-item').removeClass('mdc-drawer-item--activated');
      
      // Find and activate the matching item
      $('.mdc-drawer-item .mdc-drawer-link').each(function () {
        var $link = $(this);
        var linkPath = this.pathname;
        
        // Check for exact match or if current path starts with link path
        if (currentPath === linkPath || currentPath.startsWith(linkPath)) {
          $link.addClass('active');
          $link.closest('.mdc-drawer-item').addClass('mdc-drawer-item--activated');
          
          // If this is inside an expansion panel, expand it
          var $panel = $link.closest('.mdc-expansion-panel');
          if ($panel.length) {
            $panel.addClass('expanded').show();
            $panel.prev('[data-toggle="expansionPanel"]').addClass('expanded');
          }
          
          // Since we found a match, we can stop checking
          return false;
        }
      });
    }

    // Call the function on page load
    setActiveNavItem();

    // Toggle sidebar items
    $('[data-toggle="expansionPanel"]').on('click', function (e) {
      e.preventDefault();
      var $this = $(this);
      var target = $this.attr('data-target');
      
      // Close other items
      $('.mdc-expansion-panel').not('#' + target).hide(300);
      $('[data-toggle="expansionPanel"]').not($this).removeClass('expanded');
      
      // Toggle current item
      $('#' + target).slideToggle(300);
      $this.toggleClass('expanded');
    });

    // Apply PerfectScrollbar to the sidebar
    if (!body.hasClass("rtl") && $('.mdc-drawer .mdc-drawer__content').length) {
      new PerfectScrollbar('.mdc-drawer .mdc-drawer__content');
    }

    // Re-check active state when navigating (for SPA-like behavior)
    $(document).on('click', '.mdc-drawer-link', function() {
      setTimeout(setActiveNavItem, 100); // Small delay to allow URL to change
    });
  });
})(jQuery);