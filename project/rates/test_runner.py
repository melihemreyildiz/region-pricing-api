from django.test.runner import DiscoverRunner


class NoDbTestRunner(DiscoverRunner):
    """A test runner to use the existing database without creating or tearing down a new one."""

    def setup_databases(self, **kwargs):
        pass  # Skip setting up databases.

    def teardown_databases(self, old_config, **kwargs):
        pass  # Skip tearing down databases.
