# type: ignore


def test_main(mocker):
    app = mocker.patch("dlt_init_openapi.cli.app")

    # noinspection PyUnresolvedReferences
    from dlt_init_openapi import __main__  # noqa: F401

    app.assert_called_once()
