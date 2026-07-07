from agents import built_search_agent, built_reader_agent, writer_chain, critic_chain


def run_research_pipeline(topic: str) -> dict:
    state = {}

    # -------------------------
    # 1. SEARCH AGENT
    # -------------------------
    search_agent = built_search_agent()

    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })

    state["search_result"] = search_result["messages"][-1].content

    # -------------------------
    # 2. READER AGENT
    # -------------------------
    reader_agent = built_reader_agent()

    reader_result = reader_agent.invoke({
        "messages": [(
            "user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search result:\n{state['search_result'][:800]}"
        )]
    })

    state["scraped_content"] = reader_result["messages"][-1].content

    # -------------------------
    # 3. WRITER
    # -------------------------
    research_combined = (
        f"Search Results:\n{state['search_result']}\n\n"
        f"Scraped Content:\n{state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    }).content

    # -------------------------
    # 4. CRITIC
    # -------------------------
    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    }).content

    return state


if __name__ == "__main__":
    topic = input("\nEnter a Research Topic: ")
    result = run_research_pipeline(topic)

    print("\n\n===== FINAL REPORT =====\n")
    print(result["report"])

    print("\n\n===== FEEDBACK =====\n")
    print(result["feedback"])