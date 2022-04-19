import sys


class Teste_environment:
    def test_python_version(self):
        py_ver = sys.version_info[:2]
        assert py_ver == (3, 10)
