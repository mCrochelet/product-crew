# Task 02: Multi-Phase Delegation Workflow Design

## Executive Summary

Based on Task 01 analysis, this document designs a comprehensive 7-phase product refinement lifecycle that transforms the current single-pass delegation into a structured, iterative workflow with conditional logic and solution evaluation.

## Phase Architecture Design

### Phase Flow Overview
```
┌─────────────────────────────────────────────────────────────────┐
│                    Product Manager Orchestrator                 │
└─────────────────────────┬───────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────┐
│ Phase 1: Understand Problem                                     │
│ • Analyze existing data completeness                            │
│ • Conditional: Delegate to Market Analyst if research needed    │
│ • Output: Problem understanding assessment                      │
└─────────────────────────┬───────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────┐
│ Phase 2: Define Problem                                         │
│ • Create clear problem statement and domain                     │
│ • Conditional: Delegate to Market Analyst + Functional Analyst │
│ • Output: Problem definition and scope                          │
└─────────────────────────┬───────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────┐
│ Phase 3: Ideate Solutions                                       │
│ • Delegate to ALL agents for solution generation                │
│ • Generate multiple solution options                            │
│ • Output: Solution portfolio with alternatives                  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────┐
│ Phase 4: Validate Solutions                                     │
│ • Value Assessment (Market Analyst - conditional)               │
│ • Viability Assessment (Product Manager)                        │
│ • Feasibility Assessment (Engineering Manager)                  │
│ • Usability Assessment (Product Designer)                       │
│ • Output: Solution evaluation matrix                            │
└─────────────────────────┬───────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────┐
│ Phase 5: Refine Solutions                                       │
│ • Delegate to Product Designer (UX refinement)                  │
│ • Delegate to Functional Analyst (requirements refinement)      │
│ • Delegate to Engineering Manager (technical refinement)        │
│ • Output: Refined solution alternatives                         │
└─────────────────────────┬───────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────┐
│ Phase 6: Select Best Solution                                   │
│ • Product Manager synthesizes all evaluation data               │
│ • Apply selection criteria and decision framework               │
│ • Output: Selected solution with rationale                      │
└─────────────────────────┬───────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────┐
│ Phase 7: Plan Implementation                                    │
│ • Delegate to Functional Analyst (requirements breakdown)       │
│ • Delegate to Scrum Master (delivery planning)                  │
│ • Delegate to Engineering Manager (technical planning)          │
│ • Output: Implementation roadmap and tasks                      │
└─────────────────────────────────────────────────────────────────┘
```

## Phase Controller Architecture

### Core Components

#### 1. LifecycleContext Class
```python
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from enum import Enum

class PhaseStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class LifecycleContext:
    """Maintains state across all lifecycle phases"""
    
    # Input data
    requirements_path: Path
    pid_path: Path
    original_pid_content: str
    model: str
    
    # Phase execution state
    current_phase: int = 1
    phase_status: Dict[int, PhaseStatus] = None
    phase_results: Dict[int, Dict[str, Any]] = None
    
    # Problem understanding
    problem_clarity_score: float = 0.0
    research_needed: bool = True
    problem_statement: str = ""
    problem_domain: str = ""
    
    # Solution data
    solutions: List[Dict[str, Any]] = None
    solution_evaluations: Dict[str, Dict[str, float]] = None
    selected_solution: Optional[Dict[str, Any]] = None
    
    # Implementation planning
    implementation_plan: Optional[Dict[str, Any]] = None
    
    # PID progressive enhancement
    pid_sections: Dict[str, str] = None
    
    def __post_init__(self):
        if self.phase_status is None:
            self.phase_status = {i: PhaseStatus.PENDING for i in range(1, 8)}
        if self.phase_results is None:
            self.phase_results = {}
        if self.solutions is None:
            self.solutions = []
        if self.solution_evaluations is None:
            self.solution_evaluations = {}
        if self.pid_sections is None:
            self.pid_sections = {}
```

#### 2. Phase Controller Engine
```python
class ProductLifecycleController:
    """Controls execution of the 7-phase product refinement lifecycle"""
    
    def __init__(self, context: LifecycleContext):
        self.context = context
        self.agents = self._create_agent_pool()
        
    def execute_lifecycle(self, demo: bool = False) -> str:
        """Execute complete 7-phase lifecycle"""
        
        for phase_num in range(1, 8):
            try:
                self.context.current_phase = phase_num
                self.context.phase_status[phase_num] = PhaseStatus.IN_PROGRESS
                
                if demo:
                    self._display_phase_start(phase_num)
                
                # Execute phase-specific logic
                phase_result = self._execute_phase(phase_num)
                
                # Store results and update context
                self.context.phase_results[phase_num] = phase_result
                self._update_context_from_phase(phase_num, phase_result)
                
                # Validate phase completion
                if self._validate_phase_completion(phase_num):
                    self.context.phase_status[phase_num] = PhaseStatus.COMPLETED
                else:
                    # Handle incomplete phase
                    retry_result = self._handle_incomplete_phase(phase_num)
                    if not retry_result:
                        self.context.phase_status[phase_num] = PhaseStatus.FAILED
                        break
                
                if demo:
                    self._display_phase_completion(phase_num)
                    
            except Exception as e:
                self.context.phase_status[phase_num] = PhaseStatus.FAILED
                if demo:
                    self._display_phase_error(phase_num, str(e))
                # Decide whether to continue or abort
                if not self._should_continue_after_failure(phase_num):
                    break
        
        # Generate final PID
        return self._generate_final_pid()
```

## Conditional Delegation Framework

### Delegation Decision Engine
```python
class DelegationDecisionEngine:
    """Determines when and how to delegate to specific agents"""
    
    @staticmethod
    def should_delegate_market_research(context: LifecycleContext, phase: int) -> bool:
        """Determine if Market Analyst delegation is needed"""
        
        if phase == 1:  # Understand Problem
            # Check data completeness
            data_completeness = DelegationDecisionEngine._assess_data_completeness(context)
            return data_completeness < 0.7  # Threshold for sufficient data
            
        elif phase == 2:  # Define Problem  
            # Check problem statement clarity
            return context.problem_clarity_score < 0.8
            
        elif phase == 4:  # Validate Solutions - Value Assessment
            # Only if we need market validation
            return len(context.solutions) > 1  # Multiple solutions need market input
            
        return False
    
    @staticmethod
    def should_delegate_functional_analysis(context: LifecycleContext, phase: int) -> bool:
        """Determine if Functional Analyst delegation is needed"""
        
        if phase == 2:  # Define Problem
            # Check if problem domain needs clarification
            return not context.problem_domain or len(context.problem_domain) < 50
            
        elif phase == 5:  # Refine Solutions
            # Always needed for requirements refinement
            return True
            
        elif phase == 7:  # Plan Implementation
            # Always needed for implementation breakdown
            return True
            
        return False
    
    @staticmethod
    def _assess_data_completeness(context: LifecycleContext) -> float:
        """Assess completeness of available data (0.0 to 1.0)"""
        
        score = 0.0
        checks = 0
        
        # Check original PID content quality
        if context.original_pid_content:
            content_length = len(context.original_pid_content.strip())
            if content_length > 200:
                score += 0.3
            elif content_length > 100:
                score += 0.2
            elif content_length > 50:
                score += 0.1
        checks += 1
        
        # Check for problem statement
        if "problem" in context.original_pid_content.lower():
            score += 0.3
        checks += 1
        
        # Check for solution hints
        if "solution" in context.original_pid_content.lower():
            score += 0.2
        checks += 1
        
        # Check for user/customer mentions
        if any(term in context.original_pid_content.lower() for term in ["user", "customer", "client"]):
            score += 0.2
        checks += 1
        
        return score / checks if checks > 0 else 0.0
```

## Solution Evaluation System

### Multi-Dimensional Evaluation Framework
```python
from enum import Enum
from dataclasses import dataclass

class EvaluationDimension(Enum):
    VALUE = "value"          # User value and JTBD served
    VIABILITY = "viability"  # Revenue vs cost analysis  
    FEASIBILITY = "feasibility"  # Implementation complexity
    USABILITY = "usability"  # User experience quality

@dataclass
class SolutionEvaluation:
    """Comprehensive solution evaluation across 4 dimensions"""
    
    solution_id: str
    solution_description: str
    
    # Evaluation scores (0.0 to 10.0)
    value_score: float = 0.0
    viability_score: float = 0.0  
    feasibility_score: float = 0.0
    usability_score: float = 0.0
    
    # Detailed assessments
    value_assessment: str = ""
    viability_assessment: str = ""
    feasibility_assessment: str = ""
    usability_assessment: str = ""
    
    # Weighted composite score
    composite_score: float = 0.0
    
    # Ranking and recommendations
    rank: int = 0
    recommendation: str = ""
    risks: List[str] = None
    
    def __post_init__(self):
        if self.risks is None:
            self.risks = []
    
    def calculate_composite_score(self, weights: Dict[str, float] = None) -> float:
        """Calculate weighted composite score"""
        
        if weights is None:
            weights = {
                "value": 0.3,
                "viability": 0.3, 
                "feasibility": 0.25,
                "usability": 0.15
            }
        
        self.composite_score = (
            self.value_score * weights["value"] +
            self.viability_score * weights["viability"] +
            self.feasibility_score * weights["feasibility"] + 
            self.usability_score * weights["usability"]
        )
        
        return self.composite_score

class SolutionEvaluator:
    """Orchestrates multi-dimensional solution evaluation"""
    
    def __init__(self, context: LifecycleContext):
        self.context = context
        
    def evaluate_solutions(self) -> Dict[str, SolutionEvaluation]:
        """Evaluate all solutions across 4 dimensions"""
        
        evaluations = {}
        
        for i, solution in enumerate(self.context.solutions):
            solution_id = f"solution_{i+1}"
            evaluation = SolutionEvaluation(
                solution_id=solution_id,
                solution_description=solution.get("description", "")
            )
            
            # Delegate dimension-specific evaluations
            evaluation.value_score, evaluation.value_assessment = self._evaluate_value(solution)
            evaluation.viability_score, evaluation.viability_assessment = self._evaluate_viability(solution)
            evaluation.feasibility_score, evaluation.feasibility_assessment = self._evaluate_feasibility(solution)
            evaluation.usability_score, evaluation.usability_assessment = self._evaluate_usability(solution)
            
            # Calculate composite score
            evaluation.calculate_composite_score()
            
            evaluations[solution_id] = evaluation
        
        # Rank solutions by composite score
        sorted_evaluations = sorted(evaluations.items(), key=lambda x: x[1].composite_score, reverse=True)
        for rank, (solution_id, evaluation) in enumerate(sorted_evaluations, 1):
            evaluation.rank = rank
        
        return evaluations
    
    def _evaluate_value(self, solution: Dict[str, Any]) -> tuple[float, str]:
        """Delegate value assessment to Market Analyst if needed"""
        
        if DelegationDecisionEngine.should_delegate_market_research(self.context, 4):
            # Create task for Market Analyst
            return self._delegate_value_assessment(solution)
        else:
            # Product Manager does basic value assessment
            return self._basic_value_assessment(solution)
    
    def _evaluate_feasibility(self, solution: Dict[str, Any]) -> tuple[float, str]:
        """Delegate feasibility assessment to Engineering Manager"""
        return self._delegate_feasibility_assessment(solution)
    
    def _evaluate_usability(self, solution: Dict[str, Any]) -> tuple[float, str]:
        """Delegate usability assessment to Product Designer"""  
        return self._delegate_usability_assessment(solution)
```

## Phase Transition Logic

### Phase Completion Criteria
```python
class PhaseValidator:
    """Validates phase completion and determines transition readiness"""
    
    @staticmethod
    def validate_phase_1(context: LifecycleContext) -> bool:
        """Validate Problem Understanding phase completion"""
        
        required_elements = [
            context.problem_clarity_score > 0.5,
            len(context.phase_results.get(1, {}).get("analysis", "")) > 100,
            context.research_needed is not None  # Decision made about additional research
        ]
        
        return all(required_elements)
    
    @staticmethod  
    def validate_phase_2(context: LifecycleContext) -> bool:
        """Validate Problem Definition phase completion"""
        
        required_elements = [
            bool(context.problem_statement),
            len(context.problem_statement) > 50,
            bool(context.problem_domain),
            context.problem_clarity_score > 0.7
        ]
        
        return all(required_elements)
    
    @staticmethod
    def validate_phase_3(context: LifecycleContext) -> bool:
        """Validate Solution Ideation phase completion"""
        
        return (
            len(context.solutions) >= 2 and  # At least 2 solution options
            all("description" in sol for sol in context.solutions) and
            all(len(sol["description"]) > 100 for sol in context.solutions)
        )
    
    @staticmethod
    def validate_phase_4(context: LifecycleContext) -> bool:
        """Validate Solution Validation phase completion"""
        
        return (
            len(context.solution_evaluations) == len(context.solutions) and
            all(eval.composite_score > 0 for eval in context.solution_evaluations.values())
        )
    
    @staticmethod
    def validate_phase_6(context: LifecycleContext) -> bool:
        """Validate Solution Selection phase completion"""
        
        return (
            context.selected_solution is not None and
            "rationale" in context.selected_solution and
            len(context.selected_solution["rationale"]) > 100
        )
    
    @staticmethod
    def validate_phase_7(context: LifecycleContext) -> bool:
        """Validate Implementation Planning phase completion"""
        
        plan = context.implementation_plan
        if not plan:
            return False
            
        required_sections = ["tasks", "timeline", "resources", "risks"]
        return all(section in plan for section in required_sections)

class PhaseTransitionManager:
    """Manages transitions between lifecycle phases"""
    
    def __init__(self, context: LifecycleContext):
        self.context = context
        self.validator = PhaseValidator()
    
    def can_transition_to_phase(self, target_phase: int) -> tuple[bool, str]:
        """Check if ready to transition to target phase"""
        
        current_phase = self.context.current_phase
        
        # Can't skip phases
        if target_phase != current_phase + 1:
            return False, f"Cannot skip from phase {current_phase} to {target_phase}"
        
        # Validate current phase completion
        validation_method = getattr(self.validator, f"validate_phase_{current_phase}", None)
        if validation_method and not validation_method(self.context):
            return False, f"Phase {current_phase} validation failed"
        
        return True, "Ready for transition"
    
    def execute_phase_transition(self, target_phase: int) -> bool:
        """Execute transition to target phase"""
        
        can_transition, message = self.can_transition_to_phase(target_phase)
        if not can_transition:
            return False
        
        # Update context for new phase
        self.context.current_phase = target_phase
        self.context.phase_status[target_phase] = PhaseStatus.IN_PROGRESS
        
        return True
```

## Technical Implementation Approach

### File Structure
```
product_crew/crew/
├── lifecycle/
│   ├── __init__.py
│   ├── controller.py          # ProductLifecycleController
│   ├── context.py            # LifecycleContext, PhaseStatus
│   ├── delegation.py         # DelegationDecisionEngine  
│   ├── evaluation.py         # SolutionEvaluator, SolutionEvaluation
│   ├── validation.py         # PhaseValidator, PhaseTransitionManager
│   └── phases/
│       ├── __init__.py
│       ├── phase_01_understand.py
│       ├── phase_02_define.py
│       ├── phase_03_ideate.py
│       ├── phase_04_validate.py
│       ├── phase_05_refine.py
│       ├── phase_06_select.py
│       └── phase_07_plan.py
```

### Integration Points

#### 1. Runner Integration
```python
# In runner.py
def run_lifecycle_workflow(requirements_path: Path, pid_path: Path, overwrite: bool, 
                          demo: bool = False, model: str = 'gpt-4o') -> str:
    """Run the 7-phase product refinement lifecycle"""
    
    # Initialize lifecycle context
    context = LifecycleContext(
        requirements_path=requirements_path,
        pid_path=pid_path,
        original_pid_content=pid_path.read_text(),
        model=model
    )
    
    # Create and run lifecycle controller
    controller = ProductLifecycleController(context)
    return controller.execute_lifecycle(demo=demo)
```

#### 2. Task System Integration
```python 
# In tasks.py
def create_lifecycle_workflow_task(requirements_path: Path, pid_path: Path, model: str = 'gpt-4o') -> Task:
    """Create lifecycle-based task (replaces current orchestration)"""
    
    return Task(
        description="Execute 7-phase product refinement lifecycle with conditional delegation",
        expected_output="Comprehensive PID created through structured lifecycle process",
        agent=create_product_manager_agent(model)
    )
```

## Decision Framework

### Solution Selection Criteria
```python
class SolutionSelectionFramework:
    """Framework for systematic solution selection"""
    
    def __init__(self, context: LifecycleContext):
        self.context = context
    
    def select_best_solution(self) -> Dict[str, Any]:
        """Apply selection criteria to choose optimal solution"""
        
        evaluations = self.context.solution_evaluations
        
        # Primary selection by composite score
        best_by_score = max(evaluations.values(), key=lambda e: e.composite_score)
        
        # Secondary criteria checks
        selection_rationale = []
        
        # Risk tolerance check
        acceptable_risk_solutions = [
            eval for eval in evaluations.values()
            if len(eval.risks) <= 3  # Risk threshold
        ]
        
        # Feasibility threshold
        feasible_solutions = [
            eval for eval in evaluations.values()  
            if eval.feasibility_score >= 6.0  # Feasibility threshold
        ]
        
        # Apply selection logic
        candidates = list(set(acceptable_risk_solutions) & set(feasible_solutions))
        
        if candidates:
            selected = max(candidates, key=lambda e: e.composite_score)
            selection_rationale.append("Selected from low-risk, feasible solutions")
        else:
            selected = best_by_score
            selection_rationale.append("Selected highest scoring solution despite risk/feasibility concerns")
        
        return {
            "solution": selected,
            "rationale": ". ".join(selection_rationale),
            "alternatives_considered": len(evaluations),
            "selection_criteria": ["composite_score", "risk_tolerance", "feasibility_threshold"]
        }
```

## Success Criteria and Validation

### Implementation Success Metrics

1. **Architecture Completeness**
   - ✅ All 7 phases implemented with specific logic
   - ✅ Conditional delegation working correctly
   - ✅ Solution evaluation framework operational
   - ✅ Phase transition logic validated

2. **Quality Improvements**
   - Target: 40% improvement in PID completeness vs current system
   - Target: Solutions evaluated across all 4 dimensions
   - Target: Implementation plans 60% more detailed

3. **Performance Targets**
   - Complete lifecycle execution < 15 minutes
   - Phase validation accuracy > 95%
   - Conditional delegation precision > 90%

### Validation Approach

1. **Unit Testing**: Each phase, evaluation dimension, delegation condition
2. **Integration Testing**: Full lifecycle execution, phase transitions
3. **Quality Testing**: PID output assessment, solution selection accuracy
4. **Performance Testing**: Execution time, resource utilization

## Best Practices Implementation

### Multi-Agent Delegation Best Practices

1. **Clear Agent Responsibilities**: Each agent has well-defined role per phase
2. **Context Passing**: Rich context shared between phases and agents
3. **Error Handling**: Graceful degradation when agents fail
4. **Validation Gates**: Quality checks before phase transitions
5. **Documentation Standards**: Each task and tool documented with purpose

### Framework Documentation Requirements

1. **Phase Documentation**: Each phase with clear inputs/outputs/decisions
2. **Agent Integration Docs**: How each agent contributes per phase  
3. **Evaluation Metrics**: Detailed scoring rubrics and criteria
4. **Error Scenarios**: Common failure modes and recovery strategies
5. **Configuration Options**: Customizable thresholds and weights

This comprehensive design provides the foundation for transforming the current single-pass delegation into a sophisticated, iterative product refinement lifecycle that follows industry best practices and delivers significantly improved PID quality.