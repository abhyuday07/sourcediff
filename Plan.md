# Problem
1. Check for the files which are new in the version
2. Even if two files are same, we can have differences in their internal structures. *We have to list all the functions which are different between both the files*

# Advantages
* We are only interested in getting the function name which are different in both the codebases. We do not need to exactly locate the point of difference.

# Method 1:
* Check which files are different between two codebases and extract all the functions from these files.
* If two files with same name are present in both the codebases:
    * Hash every function of the source code by clipping the function code using clang
    * Compare the hash to get unique function

# Method 2:
* Check which files are different between two codebases and extract all the functions from these files.
* If two files with same name are present in both the codebases:
    * Hash AST of the function code using clang
    * Compare the hash to get unique function

# Tools that we already have:
* Can get a list of functions for each file
* Can get AST of the source file

# Final plan:
* Remove all the include statements from the code
* Note: include statements are removed because if the file include a standard library then all functions of standard library will also be pulled in our ast
* Extract all the function names and their boundaries in source code
* Create a mapping of function name to the hashes of their source code
* Note: Doing this, we will get two mapping corresponding to two files
* Sort both the mapping by their function name
* Compare functions to get unique functions