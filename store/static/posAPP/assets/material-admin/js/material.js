(function ($) {
  'use strict';

  mdc.autoInit();

  // Ripple for buttons
  var buttons = document.querySelectorAll('.mdc-button');
  for (var i = 0, button; button = buttons[i]; i++) {
    mdc.ripple.MDCRipple.attachTo(button);
  }

  // Focus for textfields
  var textFields = document.querySelectorAll('.mdc-text-field');
  for (var i = 0, textField; textField = textFields[i]; i++) {
    mdc.textField.MDCTextField.attachTo(textField);
  }

  // Menu handling
  const menuEls = Array.from(document.querySelectorAll('.mdc-menu'));
  menuEls.forEach((menuEl, index) => {
    const menu = new mdc.menu.MDCMenu(menuEl);
    const buttonEl = menuEl.parentElement.querySelector('.mdc-menu-button');
    buttonEl.addEventListener('click', () => {
      menu.open = !menu.open;
    })
    menu.setAnchorCorner(mdc.menu.Corner.BOTTOM_LEFT);
    menu.setAnchorElement(buttonEl)
  });

  // Tabs
  var tabBars = document.querySelectorAll('.mdc-tab-bar');
  for (var i = 0, tabBar; tabBar = tabBars[i]; i++) {
    var currentTabBar = new mdc.tabBar.MDCTabBar(tabBar);
    currentTabBar.listen('MDCTabBar:activated', function(event) {
      var $this = $(this);
      var contentEls = $this.siblings('.content');
      contentEls.map((index, contentEl) => {
        contentEl.classList.remove('content--active');
      })
      contentEls[event.detail.index].classList.add('content--active');
    });
  }

  // Sidebar navigation active state handling
  document.addEventListener('DOMContentLoaded', function() {
    // Get current path
    const currentPath = window.location.pathname;
    
    // Find all navigation items
    const navItems = document.querySelectorAll('.mdc-drawer-item');
    
    // Remove active class from all items first
    navItems.forEach(item => {
      item.classList.remove('mdc-drawer-item--activated');
    });
    
    // Find and activate the current item
    navItems.forEach(item => {
      const link = item.querySelector('.mdc-drawer-link');
      if (link) {
        const linkPath = new URL(link.href).pathname;
        if (linkPath === currentPath) {
          item.classList.add('mdc-drawer-item--activated');
        }
      }
    });
  });

})(jQuery);