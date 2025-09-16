#!/usr/bin/env python3
"""
CLI unpack command tests - ensures CLI unpack functionality works correctly.
This test would have caught the binary file mode bug in GitHub issue #113.
"""

import os
import tempfile
import shutil
from click.testing import CliRunner
from RAMP import ramp


def test_cli_unpack_binary_files():
    """Test CLI unpack command correctly extracts binary files."""
    
    # Use the existing test bundle
    bundle_path = os.path.join(os.getcwd(), "test_assets", 
                              "redisgears_python.Linux-ubuntu18.04-x86_64.1.2.5.zip")
    
    if not os.path.exists(bundle_path):
        print(f"⚠️  Test bundle not found: {bundle_path}")
        print("   Skipping CLI unpack test")
        return True  # Skip test if bundle not available
    
    # Create temporary directory for extraction
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        
        try:
            # Change to temp directory for extraction
            os.chdir(temp_dir)
            
            # Test CLI unpack command
            runner = CliRunner()
            result = runner.invoke(ramp.unpack, [bundle_path])
            
            # Verify command succeeded
            assert result.exit_code == 0, (
                f"CLI unpack failed with exit code {result.exit_code}\n"
                f"Output: {result.output}\n"
                f"Exception: {result.exception}"
            )
            
            # Check that files were extracted
            extracted_files = os.listdir('.')
            json_files = [f for f in extracted_files if f.endswith('.json')]
            so_files = [f for f in extracted_files if f.endswith('.so')]
            
            assert len(json_files) > 0, f"No JSON metadata file extracted. Files: {extracted_files}"
            assert len(so_files) > 0, f"No .so binary file extracted. Files: {extracted_files}"
            
            # Verify binary file is valid and not corrupted
            so_file = so_files[0]
            file_size = os.path.getsize(so_file)
            assert file_size > 0, f"Binary file {so_file} is empty"
            assert file_size > 1000, f"Binary file {so_file} too small ({file_size} bytes), likely corrupted"
            
            # Check that it's actually a valid binary file (ELF format for Linux modules)
            with open(so_file, 'rb') as f:
                header = f.read(4)
                assert header == b'\x7fELF', (
                    f"Binary file {so_file} corrupted. Expected ELF header (7f454c46), "
                    f"got: {header.hex() if header else 'empty'}"
                )
            
            # Verify JSON metadata file is valid
            json_file = json_files[0]
            json_size = os.path.getsize(json_file)
            assert json_size > 0, f"JSON file {json_file} is empty"
            
            # Verify JSON is parseable
            import json
            with open(json_file, 'r') as f:
                metadata = json.load(f)
                assert isinstance(metadata, dict), "Metadata is not a valid JSON object"
                assert 'module_name' in metadata, "Metadata missing module_name"
                assert 'module_file' in metadata, "Metadata missing module_file"
            
            print("✅ CLI unpack test passed!")
            return True
            
        except Exception as e:
            print(f"❌ CLI unpack test failed: {e}")
            raise
        finally:
            os.chdir(original_cwd)


def test_cli_unpack_nonexistent_file():
    """Test CLI unpack command handles missing files gracefully."""
    
    runner = CliRunner()
    result = runner.invoke(ramp.unpack, ['nonexistent_bundle.zip'])
    
    # Should fail gracefully, not crash
    assert result.exit_code != 0, "Expected failure for nonexistent file"
    assert result.exception is not None or "not found" in result.output.lower()
    
    print("✅ CLI unpack error handling test passed!")
    return True


if __name__ == '__main__':
    print("🧪 Running CLI Unpack Tests")
    print("=" * 35)
    
    try:
        test_cli_unpack_binary_files()
        test_cli_unpack_nonexistent_file()
        print("\n🎉 All CLI unpack tests passed!")
    except Exception as e:
        print(f"\n❌ CLI unpack tests failed: {e}")
        raise