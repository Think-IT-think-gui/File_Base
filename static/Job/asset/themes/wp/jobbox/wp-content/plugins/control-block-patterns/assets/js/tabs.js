( function ( window, document, $ ) {
	'use strict';

	function switchTab() {
		$( '.ctrlbp-tab-nav' ).on( 'click', 'a', e => {
			e.preventDefault();
			showTab( e.target );
		} );
	}

	function showTab( el ) {
		var tab = el.closest( 'li' ).dataset.panel,
			$wrapper = $( el ).closest( '.ctrlbp-tabs' ),
			$tabs = $wrapper.find( '.ctrlbp-tab-nav > li' ),
			$panels = $wrapper.find( '.ctrlbp-tab-panel' );

		$tabs.removeClass( 'ctrlbp-tab-active' ).filter( '[data-panel="' + tab + '"]' ).addClass( 'ctrlbp-tab-active' );
		$panels.hide().filter( '.ctrlbp-tab-panel-' + tab ).show();

		// Refresh maps, make sure they're fully loaded, when it's in hidden div (tab).
		$( window ).trigger( 'ctrlbp_map_refresh' );
	}

	// Set active tab based on visible pane to better works with Meta Box Conditional Logic.
	function tweakForConditionalLogic() {
		if ( $( '.ctrlbp-tab-active' ).is( 'visible' ) ) {
			return;
		}

		// Find the active pane.
		var activePane = $( '.ctrlbp-tab-panel[style*="block"]' ).index();
		if ( activePane >= 0 ) {
			$( '.ctrlbp-tab-nav li' ).removeClass( 'ctrlbp-tab-active' ).eq( activePane ).addClass( 'ctrlbp-tab-active' );
		}
	}

	function showValidateErrorFields() {
		var inputSelectors = 'input[class*="ctrlbp-error"], textarea[class*="ctrlbp-error"], select[class*="ctrlbp-error"], button[class*="ctrlbp-error"]';
		$( document ).on( 'after_validate', 'form', e => {
			var $input = $( e.target ).find( inputSelectors );
			showTab( $input, $input.closest( '.ctrlbp-tab-panel' ).data( 'panel' ) );
		} );
	}

	$( function() {
		switchTab();
		tweakForConditionalLogic();
		showValidateErrorFields();

		$( '.ctrlbp-tab-active a' ).trigger( 'click' );

		// Remove wrapper. Use Meta Box's seamless style.
		$( '.ctrlbp-tabs-no-wrapper' ).closest( '.postbox' ).removeClass( 'ctrlbp-default' ).addClass( 'ctrlbp-seamless' );
	} );
} )( window, document, jQuery );
