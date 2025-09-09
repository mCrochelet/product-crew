"""Solution evaluation framework for multi-dimensional solution assessment."""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum


class EvaluationDimension(Enum):
    """The four dimensions of solution evaluation."""
    VALUE = "value"          # User value and JTBD served
    VIABILITY = "viability"  # Revenue vs cost analysis  
    FEASIBILITY = "feasibility"  # Implementation complexity
    USABILITY = "usability"  # User experience quality


@dataclass
class SolutionEvaluation:
    """Comprehensive solution evaluation across 4 dimensions."""
    
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
    
    # Sub-dimension breakdowns for transparency
    value_breakdown: Dict[str, float] = field(default_factory=dict)
    viability_breakdown: Dict[str, float] = field(default_factory=dict)
    feasibility_breakdown: Dict[str, float] = field(default_factory=dict)
    usability_breakdown: Dict[str, float] = field(default_factory=dict)
    
    # Weighted composite score
    composite_score: float = 0.0
    
    # Ranking and recommendations
    rank: int = 0
    recommendation: str = ""
    risks: List[str] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    
    def calculate_composite_score(self, weights: Dict[str, float] = None) -> float:
        """Calculate weighted composite score."""
        
        if weights is None:
            weights = {
                "value": 0.3,
                "viability": 0.3, 
                "feasibility": 0.25,
                "usability": 0.15
            }
        
        # Normalize weights to ensure they sum to 1.0
        total_weight = sum(weights.values())
        if total_weight != 1.0:
            weights = {k: v / total_weight for k, v in weights.items()}
        
        self.composite_score = (
            self.value_score * weights.get("value", 0.0) +
            self.viability_score * weights.get("viability", 0.0) +
            self.feasibility_score * weights.get("feasibility", 0.0) + 
            self.usability_score * weights.get("usability", 0.0)
        )
        
        return self.composite_score
    
    def get_dimension_score(self, dimension: EvaluationDimension) -> float:
        """Get score for specific dimension."""
        dimension_map = {
            EvaluationDimension.VALUE: self.value_score,
            EvaluationDimension.VIABILITY: self.viability_score,
            EvaluationDimension.FEASIBILITY: self.feasibility_score,
            EvaluationDimension.USABILITY: self.usability_score
        }
        return dimension_map.get(dimension, 0.0)
    
    def get_dimension_assessment(self, dimension: EvaluationDimension) -> str:
        """Get assessment text for specific dimension."""
        assessment_map = {
            EvaluationDimension.VALUE: self.value_assessment,
            EvaluationDimension.VIABILITY: self.viability_assessment,
            EvaluationDimension.FEASIBILITY: self.feasibility_assessment,
            EvaluationDimension.USABILITY: self.usability_assessment
        }
        return assessment_map.get(dimension, "")
    
    def is_above_threshold(self, dimension: EvaluationDimension, threshold: float = 7.0) -> bool:
        """Check if dimension score is above threshold."""
        return self.get_dimension_score(dimension) >= threshold
    
    def get_weakest_dimension(self) -> EvaluationDimension:
        """Get the dimension with the lowest score."""
        scores = {
            EvaluationDimension.VALUE: self.value_score,
            EvaluationDimension.VIABILITY: self.viability_score,
            EvaluationDimension.FEASIBILITY: self.feasibility_score,
            EvaluationDimension.USABILITY: self.usability_score
        }
        return min(scores.items(), key=lambda x: x[1])[0]
    
    def get_strongest_dimension(self) -> EvaluationDimension:
        """Get the dimension with the highest score."""
        scores = {
            EvaluationDimension.VALUE: self.value_score,
            EvaluationDimension.VIABILITY: self.viability_score,
            EvaluationDimension.FEASIBILITY: self.feasibility_score,
            EvaluationDimension.USABILITY: self.usability_score
        }
        return max(scores.items(), key=lambda x: x[1])[0]


@dataclass
class EvaluationWeights:
    """Configurable weights for solution evaluation dimensions."""
    
    value: float = 0.3
    viability: float = 0.3
    feasibility: float = 0.25
    usability: float = 0.15
    
    def __post_init__(self):
        """Normalize weights to sum to 1.0."""
        total = self.value + self.viability + self.feasibility + self.usability
        if total != 1.0:
            self.value /= total
            self.viability /= total
            self.feasibility /= total
            self.usability /= total
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary format."""
        return {
            "value": self.value,
            "viability": self.viability,
            "feasibility": self.feasibility,
            "usability": self.usability
        }


class SolutionEvaluator:
    """Orchestrates multi-dimensional solution evaluation."""
    
    def __init__(self, context, weights: EvaluationWeights = None):
        """Initialize evaluator with context and optional custom weights."""
        from .context import LifecycleContext
        
        self.context: LifecycleContext = context
        self.weights = weights or EvaluationWeights()
        self.evaluations: Dict[str, SolutionEvaluation] = {}
    
    def evaluate_solutions(self) -> Dict[str, SolutionEvaluation]:
        """Evaluate all solutions across 4 dimensions."""
        
        self.evaluations = {}
        
        for i, solution in enumerate(self.context.solutions):
            solution_id = f"solution_{i+1}"
            evaluation = SolutionEvaluation(
                solution_id=solution_id,
                solution_description=solution.get("description", "")
            )
            
            # Evaluate each dimension
            evaluation.value_score, evaluation.value_assessment, evaluation.value_breakdown = \
                self._evaluate_value(solution)
            
            evaluation.viability_score, evaluation.viability_assessment, evaluation.viability_breakdown = \
                self._evaluate_viability(solution)
            
            evaluation.feasibility_score, evaluation.feasibility_assessment, evaluation.feasibility_breakdown = \
                self._evaluate_feasibility(solution)
            
            evaluation.usability_score, evaluation.usability_assessment, evaluation.usability_breakdown = \
                self._evaluate_usability(solution)
            
            # Calculate composite score
            evaluation.calculate_composite_score(self.weights.to_dict())
            
            # Extract strengths and risks
            evaluation.strengths = self._identify_strengths(evaluation)
            evaluation.risks = self._identify_risks(evaluation)
            
            self.evaluations[solution_id] = evaluation
        
        # Rank solutions by composite score
        self._rank_solutions()
        
        return self.evaluations
    
    def _evaluate_value(self, solution: Dict[str, Any]) -> tuple[float, str, Dict[str, float]]:
        """Evaluate solution value dimension."""
        
        # This would typically delegate to Market Analyst if available
        # For now, provide basic assessment framework
        
        breakdown = {
            "user_value_delivery": 0.0,
            "market_opportunity": 0.0,
            "value_realization": 0.0
        }
        
        # Basic scoring based on solution characteristics
        description = solution.get("description", "").lower()
        features = solution.get("features", [])
        
        # User value delivery (0-10)
        if "user" in description or "customer" in description:
            breakdown["user_value_delivery"] += 3.0
        if features and len(features) >= 3:
            breakdown["user_value_delivery"] += 2.0
        if "problem" in description or "pain" in description:
            breakdown["user_value_delivery"] += 3.0
        if "benefit" in description or "value" in description:
            breakdown["user_value_delivery"] += 2.0
        
        # Market opportunity (0-10)
        if "market" in description or "competitive" in description:
            breakdown["market_opportunity"] += 4.0
        if "scalable" in description or "growth" in description:
            breakdown["market_opportunity"] += 3.0
        if "innovative" in description or "unique" in description:
            breakdown["market_opportunity"] += 3.0
        
        # Value realization (0-10)
        if "quick" in description or "fast" in description:
            breakdown["value_realization"] += 4.0
        if "measurable" in description or "metric" in description:
            breakdown["value_realization"] += 3.0
        if "adoption" in description or "engagement" in description:
            breakdown["value_realization"] += 3.0
        
        # Cap individual scores at 10.0
        for key in breakdown:
            breakdown[key] = min(breakdown[key], 10.0)
        
        overall_score = sum(breakdown.values()) / len(breakdown)
        
        assessment = f"""
        Value Assessment:
        - User Value Delivery: {breakdown['user_value_delivery']:.1f}/10 - How well solution addresses user needs
        - Market Opportunity: {breakdown['market_opportunity']:.1f}/10 - Size and growth potential of market
        - Value Realization: {breakdown['value_realization']:.1f}/10 - Speed and measurability of value delivery
        
        Overall value score reflects solution's potential to deliver meaningful user and business value.
        """
        
        return overall_score, assessment.strip(), breakdown
    
    def _evaluate_viability(self, solution: Dict[str, Any]) -> tuple[float, str, Dict[str, float]]:
        """Evaluate solution business viability."""
        
        breakdown = {
            "revenue_model": 0.0,
            "cost_structure": 0.0,
            "financial_performance": 0.0
        }
        
        # Basic viability assessment
        description = solution.get("description", "").lower()
        complexity = solution.get("complexity", "medium").lower()
        
        # Revenue model assessment (0-10)
        if "revenue" in description or "monetization" in description:
            breakdown["revenue_model"] += 4.0
        if "subscription" in description or "saas" in description:
            breakdown["revenue_model"] += 3.0
        if "scalable" in description:
            breakdown["revenue_model"] += 3.0
        else:
            breakdown["revenue_model"] += 5.0  # Default moderate score
        
        # Cost structure assessment (0-10)
        if complexity == "low":
            breakdown["cost_structure"] += 8.0
        elif complexity == "medium":
            breakdown["cost_structure"] += 6.0
        else:  # high complexity
            breakdown["cost_structure"] += 4.0
        
        if "cloud" in description or "saas" in description:
            breakdown["cost_structure"] += 1.0
        if "integration" in description:
            breakdown["cost_structure"] -= 1.0
        
        # Financial performance projection (0-10)
        if "roi" in description or "profit" in description:
            breakdown["financial_performance"] += 3.0
        if complexity == "low":
            breakdown["financial_performance"] += 4.0
        elif complexity == "medium":
            breakdown["financial_performance"] += 3.0
        else:
            breakdown["financial_performance"] += 2.0
        
        if "quick" in description or "fast" in description:
            breakdown["financial_performance"] += 2.0
        if "scalable" in description:
            breakdown["financial_performance"] += 1.0
        
        # Cap scores at 10.0 and ensure minimum of 0.0
        for key in breakdown:
            breakdown[key] = max(0.0, min(breakdown[key], 10.0))
        
        overall_score = sum(breakdown.values()) / len(breakdown)
        
        assessment = f"""
        Viability Assessment:
        - Revenue Model: {breakdown['revenue_model']:.1f}/10 - Clarity and strength of revenue generation
        - Cost Structure: {breakdown['cost_structure']:.1f}/10 - Efficiency of cost structure
        - Financial Performance: {breakdown['financial_performance']:.1f}/10 - Projected ROI and profitability
        
        Business viability assessment based on revenue potential, cost efficiency, and financial performance.
        """
        
        return overall_score, assessment.strip(), breakdown
    
    def _evaluate_feasibility(self, solution: Dict[str, Any]) -> tuple[float, str, Dict[str, float]]:
        """Evaluate solution technical feasibility (would delegate to Engineering Manager)."""
        
        breakdown = {
            "technical_complexity": 0.0,
            "resource_requirements": 0.0,
            "technical_risks": 0.0
        }
        
        description = solution.get("description", "").lower()
        complexity = solution.get("complexity", "medium").lower()
        
        # Technical complexity assessment (0-10, higher = easier)
        if complexity == "low":
            breakdown["technical_complexity"] = 8.0
        elif complexity == "medium":
            breakdown["technical_complexity"] = 6.0
        else:  # high complexity
            breakdown["technical_complexity"] = 4.0
        
        # Adjust based on technology mentions
        if "ai" in description or "machine learning" in description:
            breakdown["technical_complexity"] -= 2.0
        if "blockchain" in description:
            breakdown["technical_complexity"] -= 2.0
        if "api" in description or "integration" in description:
            breakdown["technical_complexity"] -= 1.0
        if "web" in description or "app" in description:
            breakdown["technical_complexity"] += 1.0
        
        # Resource requirements (0-10, higher = fewer resources needed)
        if complexity == "low":
            breakdown["resource_requirements"] = 8.0
        elif complexity == "medium":
            breakdown["resource_requirements"] = 5.0
        else:
            breakdown["resource_requirements"] = 3.0
        
        if "team" in description:
            breakdown["resource_requirements"] -= 1.0
        if "infrastructure" in description:
            breakdown["resource_requirements"] -= 1.0
        
        # Technical risks (0-10, higher = lower risk)
        breakdown["technical_risks"] = 7.0  # Default moderate risk
        
        if "proven" in description or "standard" in description:
            breakdown["technical_risks"] += 2.0
        if "experimental" in description or "cutting-edge" in description:
            breakdown["technical_risks"] -= 3.0
        if "integration" in description:
            breakdown["technical_risks"] -= 1.0
        if "scalable" in description:
            breakdown["technical_risks"] += 1.0
        
        # Ensure scores are within bounds
        for key in breakdown:
            breakdown[key] = max(0.0, min(breakdown[key], 10.0))
        
        overall_score = sum(breakdown.values()) / len(breakdown)
        
        assessment = f"""
        Feasibility Assessment:
        - Technical Complexity: {breakdown['technical_complexity']:.1f}/10 - Implementation difficulty
        - Resource Requirements: {breakdown['resource_requirements']:.1f}/10 - Team and infrastructure needs
        - Technical Risks: {breakdown['technical_risks']:.1f}/10 - Technical uncertainty and risks
        
        Technical feasibility based on complexity, resource needs, and implementation risks.
        """
        
        return overall_score, assessment.strip(), breakdown
    
    def _evaluate_usability(self, solution: Dict[str, Any]) -> tuple[float, str, Dict[str, float]]:
        """Evaluate solution usability (would delegate to Product Designer)."""
        
        breakdown = {
            "user_experience_quality": 0.0,
            "user_adoption_potential": 0.0,
            "design_implementation": 0.0
        }
        
        description = solution.get("description", "").lower()
        features = solution.get("features", [])
        
        # User experience quality (0-10)
        if "intuitive" in description or "easy" in description:
            breakdown["user_experience_quality"] += 3.0
        if "user-friendly" in description or "simple" in description:
            breakdown["user_experience_quality"] += 3.0
        if "interface" in description or "ui" in description:
            breakdown["user_experience_quality"] += 2.0
        if "accessible" in description:
            breakdown["user_experience_quality"] += 2.0
        else:
            breakdown["user_experience_quality"] += 4.0  # Default moderate score
        
        # User adoption potential (0-10)
        if "onboarding" in description or "training" in description:
            breakdown["user_adoption_potential"] += 3.0
        if "familiar" in description or "standard" in description:
            breakdown["user_adoption_potential"] += 3.0
        if "engaging" in description or "interactive" in description:
            breakdown["user_adoption_potential"] += 2.0
        if "quick" in description or "fast" in description:
            breakdown["user_adoption_potential"] += 2.0
        else:
            breakdown["user_adoption_potential"] += 5.0  # Default moderate score
        
        # Design implementation (0-10)
        if "responsive" in description or "mobile" in description:
            breakdown["design_implementation"] += 3.0
        if "consistent" in description or "standard" in description:
            breakdown["design_implementation"] += 3.0
        if "scalable" in description:
            breakdown["design_implementation"] += 2.0
        if "maintainable" in description:
            breakdown["design_implementation"] += 2.0
        else:
            breakdown["design_implementation"] += 5.0  # Default moderate score
        
        # Ensure scores are within bounds
        for key in breakdown:
            breakdown[key] = max(0.0, min(breakdown[key], 10.0))
        
        overall_score = sum(breakdown.values()) / len(breakdown)
        
        assessment = f"""
        Usability Assessment:
        - User Experience Quality: {breakdown['user_experience_quality']:.1f}/10 - Intuitive and ease of use
        - User Adoption Potential: {breakdown['user_adoption_potential']:.1f}/10 - Learning curve and engagement
        - Design Implementation: {breakdown['design_implementation']:.1f}/10 - Design system and maintenance
        
        Usability evaluation focusing on user experience, adoption ease, and design quality.
        """
        
        return overall_score, assessment.strip(), breakdown
    
    def _identify_strengths(self, evaluation: SolutionEvaluation) -> List[str]:
        """Identify solution strengths based on high scores."""
        strengths = []
        
        if evaluation.value_score >= 8.0:
            strengths.append(f"Strong value proposition (Score: {evaluation.value_score:.1f})")
        if evaluation.viability_score >= 8.0:
            strengths.append(f"Excellent business viability (Score: {evaluation.viability_score:.1f})")
        if evaluation.feasibility_score >= 8.0:
            strengths.append(f"High technical feasibility (Score: {evaluation.feasibility_score:.1f})")
        if evaluation.usability_score >= 8.0:
            strengths.append(f"Outstanding usability (Score: {evaluation.usability_score:.1f})")
        
        if evaluation.composite_score >= 8.0:
            strengths.append(f"Well-balanced solution across all dimensions")
        
        return strengths
    
    def _identify_risks(self, evaluation: SolutionEvaluation) -> List[str]:
        """Identify solution risks based on low scores."""
        risks = []
        
        if evaluation.value_score < 6.0:
            risks.append(f"Limited value proposition (Score: {evaluation.value_score:.1f})")
        if evaluation.viability_score < 6.0:
            risks.append(f"Business viability concerns (Score: {evaluation.viability_score:.1f})")
        if evaluation.feasibility_score < 6.0:
            risks.append(f"Technical implementation risks (Score: {evaluation.feasibility_score:.1f})")
        if evaluation.usability_score < 6.0:
            risks.append(f"User adoption challenges (Score: {evaluation.usability_score:.1f})")
        
        # Check for extreme dimension imbalances
        scores = [evaluation.value_score, evaluation.viability_score, 
                 evaluation.feasibility_score, evaluation.usability_score]
        if max(scores) - min(scores) > 4.0:
            risks.append("Significant imbalance between evaluation dimensions")
        
        return risks
    
    def _rank_solutions(self) -> None:
        """Rank all solutions by composite score."""
        sorted_evaluations = sorted(
            self.evaluations.items(), 
            key=lambda x: x[1].composite_score, 
            reverse=True
        )
        
        for rank, (solution_id, evaluation) in enumerate(sorted_evaluations, 1):
            evaluation.rank = rank
    
    def get_top_solutions(self, n: int = 3) -> List[SolutionEvaluation]:
        """Get top N solutions by composite score."""
        return sorted(
            self.evaluations.values(),
            key=lambda x: x.composite_score,
            reverse=True
        )[:n]
    
    def get_solutions_by_dimension(self, dimension: EvaluationDimension) -> List[SolutionEvaluation]:
        """Get solutions sorted by specific dimension score."""
        return sorted(
            self.evaluations.values(),
            key=lambda x: x.get_dimension_score(dimension),
            reverse=True
        )
    
    def get_evaluation_summary(self) -> Dict[str, Any]:
        """Get summary of all evaluations."""
        if not self.evaluations:
            return {}
        
        evaluations = list(self.evaluations.values())
        
        return {
            "total_solutions": len(evaluations),
            "average_scores": {
                "value": sum(e.value_score for e in evaluations) / len(evaluations),
                "viability": sum(e.viability_score for e in evaluations) / len(evaluations),
                "feasibility": sum(e.feasibility_score for e in evaluations) / len(evaluations),
                "usability": sum(e.usability_score for e in evaluations) / len(evaluations),
                "composite": sum(e.composite_score for e in evaluations) / len(evaluations)
            },
            "best_in_dimension": {
                "value": max(evaluations, key=lambda x: x.value_score).solution_id,
                "viability": max(evaluations, key=lambda x: x.viability_score).solution_id,
                "feasibility": max(evaluations, key=lambda x: x.feasibility_score).solution_id,
                "usability": max(evaluations, key=lambda x: x.usability_score).solution_id
            },
            "top_solution": max(evaluations, key=lambda x: x.composite_score).solution_id,
            "solutions_above_threshold": len([e for e in evaluations if e.composite_score >= 7.0]),
            "balanced_solutions": len([e for e in evaluations if all(
                score >= 6.0 for score in [e.value_score, e.viability_score, e.feasibility_score, e.usability_score]
            )])
        }