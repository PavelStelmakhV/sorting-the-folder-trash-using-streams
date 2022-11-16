# sorting-the-folder-trash-using-streams
<p>The script processes the "trash" folders, sorts files by extensions using several threads.</p>
<p>The script creates a folder into which it transfers files with the appropriate extensions. The default folder name is "sorted_trash"</p>
<p>At startup, you must specify the arguments:</p>
<ul>
<li>required argument '--source', '-s': source folder</li>
<li>additional argument '--output', '-o': folder where files are transferred (default: sorted_trash)</li>
</ul>