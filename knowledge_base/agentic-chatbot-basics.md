# Agentic chatbot basics

A chatbot is agentic when the model can choose from a bounded set of tools, the application executes those tools, and their results are returned to the model before it answers. A tool call is a request from the model; it is not permission for the model to execute arbitrary code.

## The sample tool

`search_knowledge_base` searches Markdown files in this repository. It is read-only, local, limited to five results, and returns source filenames with short excerpts. It cannot read files outside the configured knowledge directory or access the network.

## Context and caching

A request's context includes instructions, tool schemas, conversation history, the current question, retrieved excerpts, and reserved output/reasoning space. Provider prompt caching can reuse computation for matching input prefixes; it does not return an old answer. The sample's local exact-query cache stores deterministic search results for the current content snapshot.
