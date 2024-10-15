#!/bin/bash

original_path="$PATH"
echo "Current PATH: $original_path" 

home_path="$HOME"
export PATH="$PATH:$home_path"

new_script="assignment_10_internal_script.sh"
echo '#!/bin/bash' > "$new_script"
echo 'echo "Content of internal script"' >> $new_script
chmod +x "$new_script"

$new_script

export PATH="$original_path"

$new_script
# it did not work since the file is located in another directory, to execute the script, its absolute path should be specified or relative to PATH
