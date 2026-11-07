import unittest
import unittest.mock
import urllib.error

from scripts.doctor import main, MODEL_NAME


class TestDoctor(unittest.TestCase):
    @unittest.mock.patch("shutil.which")
    @unittest.mock.patch("subprocess.check_output")
    @unittest.mock.patch("urllib.request.urlopen")
    def test_success(self, mock_urlopen, mock_check_output, mock_which):
        # Simulate both commands present
        mock_which.side_effect = lambda cmd: f"/usr/bin/{cmd}"

        def co_side(cmd, **kw):
            # Return a generic version string except for 'ollama list'
            if cmd[0] == "ollama" and cmd[1] == "list":
                return f"{MODEL_NAME}\t0B\t2023-01-01\n"
            return f"{cmd[0]} version 1.2.3"
        mock_check_output.side_effect = co_side

        mock_resp = unittest.mock.Mock()
        mock_resp.status = 200
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        exit_code = main()
        self.assertEqual(exit_code, 0)

    @unittest.mock.patch("shutil.which")
    def test_missing_opencode(self, mock_which):
        def which_side(cmd):
            if cmd == "opencode":
                return None
            return f"/usr/bin/{cmd}"
        mock_which.side_effect = which_side

        with unittest.mock.patch("subprocess.check_output") as mock_co, \
             unittest.mock.patch("urllib.request.urlopen") as mock_urlopen:
            mock_co.return_value = "ollama version 1.2.3"
            mock_urlopen.return_value = unittest.mock.Mock(status=200)
            exit_code = main()
            self.assertEqual(exit_code, 1)

    @unittest.mock.patch("shutil.which")
    @unittest.mock.patch("urllib.request.urlopen", side_effect=urllib.error.URLError("timeout"))
    @unittest.mock.patch("subprocess.check_output")
    def test_unreachable_server(self, mock_check_output, mock_urlopen, mock_which):
        mock_which.side_effect = lambda cmd: f"/usr/bin/{cmd}"
        mock_check_output.return_value = "ollama version 1.2.3"
        exit_code = main()
        self.assertEqual(exit_code, 1)

    @unittest.mock.patch("shutil.which")
    @unittest.mock.patch("subprocess.check_output")
    @unittest.mock.patch("urllib.request.urlopen")
    def test_similar_model_name(self, mock_urlopen, mock_check_output, mock_which):
        mock_which.side_effect = lambda cmd: f"/usr/bin/{cmd}"

        def co_side(cmd, **kw):
            if cmd[0] == "ollama" and cmd[1] == "list":
                # similar but not exact name
                return f"{MODEL_NAME}-small\t0B\t2023-01-01\n"
            return f"{cmd[0]} version 1.2.3"
        mock_check_output.side_effect = co_side

        mock_resp = unittest.mock.Mock()
        mock_resp.status = 200
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        exit_code = main()
        self.assertEqual(exit_code, 1)

    @unittest.mock.patch("shutil.which")
    @unittest.mock.patch("subprocess.check_output")
    @unittest.mock.patch("urllib.request.urlopen")
    def test_space_separated_list(self, mock_urlopen, mock_check_output, mock_which):
        # Simulate ollama list output using spaces instead of tabs
        mock_which.side_effect = lambda cmd: f"/usr/bin/{cmd}"

        def co_side(cmd, **kw):
            if cmd[0] == "ollama" and cmd[1] == "list":
                return f"{MODEL_NAME} 0B 2023-01-01\n"
            return f"{cmd[0]} version 1.2.3"
        mock_check_output.side_effect = co_side

        mock_resp = unittest.mock.Mock()
        mock_resp.status = 200
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        exit_code = main()
        # Should succeed with correct parser
        self.assertEqual(exit_code, 0)


if __name__ == "__main__":
    unittest.main()
