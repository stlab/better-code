const Plugin = {

	id: 'mark',

	MARK_STEP_DELIMITER: '|',
	MARK_LINE_DELIMITER: ',',
	MARK_LINE_RANGE_DELIMITER: '-',

    Mark: window.Mark,

	/**
	 * Marks blocks withing the given deck.
	 *
	 * Note that this can be called multiple times if
	 * there are multiple presentations on one page.
	 *
	 * @param {Reveal} reveal the reveal.js instance
	 */
	init: function( reveal ) {

		// Read the plugin config options and provide fallbacks
		let config = reveal.getConfig().mark || {};
		config.markOnLoad = typeof config.markOnLoad === 'boolean' ? config.markOnLoad : true;

		Array.from( reveal.getRevealElement().querySelectorAll( '[data-mark]' ) ).forEach( block => {

			if( config.markOnLoad ) {
				Plugin.markBlock( block );
			}

		} );

		// If we're printing to PDF, scroll the code marks of
		// all blocks in the deck into view at once
		reveal.on( 'pdf-ready', function() {
			[].slice.call( reveal.getRevealElement().querySelectorAll( '[data-mark].current-fragment' ) ).forEach( function( block ) {
				Plugin.scrollMarkedLineIntoView( block, {}, true );
			} );
		} );

	},

	/**
	 * Marks a block having the data-mark attribute.
	 *
	 * If the block contains multiple line mark steps,
	 * we clone the block and create a fragment for each step.
	 */
	markBlock: function( block ) {

		if( block.hasAttribute( 'data-mark' ) ) {

			var scrollState = { currentBlock: block };

			// If there is more than one mark step, generate
			// fragments
			var markSteps = Plugin.deserializeMarkSteps( block.getAttribute( 'data-mark' ) );
			if( markSteps.length > 1 ) {

				// If the original block has a fragment-index,
				// each clone should follow in an incremental sequence
				var fragmentIndex = parseInt( block.getAttribute( 'data-fragment-index' ), 10 );

				if( typeof fragmentIndex !== 'number' || isNaN( fragmentIndex ) ) {
					fragmentIndex = null;
				}

				// Generate fragments for all steps except the original block
				markSteps.slice(1).forEach( function( mark ) {

                    var fragmentBlock = block.cloneNode( true );
                    fragmentBlock.setAttribute( 'data-mark', Plugin.serializeMarkSteps( [ mark ] ) );
                    fragmentBlock.classList.add( 'fragment' );
                    block.parentNode.insertBefore( fragmentBlock, block.nextSibling );
                    Plugin.markLines( fragmentBlock );

					if( typeof fragmentIndex === 'number' ) {
						fragmentBlock.setAttribute( 'data-fragment-index', fragmentIndex );
						fragmentIndex += 1;
					}
					else {
						fragmentBlock.removeAttribute( 'data-fragment-index' );
					}

					// Scroll marks into view as we step through them
					fragmentBlock.addEventListener( 'visible', Plugin.scrollMarkedLineIntoView.bind( Plugin, fragmentBlock, scrollState ) );
					fragmentBlock.addEventListener( 'hidden', Plugin.scrollMarkedLineIntoView.bind( Plugin, fragmentBlock.previousSibling, scrollState ) );

				} );

				block.removeAttribute( 'data-fragment-index' )
				block.setAttribute( 'data-mark', Plugin.serializeMarkSteps( [ markSteps[0] ] ) );

            }

			// Scroll the first mark into view when the slide
			// becomes visible. Note supported in IE11 since it lacks
			// support for Element.closest.
			var slide = typeof block.closest === 'function' ? block.closest( 'section:not(.stack)' ) : null;
			if( slide ) {
				var scrollFirstMarkIntoView = function() {
					Plugin.scrollMarkedLineIntoView( block, scrollState, true );
					slide.removeEventListener( 'visible', scrollFirstMarkIntoView );
				}
				slide.addEventListener( 'visible', scrollFirstMarkIntoView );
			}

			Plugin.markLines( block );

		}
	},

	/**
	 * Animates scrolling to the first marked line
	 * in the given block.
	 */
	scrollMarkedLineIntoView: function( block, scrollState, skipAnimation ) {

		cancelAnimationFrame( scrollState.animationFrameID );

		// Match the scroll position of the currently visible
		// block
		if( scrollState.currentBlock ) {
			block.scrollTop = scrollState.currentBlock.scrollTop;
		}

		// Remember the current block so that we can match
		// its scroll position when showing/hiding fragments
		scrollState.currentBlock = block;

		var markBounds = this.getMarkedLineBounds( block )
		var viewportHeight = block.offsetHeight;

		// Subtract padding from the viewport height
		var blockStyles = getComputedStyle( block );
		viewportHeight -= parseInt( blockStyles.paddingTop ) + parseInt( blockStyles.paddingBottom );

		// Scroll position which centers all marks
		var startTop = block.scrollTop;
		var targetTop = markBounds.top + ( Math.min( markBounds.bottom - markBounds.top, viewportHeight ) - viewportHeight ) / 2;

		// Make sure the scroll target is within bounds
		targetTop = Math.max( Math.min( targetTop, block.scrollHeight - viewportHeight ), 0 );

		if( skipAnimation === true || startTop === targetTop ) {
			block.scrollTop = targetTop;
		}
		else {

			// Don't attempt to scroll if there is no overflow
			if( block.scrollHeight <= viewportHeight ) return;

			var time = 0;
			var animate = function() {
				time = Math.min( time + 0.02, 1 );

				// Update our eased scroll position
				block.scrollTop = startTop + ( targetTop - startTop ) * Plugin.easeInOutQuart( time );

				// Keep animating unless we've reached the end
				if( time < 1 ) {
					scrollState.animationFrameID = requestAnimationFrame( animate );
				}
			};

			animate();

		}

	},

	/**
	 * The easing function used when scrolling.
	 */
	easeInOutQuart: function( t ) {

		// easeInOutQuart
		return t<.5 ? 8*t*t*t*t : 1-8*(--t)*t*t*t;

	},

	getMarkedLineBounds: function( block ) {

		var markedLines = block.querySelectorAll( '.mark-line' );
		if( markedLines.length === 0 ) {
			return { top: 0, bottom: 0 };
		}
		else {
			var firstMark = markedLines[0];
			var lastMark = markedLines[ markedLines.length -1 ];

			return {
				top: firstMark.offsetTop,
				bottom: lastMark.offsetTop + lastMark.offsetHeight
			}
		}

	},

	/**
	 * Visually emphasize specific regions within a block.
	 *
	 * @param {HTMLElement} block a <... data-mark=...> block
	 * @param {String} [linesToMark] The lines that should be
	 * marked in this format:
	 * "1" 		= marks line 1
	 * "2,5"	= marks lines 2 & 5
	 * "2,5-7"	= marks lines 2, 5, 6 & 7
	 */
	markLines: function( block, linesToMark ) {

		var markSteps = Plugin.deserializeMarkSteps( linesToMark || block.getAttribute( 'data-mark' ) );

		if( markSteps.length ) {

			markSteps[0].forEach( function( mark ) {

				var pattern = '';
				if( typeof mark.end !== 'number' ) {
                    mark.end = mark.start
                }
				if( typeof mark.start === 'number' ) {
                    pattern = '^('
                        + '.*\n'.repeat(mark.start - 1)
                        + ')'
                        + '(.*(\n|$))'.repeat(mark.end - mark.start + 1) + '';
                }
                var r = new RegExp(pattern, 'y');
                new Mark(block).markRegExp(
                    r,
                    {
                        acrossElements: true, ignoreGroups: 1, className: 'mark-line',
                        // Prevent any further matches.
                        'each' : function(elem, info) { r.lastIndex = Infinity; }
                    });
			} );

		}
	},

	/**
	 * Parses and formats a user-defined string of line
	 * numbers to mark.
	 *
	 * @example
	 * Plugin.deserializeMarkSteps( '1,2|3,5-10' )
	 * // [
	 * //   [ { start: 1 }, { start: 2 } ],
	 * //   [ { start: 3 }, { start: 5, end: 10 } ]
	 * // ]
	 */
	deserializeMarkSteps: function( markSteps ) {

		// Remove whitespace
		markSteps = markSteps.replace( /\s/g, '' );

		// Divide up our line number groups
		markSteps = markSteps.split( Plugin.MARK_STEP_DELIMITER );

		return markSteps.map( function( marks ) {

			return marks.split( Plugin.MARK_LINE_DELIMITER ).map( function( mark ) {

				// Parse valid line numbers
				if( /^[\d-]+$/.test( mark ) ) {

					mark = mark.split( Plugin.MARK_LINE_RANGE_DELIMITER );

					var lineStart = parseInt( mark[0], 10 ),
						lineEnd = parseInt( mark[1], 10 );

					if( isNaN( lineEnd ) ) {
						return {
							start: lineStart
						};
					}
					else {
						return {
							start: lineStart,
							end: lineEnd
						};
					}

				}
				// If no line numbers are provided, no code will be marked
				else {

					return {};

				}

			} );

		} );

	},

	/**
	 * Serializes parsed line number data into a string so
	 * that we can store it in the DOM.
	 */
	serializeMarkSteps: function( markSteps ) {

		return markSteps.map( function( marks ) {

			return marks.map( function( mark ) {

				// Line range
				if( typeof mark.end === 'number' ) {
					return mark.start + Plugin.MARK_LINE_RANGE_DELIMITER + mark.end;
				}
				// Single line
				else if( typeof mark.start === 'number' ) {
					return mark.start;
				}
				// All lines
				else {
					return '';
				}

			} ).join( Plugin.MARK_LINE_DELIMITER );

		} ).join( Plugin.MARK_STEP_DELIMITER );

	}

}

export default () => Plugin;
