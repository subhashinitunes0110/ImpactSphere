export interface ProjectProposal {
  id: string;
  name: string;
  sector: string;
  location: string;
  district: string;
  budget: number;
  beneficiaries: number;
  needScore: number;
  impactScore: number;
  efficiencyScore: number;
  status: "Recommended" | "Under Review" | "Rejected";
}

export interface PortfolioSummary {
  cycle: string;
  mandatoryBudget: number;
  allocatedBudget: number;
  totalProposals: number;
  recommendedCount: number;
  averageImpact: number;
}