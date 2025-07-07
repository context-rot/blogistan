#!/usr/bin/env python3
"""
Test script to validate the base Docker image contains all required dependencies.
This script will be run during the base image build process to ensure everything works.
"""

import sys
import subprocess
import importlib


def test_python_packages():
    """Test that all required Python packages are installed and importable."""
    required_packages = [
        "requests",
        "pandas",
        "numpy",
        "databricks.sdk",
        "databricks.sql",
        "bs4",  # beautifulsoup4
        "git",  # gitpython
        "github",  # PyGithub
        "dspy",
    ]

    print("🔍 Testing Python packages...")
    failed_imports = []

    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"  ✅ {package}")
        except ImportError as e:
            print(f"  ❌ {package} - {e}")
            failed_imports.append(package)

    return len(failed_imports) == 0, failed_imports


def test_command_line_tools():
    """Test that command line tools are available."""
    required_commands = [
        ("python", "--version"),
        ("pip", "--version"),
        ("node", "--version"),
        ("npm", "--version"),
        ("ruby", "--version"),
        ("gem", "--version"),
        ("bundle", "--version"),
        ("jekyll", "--version"),
        ("trufflehog", "--version"),
        ("pre-commit", "--version"),
        ("jq", "--version"),
        ("vibe-tools", "--version"),
    ]

    print("\n🔍 Testing command line tools...")
    failed_commands = []

    for cmd, *args in required_commands:
        try:
            result = subprocess.run(
                [cmd] + list(args), capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                print(f"  ✅ {cmd}")
            else:
                print(f"  ❌ {cmd} - Exit code {result.returncode}")
                print(f"      stderr: {result.stderr.strip()}")
                failed_commands.append(cmd)
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            print(f"  ❌ {cmd} - {e}")
            failed_commands.append(cmd)

    return len(failed_commands) == 0, failed_commands


def test_package_functionality():
    """Test basic functionality of key packages."""
    print("\n🔍 Testing package functionality...")

    tests = []

    # Test pandas basic functionality
    try:
        import pandas as pd

        df = pd.DataFrame({"test": [1, 2, 3]})
        assert len(df) == 3
        print("  ✅ pandas - DataFrame creation works")
        tests.append(True)
    except Exception as e:
        print(f"  ❌ pandas - {e}")
        tests.append(False)

    # Test requests basic functionality
    try:
        import requests

        # Test basic import and class availability
        session = requests.Session()
        print("  ✅ requests - Session creation works")
        tests.append(True)
    except Exception as e:
        print(f"  ❌ requests - {e}")
        tests.append(False)

    # Test beautifulsoup4 functionality
    try:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup("<html><body><p>test</p></body></html>", "html.parser")
        assert soup.find("p").text == "test"
        print("  ✅ beautifulsoup4 - HTML parsing works")
        tests.append(True)
    except Exception as e:
        print(f"  ❌ beautifulsoup4 - {e}")
        tests.append(False)

    # Test GitPython functionality
    try:
        import git

        # Just test import - can't test actual git operations without a repo
        print("  ✅ gitpython - Import successful")
        tests.append(True)
    except Exception as e:
        print(f"  ❌ gitpython - {e}")
        tests.append(False)

    return all(tests), tests


def main():
    """Run all tests and report results."""
    print("🚀 Testing base Docker image dependencies...")
    print("=" * 60)

    # Run all tests
    python_ok, python_failures = test_python_packages()
    cli_ok, cli_failures = test_command_line_tools()
    func_ok, func_tests = test_package_functionality()

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)

    all_passed = python_ok and cli_ok and func_ok

    if python_ok:
        print("✅ Python packages: All imported successfully")
    else:
        print(
            f"❌ Python packages: {len(python_failures)} failed: {', '.join(python_failures)}"
        )

    if cli_ok:
        print("✅ Command line tools: All available")
    else:
        print(
            f"❌ Command line tools: {len(cli_failures)} failed: {', '.join(cli_failures)}"
        )

    if func_ok:
        print("✅ Package functionality: All tests passed")
    else:
        print(
            f"❌ Package functionality: {len([t for t in func_tests if not t])} tests failed"
        )

    print("=" * 60)

    if all_passed:
        print("🎉 ALL TESTS PASSED! Base image is ready for use.")
        sys.exit(0)
    else:
        print("💥 SOME TESTS FAILED! Base image needs fixes.")
        sys.exit(1)


if __name__ == "__main__":
    main()
