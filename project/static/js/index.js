/*
    NOTE:
        run this command on project's folder: browserify static/js/index.js -o static/js/bundle.js

        - but can do: 'npm run bfy' since i (Joemar) modify the command inside package.json
*/

// important requirements from node_module
require('flowbite')
// include the script file, in this same folder
require('./script.js');
