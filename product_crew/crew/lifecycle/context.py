"""Lifecycle context and state management."""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum
from pathlib import Path


class PhaseStatus(Enum):
    """Status of individual lifecycle phases."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class LifecycleContext:
    """Maintains state across all lifecycle phases."""
    
    # Input data
    requirements_path: Path
    pid_path: Path
    original_pid_content: str
    model: str
    
    # Phase execution state
    current_phase: int = 1
    phase_status: Dict[int, PhaseStatus] = field(default_factory=dict)
    phase_results: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    
    # Problem understanding
    problem_clarity_score: float = 0.0
    research_needed: bool = True
    problem_statement: str = ""
    problem_domain: str = ""
    
    # Solution data
    solutions: List[Dict[str, Any]] = field(default_factory=list)
    solution_evaluations: Dict[str, Dict[str, float]] = field(default_factory=dict)
    selected_solution: Optional[Dict[str, Any]] = None
    
    # Implementation planning
    implementation_plan: Optional[Dict[str, Any]] = None
    
    # PID progressive enhancement
    pid_sections: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize default values."""
        if not self.phase_status:
            self.phase_status = {i: PhaseStatus.PENDING for i in range(1, 8)}
    
    def get_phase_result(self, phase: int, key: str = None) -> Any:
        """Get result from specific phase."""
        phase_data = self.phase_results.get(phase, {})
        if key:
            return phase_data.get(key)
        return phase_data
    
    def set_phase_result(self, phase: int, key: str, value: Any) -> None:
        """Set result for specific phase."""
        if phase not in self.phase_results:
            self.phase_results[phase] = {}
        self.phase_results[phase][key] = value
    
    def is_phase_complete(self, phase: int) -> bool:
        """Check if phase is completed."""
        return self.phase_status.get(phase) == PhaseStatus.COMPLETED
    
    def get_completed_phases(self) -> List[int]:
        """Get list of completed phases."""
        return [
            phase for phase, status in self.phase_status.items()
            if status == PhaseStatus.COMPLETED
        ]