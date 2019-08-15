# file_diff.py
* Usage: python3 file_diff.py file1 file2

# folder_diff.py
* Usage: python3 folder_diff.py folder1 folder2

# Prerequisite installation:

## Clang installation in Ubuntu
* Download pre-built binary from [here](http://releases.llvm.org/download.html)
* `sudo  mkdir -p /usr/local; cd /usr/local`
* `sudo tar xvf path_to_downloaded_file --directory /usr/local`
* `sudo mv clang+llvm-8.0.0-x86_64-linux-gnu-ubuntu-18.04 llvm-8.0`
* Add `export PATH="$PATH:/usr/local/llvm-8.0/bin"` in `~/.bashrc`

