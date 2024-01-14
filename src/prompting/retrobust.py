nq_no_retrieval = """Given the following question, answer it by providing follow up questions and intermediate answers. If intermediate questions are not necessary, answer the question directly.
#
Question: how did the big red one get its name
Are follow up questions needed here: No.
So the final answer is: its shoulder patch
#
Question: where are the cayman islands on the map
Are follow up questions needed here: No.
So the final answer is: western Caribbean Sea
#
Question: who won the war between north korea and south korea
Are follow up questions needed here: No.
So the final answer is: technically still at war
#
Question: when does it's always sunny in philadelphia season 13 start
Are follow up questions needed here: No.
So the final answer is: September 5, 2018
#
Question: who sang you got a friend in me from toy story
Are follow up questions needed here: No.
So the final answer is: Randy Newman
# 
Question: when was the first person sent to space
Are follow up questions needed here: No.
So the final answer is: 12 April 1961
#
Question: """

nq_with_retrieval_at1 = """Given the following question, answer it by providing follow up questions and intermediate answers. If intermediate questions are not necessarry, answe the question directly. You are provided with evidence that can help you arrive at the answer before the question.
#
Context1: The Big Red One: Fuller was a World War II veteran and served with the 1st Infantry Division, which is nicknamed "The Big Red One" for the red numeral "1" on the division's shoulder patch. He received the Silver Star, Bronze Star, and Purple Heart during his service.
Question: how did the big red one get its name
Are follow up questions needed here: No.
So the final answer is: its shoulder patch
#
Context1: Location Map of Cayman Islands: The given Cayman Islands location map shows that the Cayman Islands are located in the western Caribbean Sea. Location Map of Cayman Islands. Where is Cayman ...
Question: where are the cayman islands on the map
Are follow up questions needed here: No.
So the final answer is: western Caribbean Sea
#
Context1: Korean War | Combatants, Summary, Years, Map ... - Britannica: After more than a million combat casualties had been suffered on both sides, the fighting ended in July 1953 with Korea still divided into two hostile states. Negotiations in 1954 produced no further agreement, and the front line has been accepted ever since as the de facto boundary between North and South Korea.
Question: who won the war between north korea and south korea
Are follow up questions needed here: No.
So the final answer is: technically still at war
#
Context1: It's Always Sunny in Philadelphia (season 13): The thirteenth season of the American comedy television series It\'s Always Sunny in Philadelphia premiered on FXX on September 5, 2018. ... The season consists of ...
Question: when does it's always sunny in philadelphia season 13 start
Are follow up questions needed here: No.
So the final answer is: September 5, 2018
#
Context1: You've Got a Friend in Me: "You've Got a Friend in Me" is a song by Randy Newman. Used as the theme song for the 1995 Disney/Pixar animated film Toy Story, it has since become a major ...
Question: who sang you got a friend in me from toy story
Are follow up questions needed here: No.
So the final answer is: Randy Newman
#
Context1: April 1961: Yuri Gagarin from the Soviet Union was the first human in space. His vehicle, Vostok 1 circled Earth at a speed of 27,400 kilometers per hour with the flight lasting 108 minutes.
Question: when was the first person sent to space
Are follow up questions needed here: No.
So the final answer is: 12 April 1961
#"""

nq_with_retrieval_at10 = """Given the following question, answer it by providing follow up questions and intermediate answers. If intermediate questions are not necessarry, answe the question directly. You are provided with evidence that can help you arrive at the answer before the question.
#
Context1: 16th Infantry Regiment (United States): As part of the new 1st Expeditionary Division, soon to become known as the "Big Red One," the 16th Infantry, commanded by William Herbert Allaire Jr., sailed
Question: how did the big red one get its name
Are follow up questions needed here: No.
So the final answer is: its shoulder patch
#
Context1: Module:Location map/data/Cayman Islands: Module:Location map/data/Cayman Islands is a location map definition used to overlay markers and labels on an equirectangular projection map of Cayman
Question: where are the cayman islands on the map
Are follow up questions needed here: No.
So the final answer is: western Caribbean Sea
#
Context1: First Battle of Seoul: The First Battle of Seoul, known in North Korean historiography as the Liberation of Seoul, was the North Korean capture of the South Korean capital, Seoul,
Question: who won the war between north korea and south korea
Are follow up questions needed here: No.
So the final answer is: technically still at war
#
Context1: It's Always Sunny in Philadelphia (season 13): The thirteenth season of the American comedy television series It's Always Sunny in Philadelphia premiered on FXX on September 5, 2018.
Question: when does it's always sunny in philadelphia season 13 start
Are follow up questions needed here: No.
So the final answer is: September 5, 2018
#
Context1: Randy Newman – You've Got a Friend in Me Lyrics: ”You've Got A Friend In Me” is the theme song of the Toy Story franchise, recurring throughout the series in different contexts. It's first
Question: who sang you got a friend in me from toy story
Are follow up questions needed here: No.
So the final answer is: Randy Newman
#
Context1: Timeline of space exploration: This is a timeline of space exploration which includes notable achievements, first accomplishments and milestones in humanity's exploration of outer space.
Question: when was the first person sent to space
Are follow up questions needed here: No.
So the final answer is: 12 April 1961
#"""

nq_with_retrieval_mix = """Given the following question, answer it by providing follow up questions and intermediate answers. If intermediate questions are not necessarry, answe the question directly. You are provided with evidence that can help you arrive at the answer before the question.
#
Context1: The Big Red One: Fuller was a World War II veteran and served with the 1st Infantry Division, which is nicknamed "The Big Red One" for the red numeral "1" on the division's shoulder patch. He received the Silver Star, Bronze Star, and Purple Heart during his service.
Question: how did the big red one get its name
Are follow up questions needed here: No.
So the final answer is: its shoulder patch
#
Context1: Module:Location map/data/Cayman Islands: Module:Location map/data/Cayman Islands is a location map definition used to overlay markers and labels on an equirectangular projection map of Cayman
Question: where are the cayman islands on the map
Are follow up questions needed here: No.
So the final answer is: western Caribbean Sea
#
Context1: Korean War | Combatants, Summary, Years, Map ... - Britannica: After more than a million combat casualties had been suffered on both sides, the fighting ended in July 1953 with Korea still divided into two hostile states. Negotiations in 1954 produced no further agreement, and the front line has been accepted ever since as the de facto boundary between North and South Korea.
Question: who won the war between north korea and south korea
Are follow up questions needed here: No.
So the final answer is: technically still at war
#
Context1: It's Always Sunny in Philadelphia (season 13): The thirteenth season of the American comedy television series It's Always Sunny in Philadelphia premiered on FXX on September 5, 2018.
Question: when does it's always sunny in philadelphia season 13 start
Are follow up questions needed here: No.
So the final answer is: September 5, 2018
#
Context1: You've Got a Friend in Me: "You've Got a Friend in Me" is a song by Randy Newman. Used as the theme song for the 1995 Disney/Pixar animated film Toy Story, it has since become a major ...
Question: who sang you got a friend in me from toy story
Are follow up questions needed here: No.
So the final answer is: Randy Newman
#
Context1: Timeline of space exploration: This is a timeline of space exploration which includes notable achievements, first accomplishments and milestones in humanity's exploration of outer space.
Question: when was the first person sent to space
Are follow up questions needed here: No.
So the final answer is: 12 April 1961
#"""
