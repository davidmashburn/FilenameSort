FilenameSort is a utility to aid in natural or "human-like" sorting of file names.

Normally using sort, ["file_1_10a.png","file_1_1a.png","file_1_5a.png"] would sort as:
["file_1_10a.png","file_1_1a.png","file_1_5a.png"]

Using the function getSortableList instead results in:
["file_1_1a.png","file_1_5a.png","file_1_10a.png"]

Which is more like what one would expect.

FilenameSort uses cmpGen to aid sorting.
