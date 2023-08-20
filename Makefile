app_name = ms-companies

check:
	@git add .
	@pre-commit

test:
	@pytest -vv

commit:
	@cz commit
