const Plugin = {

	id: 'mark',

    // If you need to write | followed by a digit or a | in a regexp pattern,
    // you can follow it with a non-capturing group, e.g.
	STEP_DELIMITER: '|',
	REGION_DELIMITER: ',',
	LINE_RANGE_DELIMITER: '-',

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

        // Prepare regexps based on the constants for later parsing.
        for (const i of ['STEP', 'REGION', 'LINE_RANGE']) {
            Plugin[i + '_DELIMITER_P']
                = RegExp( '\\s*\\' + Plugin[i + '_DELIMITER'] + '\\s*', '' );
        }

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
	 * If the block contains multiple mark steps, insert a (following) sibling
	 * fragment for each step and respond to the fragment's appearance by
	 * re-marking.
	 */
	markBlock: function( block ) {

		if( block.hasAttribute( 'data-mark' ) ) {

			var scrollState = { currentBlock: block };

			// If there is more than one mark step, generate
			// fragments
			var markSteps = Plugin.deserializeMarkSteps( block.getAttribute( 'data-mark' ) );

			if( markSteps.length > 1 ) {

                // Wrap the block and its fragments in a parent div
                const wrapper = document.createElement('div');
                wrapper.classList.add('mark-fragments');
                block.parentNode.insertBefore(wrapper, block);
                wrapper.appendChild(block);

				// If the original block has a fragment-index,
				// each mark fragment should follow in an incremental sequence
				var fragmentIndex = parseInt( block.getAttribute( 'data-fragment-index' ), 10 );

				if( typeof fragmentIndex !== 'number' || isNaN( fragmentIndex ) ) {
					fragmentIndex = null;
				}

				// Append fragments for all steps except the original block
				markSteps.slice(1).forEach( function( mark ) {

                    const fragmentBlock = document.createElement('div');
                    fragmentBlock.classList.add('fragment');
                    fragmentBlock.setAttribute( 'data-mark', Plugin.serializeMarkSteps( [ mark ] ) );
                    wrapper.appendChild( fragmentBlock );

					if( typeof fragmentIndex === 'number' ) {
						fragmentBlock.setAttribute( 'data-fragment-index', fragmentIndex );
						fragmentIndex += 1;
					}
					else {
						fragmentBlock.removeAttribute( 'data-fragment-index' );
					}

					// Re-do the marks as we step forward...
					fragmentBlock.addEventListener(
                        'visible', Plugin.asyncMarkAndScroll.bind(
                            Plugin, fragmentBlock, scrollState, true ) );

                    // ...or backward.
					fragmentBlock.addEventListener(
                        'hidden',
                        Plugin.asyncMarkAndScroll.bind(
                            Plugin, fragmentBlock.previousSibling, scrollState, true ) );
				} );

				block.removeAttribute( 'data-fragment-index' );
				block.setAttribute( 'data-mark', Plugin.serializeMarkSteps( [ markSteps[0] ] ) );

			}

			// Scroll the first mark into view when the slide
			// becomes visible. Note supported in IE11 since it lacks
			// support for Element.closest.
			var slide = typeof block.closest === 'function' ? block.closest( 'section:not(.stack)' ) : null;
			if( slide ) {
				var scrollFirstMarkIntoView = function() {
					Plugin.asyncMarkAndScroll( block, scrollState, false );
					slide.removeEventListener( 'visible', scrollFirstMarkIntoView );
				}
				slide.addEventListener( 'visible', scrollFirstMarkIntoView );
			}
            else {
			    Plugin.asyncReplaceMarks( block, Plugin.deserializeMarkSteps( block.getAttribute( 'data-mark' ) ) );
            }

		}

	},

    // Re-marks scrollState.currentBlock according to the data-mark attribute of
    // markProvider, and scrolls the marks into view, animating the scroll iff
    // animateScroll.
	asyncMarkAndScroll: function( markProvider, scrollState, animateScroll ) {
        Plugin.asyncReplaceMarks(
            scrollState.currentBlock, markProvider.getAttribute( 'data-mark' ),
            function () {
                Plugin.scrollMarkedLineIntoView(scrollState.currentBlock, scrollState, !animateScroll)
            } );
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

		var markedLines = block.querySelectorAll( 'mark[data-markjs=true]' );
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

    // Uses marker to mark the given regions of block, calling done on
    // completion.
	asyncMarkRegions: function( block, marker, regions, done ) {
        if ( regions.length === 0 ) {
            return done();
        }
        function markTail() {
            Plugin.asyncMarkRegions(block, marker, regions.slice(1), done);
        }

        const region = regions[0];
        var pattern = region.pattern;
        var flags = region.flags;

        if ( pattern === undefined ) {
            // This is a line-based pattern.
            pattern = '^('
                + '(?:.*\n){' + (region.start - 1) + '}'
                + ')'
                + '('
                + '(?:.*(\n|$)){' + (region.end - region.start + 1) + '})';
            flags = 'dy';
        }
        else if ( !flags.includes( 'g' ) &&  !flags.includes( 'y' ) ) {
            // ensure that the "each" trick for quitting matches actually works.
            flags = flags + 'g';
        }

        var matcher = new RegExp(pattern, flags);
        marker.markRegExp(
            matcher,
            {
                acrossElements: true,
                ignoreGroups: flags.includes('d') ? 1 : 0,
                // Prevent any further matches.
                'each' : function(elem, info) { matcher.lastIndex = Infinity; },
                done: markTail
            } );
    },

    // Removes any marks from block and applies the given
    // serializedMarks, calling done on completion.
    //
    // Requires: serializedMarks does not contain multiple marking steps.
	asyncReplaceMarks: function( block, serializedMarks, done ) {
        const steps = Plugin.deserializeMarkSteps( serializedMarks );
        console.assert( steps.length == 1 );
        const regions = steps[0];

        const marker = new Mark(block);
        marker.unmark({
            done: function() {
                Plugin.asyncMarkRegions(block, marker, regions, done)
            }
        } );
	},

    parseLineSpec: function( input ) {
        const oldInput = input[0];
        const start = parseInt( dropLeading( input, /\d+/ ), 10 );
        if ( isNaN( start ) ) { return null; }

        const end = dropLeading( input, Plugin.LINE_RANGE_DELIMITER_P )
              ? parseInt( dropLeading( input, /\d+/ ), 10 ) : start;
        if ( isNaN(end) ) { return null; }
        return {
            start: start, end: end,
            text: oldInput.slice(0, oldInput.length - (input[0].length))
        };
    },

    parseRegExp: function( input ) {
        const r = dropLeading(
            input, /(.)(?:\\.|(?!\1)[^\\])*\1[dgimsuy]*/s );
        if ( r === null ) return null;

        const delimiter = r[0]
        const patternEnd = r.lastIndexOf( delimiter )

        const pattern = r.slice( 1, patternEnd )
        // Un-escape any escaped delimiters.
              .replace( '\\' + delimiter, delimiter );
        const flags = r.slice( patternEnd + 1 );
        return { pattern: pattern, flags: flags, text: r };
    },

	/**
	 * Parses and formats a user-defined string of marking steps.
	 *
	 * @example
	 * Plugin.deserializeMarkSteps( '1,2|3,5-10' )
	 * // [
	 * //   [ { start: 1 }, { start: 2 } ],
	 * //   [ { start: 3 }, { start: 5, end: 10 } ]
	 * // ]
	 */
	deserializeMarkSteps: function( serialized ) {

        const steps = []
        const input = [ serialized.trimStart() ];
        var lastLength = Infinity;

        do { // parse a step
            const regions = [];
            steps.push(regions);

            // Check that we're actually consuming the input.
            if ( input[0].length >= lastLength ) {
                console.assert( input[0].length < lastLength );
                return [];
            }
            lastLength = input[0].length;

            if ( startsWith( input, Plugin.STEP_DELIMITER_P ) ) continue;

            do {  // parse a step
                const region = Plugin.parseLineSpec( input )
                      || Plugin.parseRegExp( input );
                if ( !region ) break;
                regions.push( region );
            }
            while( dropLeading( input, Plugin.REGION_DELIMITER_P ) );
        }
        while( dropLeading( input, Plugin.STEP_DELIMITER_P ) );
        console.log(
            'deserialized', serialized, 'to',
            Plugin.serializeMarkSteps( steps ));
        return steps;
	},

	/**
	 * Serializes parsed line number data into a string so
	 * that we can store it in the DOM.
	 */
	serializeMarkSteps: function( markSteps ) {

		return markSteps.map( function( marks ) {

			return marks.map( function( mark ) { return mark.text } )
		        .join( Plugin.REGION_DELIMITER );

		} ).join( Plugin.STEP_DELIMITER );
	}

}

function dropLeading( s, pattern ) {
    if ( typeof( pattern ) == 'string' ) {
        if (s[0].startsWith( pattern )) {
            s[0] = s[0].slice( pattern.length );
            return pattern;
        }
    }
    else {
        const r = s[0].match(pattern);
        if (r && r.index === 0) {
            s[0] = s[0].slice(r[0].length);
            return r[0];
        }
    }
    return null;
}

function startsWith( s, pattern ) {
    if ( typeof( pattern ) == 'string' ) {
        return s[0].startsWith( pattern );
    }
    const r = s[0].match(pattern);
    return r && r.index === 0;
}



export default () => Plugin;
