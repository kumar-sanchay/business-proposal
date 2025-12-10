from langchain_core.prompts import PromptTemplate


executive_summary_ext_prompt = PromptTemplate.from_template(
    """
    You are a classifier. Determine whether this section is acting as an 
    executive summary in a consulting proposal.

    Executive summary indicators:
    - Good Information about the firm and what the firm does
    - High-level overview of the client’s goals or needs
    - High-level description of the provider and solution
    - Explains value, outcomes, and strategic approach
    - Non-technical, business-focused language

    Return only: “YES” or “NO”.
    Even if 1 summary indicators is valid then return "YES" otherwise "NO"

    Section Content:
    {context}
    """
)


problem_statement_ext_prompt = PromptTemplate.from_template(
    """"
    You are a strict classifier.

    Your task: Determine whether the provided section text is acting as a *Problem Statement* in a consulting business proposal.

    A section IS a "Problem Statement" if it:
    - Describes a challenge, issue, gap, or pain point faced by the client.
    - Mentions obstacles, inefficiencies, bottlenecks, missed opportunities, or business risks.
    - States why the current situation is problematic or needs change.
    - Highlights negative outcomes, constraints, or unmet goals.

    A section is NOT a "Problem Statement" if it:
    - Describes a solution, methodology, or approach.
    - Talks about features, deliverables, or project scope.
    - States company background, credentials, or experience.
    - Provides general context without identifying a problem.
    - Describes benefits, future goals, or value proposition.

    You MUST follow the output format:
    - Output **only** one word: `YES` if the text is a problem statement, otherwise `NO`.
    - No explanation. No additional words. No punctuation.

    Section Content:
    {context}
    """
)


approach_ext_prompt = PromptTemplate.from_template(
    """
    You are a strict binary classifier.

    Your task: Determine whether the provided section text represents a *Proposed Solution or Approach* in a consulting business proposal.

    A section IS a "Proposed Solution / Approach" if it:
    - Describes how the consulting firm plans to solve the client's problem.
    - Outlines steps, phases, activities, or methodology.
    - Explains actions the team will take.
    - Describes frameworks, strategies, or implementation plans.
    - Explains deliverables, solution components, or workstreams.
    - Talks about tools, techniques, or processes that will be applied.

    A section is NOT a "Proposed Solution / Approach" if it:
    - Describes the client’s current problems, challenges, or pain points.
    - Talks about the client's background or industry context.
    - Describes the firm’s credentials, experience, or company information.
    - Lists project goals, outcomes, or benefits without specifying the solution.
    - Contains general narrative without describing a solution or method.

    You MUST follow the output rules:
    - Output exactly one word: YES or NO.
    - No explanation. No additional words. No punctuation.

    Section Context:
    {context}
    """
)