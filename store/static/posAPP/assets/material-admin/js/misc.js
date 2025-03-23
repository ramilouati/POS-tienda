(function ($) {
  'use strict';
  $(function () {
    var sidebar = $('.mdc-drawer-menu');
    var body = $('body');

    // Initialize the Material Design drawer
    if ($('.mdc-drawer').length) {
      var drawer = mdc.drawer.MDCDrawer.attachTo(document.querySelector('.mdc-drawer'));

      // Toggle drawer on sidebar-toggler click
      document.querySelector('.sidebar-toggler').addEventListener('click', function () {
        drawer.open = !drawer.open;
      });
    }

    // Collapse drawer for smaller screens
    if (window.matchMedia('(max-width: 991px)').matches) {
      if (document.querySelector('.mdc-drawer.mdc-drawer--dismissible').classList.contains('mdc-drawer--open')) {
        document.querySelector('.mdc-drawer.mdc-drawer--dismissible').classList.remove('mdc-drawer--open');
      }
    }

    // Add active class to nav-link based on URL dynamically
    var currentPath = window.location.pathname.replace(/^\/|\/$/g, ''); // Current path without leading/trailing slashes

    // Iterate through all sidebar links
    $('.mdc-drawer-item .mdc-drawer-link', sidebar).each(function () {
      var $this = $(this);
      var linkPath = $this[0].pathname.replace(/^\/|\/$/g, ''); // Path of the current link

      if (currentPath === "") {
        // For root URL (index.html)
        if (linkPath.endsWith("index.html")) {
          $this.addClass('active');
          if ($this.parents('.mdc-expansion-panel').length) {
            $this.closest('.mdc-expansion-panel').addClass('expanded');
          }
        }
      } else {
        // Match exact path
        if (currentPath === linkPath) {
          $this.addClass('active');
          if ($this.parents('.mdc-expansion-panel').length) {
            $this.closest('.mdc-expansion-panel').addClass('expanded');
            $this.closest('.mdc-expansion-panel').show();
          }
        }
      }
    });

    // Toggle sidebar items
    $('[data-toggle="expansionPanel"]').on('click', function () {
      // Close other items
      $('.mdc-expansion-panel').not($('#' + $(this).attr("data-target"))).hide(300);
      $('.mdc-expansion-panel').not($('#' + $(this).attr("data-target"))).prev('[data-toggle="expansionPanel"]').removeClass("expanded");

      // Open the clicked menu
      $('#' + $(this).attr("data-target")).slideToggle(300, function () {
        $('#' + $(this).attr("data-target")).toggleClass('expanded');
      });
    });

    // Add expanded class to mdc-drawer-link after expanding
    $('.mdc-drawer-item .mdc-expansion-panel').each(function () {
      $(this).prev('[data-toggle="expansionPanel"]').on('click', function () {
        $(this).toggleClass('expanded');
      });
    });

    // Apply PerfectScrollbar to the sidebar
    if (!body.hasClass("rtl")) {
      if ($('.mdc-drawer .mdc-drawer__content').length) {
        const chatsScroll = new PerfectScrollbar('.mdc-drawer .mdc-drawer__content');
      }
    }
  });
})(jQuery);
