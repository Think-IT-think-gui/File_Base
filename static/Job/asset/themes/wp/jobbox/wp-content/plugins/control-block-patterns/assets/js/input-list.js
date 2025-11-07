( function ( $, ctrlbp ) {
	'use strict';

	function toggleTree() {
		var $this = $( this ),
			$children = $this.closest( 'li' ).children( 'ul' );

		if ( $this.is( ':checked' ) ) {
			$children.removeClass( 'hidden' );
		} else {
			$children.addClass( 'hidden' ).find( 'input' ).prop( 'checked', false );
		}
	}

	function toggleAll( e ) {
		e.preventDefault();

		var $this = $( this ),
			checked = $this.data( 'checked' );

		if ( undefined === checked ) {
			checked = true;
		}

		$this.parent().siblings( '.ctrlbp-input-list' ).find( 'input' ).prop( 'checked', checked ).trigger( 'change' );

		checked = ! checked;
		$this.data( 'checked', checked );
	}

	function init( e ) {
		$( e.target ).find( '.ctrlbp-input-list.ctrlbp-collapse input[type="checkbox"]' ).each( toggleTree );
	}

	ctrlbp.$document
		.on( 'ctrlbp_ready', init )
		.on( 'change', '.ctrlbp-input-list.ctrlbp-collapse input[type="checkbox"]', toggleTree )
		.on( 'clone', '.ctrlbp-input-list.ctrlbp-collapse input[type="checkbox"]', toggleTree )
		.on( 'click', '.ctrlbp-input-list-select-all-none', toggleAll );
} )( jQuery, ctrlbp );
