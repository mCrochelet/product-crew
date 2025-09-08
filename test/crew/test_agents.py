"""
Tests for crew module agents and tasks.
"""

from ..common import main


class TestCrewAIAgent:
    """Test CrewAI agent functionality."""
    
    def test_create_path_printer_agent(self):
        """Test CrewAI agent creation."""
        agent = main.create_path_printer_agent()
        
        assert agent.role == "Path Printer"
        assert "Print file paths exactly" in agent.goal
        assert agent.verbose is False
        assert agent.allow_delegation is False
    
    def test_create_print_paths_task(self, tmp_path):
        """Test CrewAI task creation."""
        req_path = tmp_path / "requirements"
        pid_path = tmp_path / "test.md"
        
        task = main.create_print_paths_task(req_path, pid_path, True)
        
        assert str(req_path) in task.description
        assert str(pid_path) in task.description
        assert "True" in task.description
        assert task.agent is not None