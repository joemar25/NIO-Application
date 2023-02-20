/*
NOTE:
run this command on project's folder: browserify static/js/index.js -o static/js/bundle.js
- just run: 'npm run bfy' since (Joemar) modify the command inside package.json
*/

// important requirements from node_module
require('flowbite')
// include local scripts
require('./recording.js');
require('./chart.js');
// include the script file, in this same folder
require('./script.js');
