/*
NOTE:
run this command on project's folder: browserify static/js/index.js -o static/js/bundle.js
- just run: 'npm run bfy' since (Joemar) modify the command inside package.json
*/

// important requirements from node_module
require('flowbite')
require('flowbite-typography');
require('blueimp-file-upload/js/jquery.fileupload');

// include local scripts
require('./dark_mode.js');
require('./home_controller.js');
require('./recording.js');
require('./verification.js');

