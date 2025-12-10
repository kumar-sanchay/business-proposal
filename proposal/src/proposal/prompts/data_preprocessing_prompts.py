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