@echo off
echo Creating test VFS archive
py create_test_vfs.py

echo.
echo Starting emulator with test script
py emulator.py --vfs test_vfs.zip --script test_script.txt

echo.
echo Done! Press any key to close
pause
