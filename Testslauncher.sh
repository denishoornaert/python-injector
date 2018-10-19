pytestlist=`find test/ -name 'Test*[^__init__]*.py'`
python3 -m unittest $pytestlist -v
