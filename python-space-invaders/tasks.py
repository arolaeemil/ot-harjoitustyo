from invoke import task


@task
def start(ctx):
    #windows command line start, if wish to use windows uncomment this and comment the other start
    #ctx.run("python src/game.py", pty=False)
    ctx.run("python3 src/game.py", pty=True)

@task
def test(ctx):
    ctx.run("pytest src", pty=True)



@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src", pty=True)


@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html", pty=True)

@task
def format(ctx):
    ctx.run("autopep8 --in-place --recursive src", pty=True)

@task
def lint(ctx):
    ctx.run("pylint src", pty=True)
