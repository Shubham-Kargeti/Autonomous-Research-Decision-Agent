export interface Step {
  id: number;
  action: string;
  details: string;
  tool: string | null;
  tool_input: any | null;
}

export interface ExecutionResult {
  step_id: number;
  action: string;
  status: string;
  critic_reason: string;
  tool_used: string | null;
  tool_output: any;
  retries: number;
}
