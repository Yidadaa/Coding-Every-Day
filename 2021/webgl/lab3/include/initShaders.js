//
//  initShaders.js
//
//
// this function initializes the vertex and fragment shaders
function initShaders( gl, vertexShaderId, fragmentShaderId ) {
	var vertShdr;
	var fragShdr;

	var vertElem = document.getElementById( vertexShaderId );
	if ( !vertElem ) {
		alert( "Unable to load vertex shader " + vertexShaderId );
		return -1;
	}
	else {
		// get the vertex shader source (string) and then compile it

		// create the vertex shader  
		vertShdr = gl.createShader(gl.VERTEX_SHADER);

		// read it - as a string
		gl.shaderSource( vertShdr, vertElem.text );

		// compile it
		gl.compileShader( vertShdr );

		// print error logs if compilation failed
		if ( !gl.getShaderParameter(vertShdr, gl.COMPILE_STATUS) ) {
			var msg = "Vertex shader failed to compile.  The error log is:"
				+ "<pre>" + gl.getShaderInfoLog( vertShdr ) + "</pre>";
			alert( msg );
			return -1;
		}
	}

	// get the fragment shader source (string) and then compile it
	var fragElem = document.getElementById( fragmentShaderId );
	if ( !fragElem ) {
		alert( "Unable to load vertex shader " + fragmentShaderId );
		return -1;
	}
	else {
		// create a fragment shader
		fragShdr = gl.createShader( gl.FRAGMENT_SHADER );

		// read it as a string
		gl.shaderSource( fragShdr, fragElem.text );

		// compile it
		gl.compileShader( fragShdr );

		// print error logs if compilation failed
		if ( !gl.getShaderParameter(fragShdr, gl.COMPILE_STATUS) ) {
			var msg = "Fragment shader failed to compile.  The error log is:"
				+ "<pre>" + gl.getShaderInfoLog( fragShdr ) + "</pre>";
			alert( msg );
			return -1;
		}
	}

	// create  a shader program 
	var program = gl.createProgram();

	// attach the two shaders to the program
	gl.attachShader( program, vertShdr );
	gl.attachShader( program, fragShdr );

	// link the program
	gl.linkProgram( program );

	// if linking failed, print error log
	if ( !gl.getProgramParameter(program, gl.LINK_STATUS) ) {
		var msg = "Shader program failed to link.  The error log is:"
			+ "<pre>" + gl.getProgramInfoLog( program ) + "</pre>";
		alert( msg );
		return -1;
	}
	return program;
}
