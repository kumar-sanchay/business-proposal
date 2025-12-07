from langchain_core.runnables import Runnable, RunnablePassthrough, retry
from langchain_core.output_parsers import StrOutputParser
from proposal.prompts.data_preprocessing_prompts import executive_summary_ext_prompt
from proposal.core.llm import llm


class ExecutiveSectionChain(Runnable):

    def __get_relevance_chain(self):

        chain = ({
            "context": RunnablePassthrough()
            }
            | executive_summary_ext_prompt
            | llm
            | StrOutputParser()
        )

        chain_with_retry = retry(
            runnable=chain,
            max_retries=5,
            wait_milliseconds=2000
        )

        return chain_with_retry

    def invoke(self, inputs, config=None):
        proposal_document = inputs["proposal_document"]
        
        executive_summary_keywords = ("About", "ABOUT", "Overview", "OVERVIEW", "Introduction", "INTRODUCTION",
                              "Summary", "SUMMARY", "Company", "COMPANY", "Executive","EXECUTIVE")
        
        chain = self.__get_relevance_chain()

        for doc_idx, document in enumerate(proposal_document):

            if document["metadata"]["page_num"] < 4 and any(key in document["text"] for key in executive_summary_keywords):
                
                if chain.invoke(document['text']) == "YES":
                    proposal_document[doc_idx]["metadata"]["section_type"] = "Executive Summary"
        
        return {"proposal_document": proposal_document}