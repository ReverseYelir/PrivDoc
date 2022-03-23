# PrivDoc

How to execute script:
	1. Clone repo
	2. open windows enviroment variables (windows button + "edit enviroment")
	3. Find PATH under "Enviroment Variables", select it and click "Edit"
	4. In the new window labeled "edit enviroment variable", click "New" and paste in the your local absolute path to the repo (ex: C:\Users\User\PrivDoc)
	5. This allows PrivDoc.py to be called from any directory
	6. Ensure the default application for .py files is set to your python.exe installation

Note:
    If you are having difficulties getting windows to pass along your command line arguments
    see this stack overflow post: https://stackoverflow.com/questions/2640971/windows-is-not-passing-command-line-arguments-to-python-programs-executed-from-t
    In the [HKEY_CLASSES_ROOT\Applications\python.exe\shell\open\command] registry, under default, the "%*" is missing at the end of @="\"C:\\Python25\\python.exe\" \"%1\"

Usage:
    - encryption: PrivDoc.py -enc absolute_path_file_to_encrypt
    - decryption: PrivDoc.py -dec absolute_path_file_to_decrypt
