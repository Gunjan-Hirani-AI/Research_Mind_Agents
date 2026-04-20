from agents import build_search_agent, build_read_agent, writer_chain, critic_chain

def run_research_pipeline(topic):
    
    state = {}
    
    #----> 1
    
    search_agent = build_search_agent()
    search_results = search_agent.invoke({
        "messages":[("user",f"Find recent, reliable and detailed information about: {topic}")] 
    })
    state["search_results"] = search_results['messages'][-1].content
    
    print("Search Results:", state["search_results"])
    
     #----> 2
    
    reader_agent = build_read_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}"
        )]
    })
    state['scraped_content'] = reader_result['messages'][-1].content
    
    print("Reader Results:", state["scraped_content"])
    
     #----> 3
     
    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )
      
    state["report"] = writer_chain.invoke({
        "topic" : topic,
        "research" : research_combined
    })
    
    print("\n Final Report\n",state['report'])

    state["feedback"] = critic_chain.invoke({
        "report":state['report']
    })
    
    print("\n critic report \n", state['feedback'])

    return state

if __name__ == "__main__":
    topic = input('\n Enter a research topic :')
    run_research_pipeline(topic)
    