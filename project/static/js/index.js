/*
NOTE:
run this command on project's folder: browserify static/js/index.js -o static/js/bundle.js
- just run: 'npm run bfy' since (Joemar) modify the command inside package.json
*/

// important requirements from node_module
require('flowbite')
require('blueimp-file-upload/js/jquery.fileupload');
// include local scripts
require('./drag_n_drop.js');
require('./recording.js');
// include the script file, in this same folder
require('./script.js');


