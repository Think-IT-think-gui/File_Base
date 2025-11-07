// Global object for shared functions and data.
window.ctrlbp = window.ctrlbp || {};

( function( $, document, ctrlbp ) {
	'use strict';

	// Selectors for all plugin inputs.
	ctrlbp.inputSelectors = 'input[class*="ctrlbp"], textarea[class*="ctrlbp"], select[class*="ctrlbp"], button[class*="ctrlbp"]';

	// Detect Gutenberg.
	ctrlbp.isGutenberg = document.body.classList.contains( 'block-editor-page' );

	// Generate unique ID.
	ctrlbp.uniqid = function uniqid() {
		return Math.random().toString( 36 ).substr( 2 );
	}

	// Trigger a custom ready event for all scripts to hook to.
	// Used for static DOM and dynamic DOM (loaded in MB Blocks extension for Gutenberg).
	ctrlbp.$document = $( document );
	$( function() {
		ctrlbp.$document.trigger( 'ctrlbp_ready' );
	} );
} )( jQuery, document, ctrlbp );