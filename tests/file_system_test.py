"""Tests for the file_system functions."""
import unittest
from pathlib import WindowsPath
from unittest.mock import Mock

import library.helpers.file_system as file_system


class TestFileSystemHelpers(unittest.TestCase):
    def test_get_nested_directories(self):
        """Test get_nested_directories."""
        start_menu_directory = Mock(WindowsPath)
        start_menu_directory.__repr__ = Mock(return_value="Start Menu")
        programs_directory = Mock(WindowsPath)
        programs_directory.__repr__ = Mock(return_value="Programs")
        test_directory_one = Mock(WindowsPath)
        test_directory_one.__repr__ = Mock(return_value="Test Directory One")
        nested_test_directory_one = Mock(WindowsPath)
        nested_test_directory_one.__repr__ = Mock(return_value="Nested Test Directory One")
        nested_test_directory_two = Mock(WindowsPath)
        nested_test_directory_two.__repr__ = Mock(return_value="Nested Test Directory Two")

        start_menu_directory.iterdir = Mock(
            return_value=[programs_directory]
        )
        start_menu_directory.is_dir = Mock(return_value=True)
        programs_directory.iterdir = Mock(
            return_value=[test_directory_one]
        )
        programs_directory.is_dir = Mock(return_value=True)
        test_directory_one.iterdir = Mock(
            return_value=[nested_test_directory_one, nested_test_directory_two]
        )
        test_directory_one.is_dir = Mock(return_value=True)
        nested_test_directory_one.iterdir = Mock(return_value=[])
        nested_test_directory_one.is_dir = Mock(return_value=True)
        nested_test_directory_two.iterdir = Mock(return_value=[])
        nested_test_directory_two.is_dir = Mock(return_value=True)

        nested_directories = file_system.get_nested_directories(start_menu_directory)
        self.assertListEqual(
            nested_directories,
            [
                programs_directory,
                test_directory_one,
                nested_test_directory_one,
                nested_test_directory_two,
            ],
        )


if __name__ == "__main__":
    unittest.main()
