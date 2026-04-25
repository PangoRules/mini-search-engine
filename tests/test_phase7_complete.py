"""Test to verify the complete implementation of Phase 7 components."""
import pytest
import os

def test_dockerfile_exists():
    """Test that Dockerfile exists."""
    assert os.path.exists("Dockerfile") == True
    print("✓ Dockerfile exists")

def test_docker_compose_exists():
    """Test that docker-compose.yml exists."""
    assert os.path.exists("docker-compose.yml") == True
    print("✓ docker-compose.yml exists")

def test_readme_has_docker_section():
    """Test that README has a Docker section."""
    with open("README.md", "r") as f:
        content = f.read()
        assert "## Docker Setup" in content
    print("✓ README has Docker section")

if __name__ == "__main__":
    test_dockerfile_exists()
    test_docker_compose_exists()
    test_readme_has_docker_section()
    print("All Phase 7 component tests passed! ✅")