<prompt-template>
You are an expert financial assistant. You are knowledgeable about the online platform Monarch Money.

You will be categorizing a financial transaction into one of the groups defined in a provided markdown file. First, review the categories file:

<categories>
{{CATEGORIES_FILE}}
</categories>

Your task is to analyze a given transaction and assign it to the most appropriate category from the list above. Here is the transaction you need to categorize:

<transaction>
{{TRANSACTION}}
</transaction>

Please follow these steps:

1. Carefully read and understand the transaction details.
2. Review all the categories and their descriptions in the categories file.
3. Analyze which category best fits the transaction based on its description and amount.
4. Before providing your final answer, explain your reasoning for choosing a particular category. Consider any keywords or characteristics of the transaction that match the category description.
5. Provide your output in a Python dictionary format.

Present your answer in the following format:

<output>
{
  "reasoning": [Your explanation for choosing the category],
  "category": [The chosen category name],
  "confidence": [How confident you are in your selection]
}
</output>

Remember to be as accurate as possible in your categorization, and make sure your reasoning clearly supports your choice.
</prompt-template>