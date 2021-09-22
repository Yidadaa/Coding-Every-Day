var gl;
var theta = 0.0;
var thetaLoc, colorLoc;
var delay = 100;
var direction = true;
var vBuffer, cBuffer;
var program;
var vertices = [];
var vcolors = [];
var primitives = 0;
var max_prims = 200, num_triangles = 0;
let trianglesFlag = false;
let stripesFlag = false;
let fansFlag = false;

counter_tri = 1;
counter_stri = 1;
counter_fans = 1;

window.onload = function init() {
    // get the canvas handle from the document's DOM
    var canvas = document.getElementById("gl-canvas");
    const Triangle = document.getElementById("Triangles");
    const TrianglesStrips = document.getElementById("TrianglesStrips");
    const TrianglesFans = document.getElementById("TrianglesFans");

    Triangle.addEventListener("click", () => {
        trianglesFlag = !trianglesFlag;
    });
    TrianglesStrips.addEventListener("click", () => {
        stripesFlag = !stripesFlag;
    });
    TrianglesFans.addEventListener("click", () => {
        fansFlag = !fansFlag;
    });
    // console.log(trianglesFlag)
    window.addEventListener("keydown", () => {
        switch (event.keyCode) {
            case 49:
                trianglesFlag = !trianglesFlag;
                break;
            case 50:
                stripesFlag = !stripesFlag;
                break;
            case 51:
                fansFlag = !fansFlag;
                break;
        }
    })
    // reference slides Angel_UNM_14_4_3.ppt
    // initialize webgl
    gl = WebGLUtils.setupWebGL(canvas);

    // check for errors
    if (!gl) {
        alert("WebGL isn't available");
    }

    // set up a viewing surface to display your image
    gl.viewport(0, 0, canvas.width, canvas.height);

    // clear the display with a background color 
    // specified as R,G,B triplet in 0-1.0 range
    gl.clearColor(0.5, 0.5, 0.5, 1.0);

    //  Load shaders -- all work done in init_shaders.js
    program = initShaders(gl, "vertex-shader", "fragment-shader");

    // make this the current shader program
    gl.useProgram(program);

    // Get a handle to theta  - this is a uniform variable defined 
    // by the user in the vertex shader, the second parameter should match
    // exactly the name of the shader variable
    thetaLoc = gl.getUniformLocation(program, "theta");

    // we are also going manipulate the vertex color, so get its location
    colorLoc = gl.getUniformLocation(program, "vertColor");

    // set an initial color for all vertices
    // gl.uniform4fv (colorLoc, [1., 0., 0., 1.])

    // create a vertex buffer and initialize 
    vBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer)
    gl.bufferData(gl.ARRAY_BUFFER, 300 * 64, gl.STATIC_DRAW);
    // ArrayBuffer vBuffer = new ArrayBuffer(300 * 64, gl.STATIC_DRAW)
    vBuffer1 = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer1)
    gl.bufferData(gl.ARRAY_BUFFER, 300 * 48, gl.STATIC_DRAW);
    vBuffer2 = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer2)
    gl.bufferData(gl.ARRAY_BUFFER, 300 * 32, gl.STATIC_DRAW);


    // create a color buffer and initialize 
    cBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, cBuffer)
    gl.bufferData(gl.ARRAY_BUFFER, 300 * 6 * 8 * 6, gl.STATIC_DRAW);
    cBuffer1 = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, cBuffer1)
    gl.bufferData(gl.ARRAY_BUFFER, 300 * 6 * 8 * 6, gl.STATIC_DRAW);
    cBuffer2 = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, cBuffer2)
    gl.bufferData(gl.ARRAY_BUFFER, 300 * 6 * 8 * 6, gl.STATIC_DRAW);

    // create the square geometry, send it to GPU
    // updateVertices(0);

    render();
};


function updateVertices(counter, primitives) {
    if (trianglesFlag) {

        if (counter_tri <= 300) {
            color_val = [1, 0, 0, 1.];
            // triangle colors different from the fans and stripes
            const size_square = [0.02, 0.03, 0.04];
            const direction = [-1, 1]
            var random_shape = size_square[Math.floor(Math.random() * size_square.length)];
            var translation = [direction[Math.floor(Math.random() * direction.length)] * Math.random(), direction[Math.floor(Math.random() * direction.length)] * Math.random()]
            // inspired by Shahin's method about this translation setting and if algorithm for
            // the number of the verticaes (300), and the changing size of each vertice
            // my previous settings about how to create 0-300 squares are the commented lines above

            // triangle 1
            //    vertices.push([ 0.0 + x_random,  0.03 + y_random]); 
            // vertices.push([-0.03 + x_random,  0.0 + y_random]); 
            //    vertices.push([ 0.0 + x_random, -0.03 + y_random]); 

            vertices = []
            vertices.push([translation[0], random_shape + translation[1]]);
            vertices.push([translation[0] - random_shape, translation[1]]);
            vertices.push([translation[0], translation[1] - random_shape]);
            // triangle 2
            // vertices.push([ 0.0 + x_random,  0.03 + y_random]); 
            // vertices.push([ 0.0 + x_random, -0.03  + y_random]); 
            //    vertices.push([ 0.03 + x_random,  0.0  + y_random]); 
            vertices.push([translation[0], translation[1] + random_shape]);
            vertices.push([translation[0], translation[1] - random_shape]);
            vertices.push([translation[0] + random_shape, translation[1]]);
            // different colors
            vcolors = []
            vcolors.push(color_val);
            vcolors.push(color_val);
            vcolors.push(color_val);
            vcolors.push(color_val);
            vcolors.push(color_val);
            vcolors.push(color_val);
        }

        gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer)
        // transfer the data -- this is actually pretty inefficient!
        // flatten() function is defined in MV.js - this simply creates only
        // the vertex coordinate data array - all other metadata in Javascript
        // arrays should not be in the vertex buffer.
        gl.bufferSubData(gl.ARRAY_BUFFER, counter_tri * 48, flatten(vertices), gl.STATIC_DRAW);
        // specify the format of the vertex data - here it is a float with
        // 2 coordinates per vertex - these are its attributes 
        var vPosition = gl.getAttribLocation(program, "vPosition");
        gl.vertexAttribPointer(vPosition, 2, gl.FLOAT, false, 0, 0);
        gl.enableVertexAttribArray(vPosition);

        gl.bindBuffer(gl.ARRAY_BUFFER, cBuffer)
        gl.bufferSubData(gl.ARRAY_BUFFER, counter_tri * 6 * 4 * 4, flatten(vcolors));
        var vColor = gl.getAttribLocation(program, "vColor");
        gl.vertexAttribPointer(vColor, 4, gl.FLOAT, false, 0, 0);
        gl.enableVertexAttribArray(vColor);

        for (i = 0; i < counter_tri; i++) {
            gl.drawArrays(gl.TRIANGLES, i * 6, 6);
            // using gl.TRIANGLES in loop
        }

    }

    if (stripesFlag) {

        if (counter_stri <= 300) {
            color_val = [0, 1, 0, 1.];
            const size_square = [0.02, 0.03, 0.04];
            const direction = [-1, 1]
            var random_shape = size_square[Math.floor(Math.random() * size_square.length)];
            var translation = [direction[Math.floor(Math.random() * direction.length)] * Math.random(), direction[Math.floor(Math.random() * direction.length)] * Math.random()]
            // inspired by Shahin's method about this translation setting and if algorithm for
            // the number of the verticaes (300), and the changing size of each vertice
            // my previous settings about how to create 0-300 squares are the commented lines above

            vertices1 = []
            // stripes 1 and 2
            // same with the triangles
            vertices1.push([translation[0] + random_shape, translation[1] + random_shape]);
            vertices1.push([translation[0] + random_shape, translation[1] - random_shape]);
            vertices1.push([translation[0] - random_shape, translation[1] + random_shape]);
            vertices1.push([translation[0] - random_shape, translation[1] - random_shape]);

            vcolors1 = []
            vcolors1.push(color_val);
            vcolors1.push(color_val);
            vcolors1.push(color_val);
            vcolors1.push(color_val);
        }

        gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer1)
        gl.bufferSubData(gl.ARRAY_BUFFER, counter_stri * 32, flatten(vertices1), gl.STATIC_DRAW);
        var vPosition = gl.getAttribLocation(program, "vPosition");
        gl.vertexAttribPointer(vPosition, 2, gl.FLOAT, false, 0, 0);
        gl.enableVertexAttribArray(vPosition);

        gl.bindBuffer(gl.ARRAY_BUFFER, cBuffer1)
        gl.bufferSubData(gl.ARRAY_BUFFER, counter_stri * 4 * 4 * 4, flatten(vcolors1));
        var vColor = gl.getAttribLocation(program, "vColor");
        gl.vertexAttribPointer(vColor, 4, gl.FLOAT, false, 0, 0);
        gl.enableVertexAttribArray(vColor);

        for (i = 0; i < counter_stri; i++) {
            gl.drawArrays(gl.TRIANGLE_STRIP, i * 4, 4);
            // using gl.TRIANGLE_STRIP
        }
    }

    if (fansFlag) {

        if (counter_fans <= 300) {
            color_val = [0, 0, 1, 1.];
            const size_square = [0.02, 0.03, 0.04];
            const direction = [-1, 1]
            var random_shape = size_square[Math.floor(Math.random() * size_square.length)];
            var translation = [direction[Math.floor(Math.random() * direction.length)] * Math.random(), direction[Math.floor(Math.random() * direction.length)] * Math.random()]
            // inspired by Shahin's method about this translation setting and if algorithm for
            // the number of the verticaes (300), and the changing size of each vertice
            // my previous settings about how to create 0-300 squares are the commented lines above
            vertices2 = []
            // fans 1 and 2
            // same with the triangles
            vertices2.push([translation[0] + random_shape, translation[1] + random_shape]);
            vertices2.push([translation[0] - random_shape, translation[1] + random_shape]);
            vertices2.push([translation[0] - random_shape, translation[1] - random_shape]);
            vertices2.push([translation[0] + random_shape, translation[1] - random_shape]);

            vcolors2 = []
            vcolors2.push(color_val);
            vcolors2.push(color_val);
            vcolors2.push(color_val);
            vcolors2.push(color_val);
        }

        gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer2)
        gl.bufferSubData(gl.ARRAY_BUFFER, counter_fans * 32, flatten(vertices2), gl.STATIC_DRAW);
        var vPosition = gl.getAttribLocation(program, "vPosition");
        gl.vertexAttribPointer(vPosition, 2, gl.FLOAT, false, 0, 0);
        gl.enableVertexAttribArray(vPosition);

        gl.bindBuffer(gl.ARRAY_BUFFER, cBuffer2)
        gl.bufferSubData(gl.ARRAY_BUFFER, counter_fans * 4 * 4 * 4, flatten(vcolors2));
        var vColor = gl.getAttribLocation(program, "vColor");
        gl.vertexAttribPointer(vColor, 4, gl.FLOAT, false, 0, 0);
        gl.enableVertexAttribArray(vColor);

        for (i = 0; i < counter_fans; i++) {
            gl.drawArrays(gl.TRIANGLE_FAN, i * 4, 4);
            // using gl.TRIANGLE_FAN
        }
    }
}

counter = 1;
keyCode = 1;

function render() {
    // this is render loop

    //add event to buttons
    // clear the display with the background color
    gl.clear(gl.COLOR_BUFFER_BIT);
    theta += 0.04;
    // set the theta value for the rotation speed
    gl.uniform1f(thetaLoc, theta);
    // reference slides Angel_UNM_14_4_3.ppt
    if (trianglesFlag === true) {
        if (counter_tri < 300)
            counter_tri++;
    }
    updateVertices(counter_tri, 1);
    if (stripesFlag === true) {
        if (counter_stri < 300)
            counter_stri++;
    }
    updateVertices(counter_stri, 2);
    if (fansFlag === true) {
        if (counter_fans < 300)
            counter_fans++;
    }
    updateVertices(counter_fans, 3);
    setTimeout(() => {

        requestAnimFrame(render);
    }, delay);
}