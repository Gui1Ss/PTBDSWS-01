import os

from flask_migrate import Migrate

from app import create_app, db
from app.models import Role, User

app = create_app(os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Role": Role}


@app.cli.command()
def test():
    """Executa os testes unitários."""
    import unittest

    testes = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(testes)


if __name__ == "__main__":
    app.run(debug=True)
