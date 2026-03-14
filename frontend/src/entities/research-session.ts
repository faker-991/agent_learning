export type ResearchSession = {
  id: string;
  workspace_id: string;
  question: string;
  intent_type: string;
  time_window_years: number;
  status: string;
  plan_snapshot?: Record<string, unknown> | null;
  retrieved_paper_ids: string[];
  selected_paper_ids: string[];
  research_card_id?: string | null;
};

