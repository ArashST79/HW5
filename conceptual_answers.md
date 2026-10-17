# Conceptual questions

## 1. A realistic use case for the 311 project

New York City service managers could use this dashboard to compare the average time taken to close 311 complaints across ZIP codes each month. Comparing two ZIP codes with the citywide average could help them identify areas with consistently longer closure times and decide where to investigate staffing, workload, or service processes.

The dashboard supports further investigation rather than explaining the causes of delays. For example, an area's longer average closure time might reflect a larger proportion of complicated complaints rather than slower service.

## 2. Refining the My Little Pony question

The original question—“We'd like to understand how much characters talk across the My Little Pony series”—is too broad to measure consistently. I would refine it as follows:

1. **Define the series and scope.** Use all regular episodes from seasons 1–9 of *My Little Pony: Friendship Is Magic*, excluding movies and specials.
2. **Define the characters.** Include every character with identifiable dialogue in the episode transcripts.
3. **Define “how much they talk.”** Count spoken words attributed to each character. Exclude stage directions and song lyrics, and record dialogue with an unclear speaker separately.
4. **Define the comparison.** Calculate each character's total spoken-word count and percentage of all counted dialogue across the series. Also calculate these measures by season to show how their contributions change.

The refined question is: **“Across seasons 1–9 of My Little Pony: Friendship Is Magic, how many spoken words does each character have, what percentage of the series' counted dialogue does that represent, and how does that percentage vary by season?”**

To answer it, I would need episode transcripts with speaker labels, season and episode identifiers, and consistent character names. I would check transcript coverage and speaker attribution before calculating results. These scope and measurement choices are explicit assumptions made to give the question operational clarity.

## 3. Why notebook state is difficult to maintain

Cells in Jupyter notebooks can be executed in any order, while variables and other objects remain in memory between executions. The current state therefore depends on execution history, not just the code visible on the page.

Editing or deleting a cell does not automatically update or remove the values it previously created. This can leave outdated variables or displayed results and make an analysis difficult to understand or reproduce.

To reduce these problems, I would organize cells to run from top to bottom and regularly restart the kernel and run all cells. This checks that the notebook works from a clean state without relying on earlier, hidden execution steps.

## 4. Why share a notebook with future data-science collaborators?

A Jupyter notebook can be more useful than a README for sharing an analysis because it brings explanations, executable code, results, and visualizations together. Future collaborators can see how data was cleaned, how calculations were performed, and how results support the conclusions.

They can also rerun the analysis, change assumptions, and explore additional questions. This makes the notebook useful for both understanding and extending the work.

These benefits depend on clear organization, documented dependencies and data requirements, and successful execution from top to bottom. A README is still useful for setup and navigation, while the notebook provides a detailed, executable account of the analysis.
