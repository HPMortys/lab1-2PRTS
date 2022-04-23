from Lab2.fixtures import parser


class TestSuite:

    def test_iperf3_client_connection(self, client):

        stdout, error, serv_error = client

        assert not error and not serv_error

        result_dict = parser.parser(stdout)
        for value in result_dict:
            assert value['Transfer'] > 1 and value['Bitrate'] > 1
