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

