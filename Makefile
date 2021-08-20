tests: force
	@PYTHONPATH=`pwd`/plugin python tests/test_connection.py

force:
