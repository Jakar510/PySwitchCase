rmdir /Q /S dist
mkdir dist

pause

python setup.py build sdist bdist_wheel

python -m twine upload dist/*

pause
