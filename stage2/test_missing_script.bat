@echo off
echo Testing error handling with missing script...
py emulator.py --script missing_script.txt

echo.
echo Test completed. Press any key to close
pause
