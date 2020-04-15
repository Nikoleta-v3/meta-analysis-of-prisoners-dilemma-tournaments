from invoke import task

@task
def test(c):
    """
    Test all packaged code and notebooks
    """
    c.run("pytest tests")