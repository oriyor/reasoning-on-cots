strategyqa_decomposition = """Given the following question, answer it by providing follow up questions and intermediate answers. For each follow up question, you are given a context which is the top returned google snippet for the question from Wikipedia. If no follow up questions are necessary, answer the question directly.
#
Context1: Frost: Frost is a thin layer of ice on a solid surface, which forms from water vapor in an above-freezing atmosphere coming in contact with a solid surface whose ...
Context2: Graduation: Graduation is the awarding of a diploma to a student by an educational institution. It may also refer to the ceremony that is associated with it.
Context3: Winter: Winter ; Astronomical season, 22 December – 21 March ; Meteorological season, 1 December – 28/29 February ; Solar (Celtic) season, 1 November – 31 January.
Question: Is it common to see frost during some college commencements?
Are follow up questions needed here: Yes.
Follow up: What seasons can you expect to see frost?
Intermediate answer: Frost is common during the winter.
Follow up: When is college commencement?
Intermediate answer: College commencement ceremonies often happen during the months of December, May, June.
Follow up: Do any of the months December, May, June occur during the Winter?
Intermediate answer: December is in the winter.
So the final answer is: Yes.
#
Context1: War in Vietnam (1945–1946): [[\'Date\', \'September 13, 1945 – March 30, 1946 (6 months, 2 weeks and 3 days)\'], [\'Location\', \'Southern Vietnam below the 16th parallel\']]
Context2: Llama: The gestation period of a llama is 11.5 months (350 days). Dams (female llamas) do not lick off their babies, as they have an attached tongue that does not reach outside of the mouth more than 13 millimetres (1⁄2 inch). Rather, they will nuzzle and hum to their newborns.
Context3: Logarithm: In mathematics, the logarithm is the inverse function to exponentiation. That means the logarithm of a number x to the base b is the exponent to ... The binary logarithm uses base 2 and is frequently used in computer ...
Question: Could a llama birth twice during War in Vietnam (1945-46)?
Are follow up questions needed here: Yes.
Follow up: How long did the vietnam war (1945-1946) last?
Intermediate answer: The War in Vietnam (1945-46) lasted around 6 months.
Follow up: How long is the llama gestation period?
Intermediate answer: The gestation period for a llama is 11.5 months.
Follow up: What is 2 times 11.5?
Intermediate answer: 23, which is longer than 6.
So the final answer is: No.
#
Question: Do truck drivers generally also teach math?
Are follow up questions needed here: No.
So the final answer is: No.
#
Context1: Princeton University: She graduated from the Dwight-Englewood School in Englewood, New Jersey, in 1983. She went to Princeton University to pursue her bachelor's degree in French literature, where she graduated in 1987. So the answer is Princeton University.
Context2: Princeton University: Princeton University is a private research university in Princeton, New Jersey. Founded in 1746 in Elizabeth as the College of New Jersey, Princeton is ... It is one of the highest-ranked universities in the world.
Context3: University of Pennsylvania: It is the fourth-oldest institution of higher education in the United States and is ranked among the highest-regarded universities by numerous organizations and ...
Question: Could Brooke Shields succeed at University of Pennsylvania?
Are follow up questions needed here: Yes.
Follow up: What college did Brooke Shields go to?
Intermediate answer: Brooke Shields graduated from Princeton University.
Follow up: Out of all colleges in the US, how is Princeton University ranked?
Intermediate answer: Princeton is ranked as the number 1 national college by US news.
Follow up: Is the ranking of University of Pennsylvania similar to Princeton University?
Intermediate answer: University of Pennsylvania is also ranked at the top 10 national colleges by US news.
So the final answer is: Yes.
#
Context1: 23 April 1616: William Shakespeare ( bapt. 26 April 1564 – 23 April 1616) was an English playwright, poet and actor. So the answer is 23 April 1616.
Context2: Email: The original usage in June 1979 occurred in the journal Electronics in reference to the United States Postal Service initiative called E-COM, which was developed in the late 1970s and operated in the early 1980s.
Context3: List of years: This page indexes the individual years pages. Contents. 1 3rd millennium. 1.1 21st century. 2 2nd millennium. 2.1 20th century; 2.2 19th century ...
Question: Did William Shakespeare ever email his friends?
Are follow up questions needed here: Yes.
Follow up: When did William Shakespeare die?
Intermediate answer: William Shakespeare died on 23 April 1616.
Follow up: When was the email invented?
Intermediate answer: The email was invented in 1971.
Follow up: Is 1616 before 1971?
Intermediate answer: Yes, 1616 is before 1971.
So the final answer is: No.
#
Context1: Hamster: Hamsters are rodents (order Rodentia) belonging to the subfamily Cricetinae, which contains 19 species classified in seven genera. They have become established as popular small pets. The best-known species of hamster is the golden or Syrian hamster (Mesocricetus auratus), which is the type most commonly kept as pets.
Context2: Predation: Predation is a biological interaction where one organism, the predator, kills and eats another organism, its prey. It is one of a family of common feeding ...
Question: Do hamsters provide food for any animals?
Are follow up questions needed here: Yes.
Follow up: What types of animals are hamsters?
Intermediate answer: Hamsters are prey animals.
Follow up: Do prey animals provide food for any other animals?
Intermediate answer: Prey animals provide food for predators.
So the final answer is: Yes.
#
Question: Do the Druze believe in reincarnation?
Are follow up questions needed here: No.
So the final answer is: Yes.
#
Context1: about 1 gram per cubic centimetre: The density of water is about 1 gram per cubic centimetre (62 lb/cu ft): this relationship was originally used to define the gram. So the answer is about 1 gram per cubic centimetre.
Context2: Gram per cubic centimetre: The density of water is about 1 g/cm3, since the gram was originally defined as the mass of one cubic centimetre of water at its maximum density at 4 °C.
Question: Would a pear sink in water?
Are follow up questions needed here: Yes.
Follow up: What is the density of a pear?
Intermediate answer: The density of a raw pear is about 0.59 g/cm^3.
Follow up: What is the density of water?
Intermediate answer: The density of water is about 1 g/cm^3.
Follow up: Is 0.59 g/cm^3 greater than 1 g/cm^3?
Intermediate answer: 0.59 g/cm^3 is less than 1 g/cm^3.
So the final answer is: No.
#
Context1: Last rites: The last rites, also known as the Commendation of the Dying, are the last prayers and ministrations given to an individual of Christian faith, when possible, shortly before death. They may be administered to those awaiting execution, mortally injured, or terminally ill.
Context2: Richard Dawkins: Dawkins is an outspoken atheist and a supporter of various atheist, secular, and humanist organisations, including Humanists UK and the Brights movement. Dawkins suggests that atheists should be proud, not apologetic, stressing that atheism is evidence of a healthy, independent mind.
Context3: Prayer in the Catholic Church: In the Catholic Church, prayer is "the raising of one\'s mind and heart to God or the requesting of good things from God." It is an act of the moral virtue ...
Question: Would Richard Dawkins hypothetically refuse an offering of the Last rites?
Are follow up questions needed here: Yes.
Follow up: What are the last Rites?
Intermediate answer: The Last rites, in Catholicism, are the last prayers and ministrations given to an individual of the faith, when possible, shortly before death.
Follow up: What are Richard Dawkins religious beliefs?
Intermediate answer:  Richard Dawkins is known as an outspoken atheist, well known for his criticism of creationism and intelligent design.
Follow up: Would an atheist participate in Catholics prayers?
Intermediate answer:  It is unlikely that an atheist would participate in Catholics prayers.
So the final answer is: Yes.
#
Context1: number 1: Hydrogen is the chemical element with the symbol H and atomic number 1. Hydrogen is the lightest element. So the answer is number 1.
Context2: Spice Girls - Simple English Wikipedia, the free encyclopedia: The group has five members. Each member uses a nickname initially given to them: Melanie Chisholm ("Sporty Spice"), Emma Bunton ("Baby Spice"), Melanie Brown ("Scary Spice"), Victoria Beckham (née Adams) ("Posh Spice"), and Geri Halliwell ("Ginger Spice") .
Context3: Square number: In mathematics, a square number or perfect square is an integer that is the square of an integer; in other words, it is the product of some integer with ...
Question: Hydrogen's atomic number squared exceeds number of Spice Girls?
Are follow up questions needed here: Yes.
Follow up: What is the atomic number of hydrogen?
Intermediate answer: Hydrogen has an atomic number of 1.
Follow up: How many people are in the Spice Girls band?
Intermediate answer: The Spice Girls has 5 members.
Follow up: Is the square of 1 greater than 5?
Intermediate answer: The square of 1 is 1 which is less than 5.
So the final answer is: No.
#"""

strategy_mcr = """Given a question and a context, provide a Yes or No answer and explain why. If you are unsure, answer Unknown.

#
Context:
What type of animal is a jellyfish? A jellyfish is a type of invertebrate.
Do jellyfish have arteries? No, jellyfish do not have arteries. They have a type of nervous system called a nerve net.
What is atherosclerosis? Atherosclerosis is a disease where plaque builds up in the arteries.
Do jellyfish have arteries? Jellyfish do not have a circulatory system and therefore do not have arteries.
So jellyfish don't have atherosclerosis because they don't have arteries? Yes, that is correct.
What is atherosclerosis? Atherosclerosis is a type of heart disease.
Is an invertebrate susceptible to atherosclerosis? No, invertebrates are not susceptible to atherosclerosis.
What is atherosclerosis? Atherosclerosis is a disease in which plaque builds up on the walls of the arteries.

Question:
Is a jellyfish safe from atherosclerosis?

Answer:
Jellyfish do not have a circulatory system and therefore do not have arteries. Atherosclerosis is a disease in which plaque builds up on the walls of the arteries.
So the answer is: Yes.
#
Context:
Is 242 mph greater than 130 mph? Yes, 242 mph is greater than 130 mph.
Is 130 mph greater than 200 mph? No, 130 mph is less than 200 mph.
What is the top wind speed of Hurricane Harvey? Hurricane Harvey had top wind speeds of 130 mph.
What is the top wind speed of a Peregrine falcon? A Peregrine falcon can fly at speeds of up to 200 mph.
Is 240 mph greater than 130 mph? 240 mph is greater than 130 mph.
How fast can Hurricane Harvey winds go? Hurricane Harvey can have wind speeds up to 130 mph.
How fast can a Peregrine falcon fly? The Peregrine falcon is the fastest bird, and can fly up to 242 mph.
How fast can a Peregrine falcon fly? The Peregrine falcon can fly up to 240 mph.
How fast can Hurricane Harvey winds travel? Hurricane Harvey winds can travel up to 130 mph.

Question:
Could Hurricane Harvey catch a Peregrine falcon?

Answer:
Hurricane Harvey had top wind speeds of 130 mph. A Peregrine falcon can fly at speeds of up to 200 mph. 130 mph is less than 200 mph.
So the answer is: No.
#
Context:
Who is Donald Trump? Donald Trump is the 45th President of the United States.
What has Donald Trump said about Muslims? Donald Trump has said many things that can be perceived as Islamophobic such as "Islam hates us" and "I think Islam is a problem in the world.
Is Donald Trump a Muslim? No, Donald Trump is not a Muslim.
What is Islamophobia? Islamophobia is the fear, hatred of, or prejudice against, the Islamic religion or Muslims.
What is the definition of Islamophobia? Islamophobia is the fear or hatred of Islam.
Did Donald Trump show any fear or hatred of Islam? Yes, Donald Trump has made multiple statements that are critical of Islam.
What is Islamophobia? Islamophobia is the fear or hatred of Muslims.
Do Donald Trump's comments fit the definition of Islamophobia? Yes, Donald Trump's comments about Islam fit the definition of Islamophobia.

Question:
Was Donald Trump the target of Islamophobia?

Answer:
Islamophobia is the fear or hatred of Islam. Donald Trump is not a Muslim.
So the answer is: No.
#
Context:
When was Stone Cold Steve Austin born? Stone Cold Steve Austin was born on December 18, 1964.
What is the latest year Stone Cold Steve Austin could have wrestled in? The latest year Stone Cold Steve Austin could have wrestled in is 1999.
What is Stone Cold Steve Austin's birthdate? Stone Cold Steve Austin was born on December 18, 1964.
What centuries do those years belong to? 1964 and 1989 belong to the 20th century, and 2003 belongs to the 21st century.
What centuries did December 18, 1964 fall in? December 18, 1964 falls in the 20th century.
Did Stone Cold Steve Austin wrestle in the 20th century? Yes.
What years was Stone Cold Steve Austin born and active as a wrestler? Stone Cold Steve Austin was born in 1964 and was an active wrestler from 1989-2003.
What is the earliest year Stone Cold Steve Austin could have wrestled in? The earliest year Stone Cold Steve Austin could have wrestled in is 1900.

Question:
Did Stone Cold Steve Austin wrestle in two different centuries?

Answer:
Stone Cold Steve Austin was born in 1964 and was an active wrestler from 1989-2003. 1964 and 1989 belong to the 20th century, and 2003 belongs to the 21st century.
So the answer is: Yes.
#
Context:
What is tonsure? Tonsure is the practice of cutting or shaving the hair from the scalp, as a sign of religious devotion or humility.
What is Christopher Hitchens' religious affiliation? Christopher Hitchens was an atheist.
What is tonsure? Tonsure is a practice of cutting or shaving the hair from the scalp.
Would Christopher Hitchens be likely to do something as a sign of religious devotion? No.
Would Christopher Hitchens be religious? Christopher Hitchens was an atheist.
Is an atheist likely to engage in religious practices? No, an atheist is not likely to engage in religious practices.
What is tonsure? Tonsure is the practice of cutting or shaving the hair from the scalp, as a sign of religious devotion or humility.
What is Christopher Hitchens' religious affiliation? Christopher Hitchens was an atheist.
Do atheists usually engage in tonsure? No, atheists do not usually engage in tonsure as it is a religious practice.

Question:
Would Christopher Hitchens be very unlikely to engage in tonsure?

Answer:
Tonsure is the practice of cutting or shaving the hair from the scalp, as a sign of religious devotion or humility. Christopher Hitchens was an atheist. An atheist is not likely to engage in religious practices.
So the answer is: Yes.
#
Context:
What is the evidence that Neanderthals used arithmetic? There is no direct evidence that Neanderthals used arithmetic, but indirect evidence suggests that they may have had some understanding of basic mathematical concepts.
What is the earliest evidence of arithmetic? The earliest evidence of arithmetic dates back to the ancient Sumerians, who lived in what is now modern-day Iraq.
Did Neanderthals live before the ancient Sumerians? Yes.
What is arithmetic? Arithmetic is the branch of mathematics that deals with the properties and manipulation of numbers.
Is there any reason to believe that Neanderthals could not have used arithmetic? There is no reason to believe that Neanderthals could not have used arithmetic.
Do we have any evidence that Neanderthals could manipulate numbers? We have no evidence that Neanderthals could manipulate numbers.
What is arithmetic? Arithmetic is the branch of mathematics that deals with the properties and manipulation of numbers.
What is arithmetic? Arithmetic is the branch of mathematics that deals with the addition, subtraction, multiplication, and division of whole numbers and with the manipulation of fractions and decimals.

Question:
Did Neanderthals use arithmetic?

Answer:
There is no evidence that Neanderthals used arithmetic. The earliest evidence of arithmetic dates back to the ancient Sumerians who lived after the Neanderthals.
So the answer is: No.
#
Context:"""

wikihop_entailment = """Given a question and a context, answer the question and explain why. If you are unsure, answer Unknown.
#
Context:
Who is the wife of Douglas Leiterman? The wife of Douglas Leiterman is Beryl Fox.
Where was Beryl Fox born? Beryl Fox was born in Winnipeg, Manitoba.
Who is the wife of Douglas Leiterman? The wife of Douglas Leiterman is Beryl Fox.
Where was Beryl Fox born? Beryl Fox was born in Winnipeg, Manitoba.
Who is the wife of Douglas Leiterman? The wife of Douglas Leiterman is Mary.
When and where was Mary born? Mary was born in c. 18 BC or September 8 (21), 16 BC Herodian Kingdom of Judea.

Question:
Where was the wife of Douglas Leiterman born?

Answer:
The wife of Douglas Leiterman is Beryl Fox. Beryl Fox was born in Winnipeg, Manitoba.
So the answer is: Winnipeg, Manitoba.
#
Context:
Who is the director of El extraño viaje? The director of El extraño viaje is Fernando Fernán Gómez.
Who is the director of Love in Pawn? The director of Love in Pawn is Charles Saunders.
When was Fernando Fernán Gómez born? Fernando Fernán Gómez was born on 28 August 1921.
When was Charles Saunders born? Charles Saunders was born on July 12, 1946.
Who is the director of El extraño viaje? The director of El extraño viaje is Fernando Fernán Gómez.
When was Fernando Fernán Gómez born? Fernando Fernán Gómez was born on 28 August 1921.
Who is the director of Love in Pawn? The director of Love in Pawn is Charles Saunders.
When was Charles Saunders born? Charles Saunders was born on July 12, 1946.
Who is the director of El extraño viaje? The director of El extraño viaje is Fernando Fernán Gómez
Who is the director of Love in Pawn? The director of Love in Pawn is Charles Saunders.
When was Fernando Fernán Gómez born? Fernando Fernán Gómez was born on 28 August 1921.
When was Charles Saunders (director) born? Charles Saunders (director) was born on 8 April 1904.

Question:
Which film has the director who was born later, El Extraño Viaje or Love In Pawn?

Answer:
The director of El extraño viaje is Fernando Fernán Gómez. The director of Love in Pawn is Charles Saunders. Fernando Fernán Gómez was born on 28 August 1921. Charles Saunders (director) was born on 8 April 1904.
So the answer is: El extraño viaje.
#
Context:
What year did Blind Shaft come out? Blind Shaft came out in 2003.
What year did The Mask of Fu Manchu come out? The Mask of Fu Manchu came out in 1932.
When did Blind Shaft come out? Blind Shaft came out in 2003.
When did The Mask of Fu Manchu come out? The Mask of Fu Manchu came out on December 2, 1932.
When was the film Blind Shaft released? Blind Shaft was released on 4 February 2004.
When was the film The Mask of Fu Manchu released? The Mask of Fu Manchu was released on December 2, 1932.

Question:
Which film came out first, Blind Shaft or The Mask Of Fu Manchu?

Answer:
Blind Shaft came out in 2003. The Mask of Fu Manchu came out in 1932. 
So the answer is: The Mask of Fu Manchu.
#
Context:
When did John V, Prince Of Anhalt-Zerbst's father die? The father of John V, Prince of Anhalt-Zerbst is Ernest I, Prince of Anhalt-Dessau.
When did Ernest I, Prince of Anhalt-Dessau die? Ernest I, Prince of Anhalt-Dessau died on 12 June 1516.
Who is the father of John V, Prince of Anhalt-Zerbst? The father of John V, Prince of Anhalt-Zerbst is Ernest I, Prince of Anhalt-Dessau.
When did Ernest I, Prince of Anhalt-Dessau die? Ernest I, Prince of Anhalt-Dessau died on 12 June 1516.
Who is the father of John V, Prince of Anhalt-Zerbst? The father of John V, Prince of Anhalt-Zerbst is Ernest I, Prince of Anhalt-Dessau.
When did Ernest I, Prince of Anhalt-Dessau die? Ernest I, Prince of Anhalt-Dessau died on 12 June 1516.

Question:
When did John V, Prince Of Anhalt-Zerbst's father die?

Answer:
The father of John V, Prince of Anhalt-Zerbst is Ernest I, Prince of Anhalt-Dessau. Ernest I, Prince of Anhalt-Dessau died on 12 June 1516.
So the answer is: 12 June 1516.
#
Context:
Who is the husband of Catherine of Pomerania? The husband of Catherine of Pomerania is John II, Count Palatine of Neumarkt.
Who is the father of John II, Count Palatine of Neumarkt? The father of John II, Count Palatine of Neumarkt is Rupert III, Elector Palatine.
Who are the parents of Rupert III, Elector Palatine? The parents of Rupert III, Elector Palatine are Rupert II, Elector Palatine and Beatrice of Aragon.
Who is Beatrice of Aragon's father? The father of Beatrice of Aragon is King Ferdinand I of Naples.
Who is Catherine Of Pomerania, Countess Palatine Of Neumarkt's husband? The husband of Catherine Of Pomerania, Countess Palatine Of Neumarkt is John I, Count Palatine of Neumarkt.
Who is the father of John I, Count Palatine of Neumarkt? The father of John I, Count Palatine of Neumarkt is Rupert III, Elector Palatine.
Who is the father of Rupert III, Elector Palatine? The father of Rupert III, Elector Palatine is Rupert II, Elector Palatine.
Who is Catherine Of Pomerania, Countess Palatine Of Neumarkt's husband? The husband of Catherine Of Pomerania, Countess Palatine Of Neumarkt is John II, Count of Holstein-Rendsburg.
Who is the father of John II, Count of Holstein-Rendsburg? The father of John II, Count of Holstein-Rendsburg is Henry II, Count of Holstein-Rendsburg.

Question:
Who is Catherine Of Pomerania, Countess Palatine Of Neumarkt's father-in-law?

Answer:
The husband of Catherine Of Pomerania, Countess Palatine Of Neumarkt is John I, Count Palatine of Neumarkt. The father of John I, Count Palatine of Neumarkt is Rupert III, Elector Palatine.
So the answer is: Rupert III, Elector Palatine.
#
Context:
Who is the director of Crimen A Las Tres? The director of Crimen A Las Tres is Luis Saslavsky.
Who is the director of The Working Class Goes to Heaven? The director of The Working Class Goes to Heaven is Elio Petri.
When did Luis Saslavsky die? Luis Saslavsky died on March 20, 1995.
When did Elio Petri die? Elio Petri died on 10 November 1982.
Who is the director of Crimen A Las Tres? The director of Crimen A Las Tres is Luis Saslavsky.
Who is the director of The Working Class Goes to Heaven? The director of The Working Class Goes to Heaven is Elio Petri.
When did Luis Saslavsky die? Luis Saslavsky died on March 20, 1995.
When did Elio Petri die? Elio Petri died on 10 November 1982.
Who is the director of Crimen A Las Tres? The director of Crimen A Las Tres is Luis Saslavsky.
When did Luis Saslavsky die? Luis Saslavsky died on March 20, 1995.
Who is the director of The Working Class Goes to Heaven? The director of The Working Class Goes to Heaven is Elio Petri.
When did Elio Petri die? Elio Petri died on 10 November 1982.

Question:
Which film has the director died first, Crimen A Las Tres or The Working Class Goes To Heaven?

Answer:
The director of Crimen A Las Tres is Luis Saslavsky. The director of The Working Class Goes to Heaven is Elio Petri. Luis Saslavsky died on March 20, 1995. Elio Petri died on 10 November 1982.
So the answer is: The Working Class Goes To Heaven.
#
Context:"""

wikihop_decompositions_with_retrieval_context_first = """Given the following question, answer it by providing follow up questions and intermediate answers. If no follow up questions are necessary, answer the question directly. You are also provided with the most relevant google snippet for each intermediate question.
#
Context1: Xawery Żuławski: Polish-Russian War (Wojna polsko-ruska) is a 2009 Polish film directed by Xawery Żuławski based on the novel Polish-Russian War under the white-red flag by Dorota Masłowska. So the answer is Xawery Żuławski.
Context2: Xawery Żuławski: Xawery Żuławski ; National Film School in Łódź · 1995–present · Maria Strzelecka · 2.
Question: Who is the mother of the director of film Polish-Russian War (Film)?
Are follow up questions needed here: Yes.
Follow up: Who is the director of the film Polish-Russian War (Film)?
Intermediate answer: The director of the film Polish-Russian War is Xawery Żuławski.
Follow up: Who is the mother of Xawery Żuławski?
Intermediate answer: The mother of Xawery Żuławski is Małgorzata Braunek.
So the final answer is: Rick Scott Małgorzata Braunek.
#
Context1: 2003: Blind Shaft (Chinese: 盲井; pinyin: Mángjǐng) is a 2003 film about a pair of brutal con artists operating in the illegal coal mines of present-day northern China. So the answer is 2003.
Context2: December 2, 1932: Release and reception. The Mask of Fu Manchu opened in New York on December 2, 1932. The film cost a total of $338,000 and had worldwide rentals of $625,000. It had a profit of $62,000. So the answer is December 2, 1932.
Question: Which film came out first, Blind Shaft or The Mask Of Fu Manchu?
Are follow up questions needed here: Yes.
Follow up: When did Blind Shaft come out?
Intermediate answer: Blind Shaft came out in 2003.
Follow up: When did The Mask Of Fu Manchu come out?
Intermediate answer: The Mask Of Fu Manchu came out in 1932.
So the final answer is: The Mask Of Fu Manchu.
#
Context1: John V, Prince of Anhalt-Zerbst: John was the second (but eldest surviving) son of Ernest I, Prince of Anhalt-Dessau, by his wife Margarete, daughter of Henry I, Duke of Münsterberg-Oels, and granddaughter of George of Poděbrady, King of Bohemia.
Context2: 12 June 1516: Ernest I, Prince of Anhalt-Dessau (died Dessau, 12 June 1516), was a German prince of the House of Ascania and ruler of the principality of Anhalt-Dessau. So the answer is 12 June 1516.
Question: When did John V, Prince Of Anhalt-Zerbst's father die?
Are follow up questions needed here: Yes.
Follow up: Who is the father of John V, Prince Of Anhalt-Zerbst?
Intermediate answer: The father of John V, Prince Of Anhalt-Zerbst is Ernest I, Prince of Anhalt-Dessau.
Follow up: When did Ernest I, Prince of Anhalt-Dessau die?
Intermediate answer: Ernest I, Prince of Anhalt-Dessau died on 12 June 1516.
So the final answer is: 12 June 1516
#
Context1: El extraño viaje: El extraño viaje (English: The Strange Voyage) is a 1964 Spanish black drama film directed by Fernando Fernán Gómez.
Context2: Love in Pawn: Love in Pawn is a 1953 British comedy film directed by Charles Saunders and starring Bernard Braden, Barbara Kelly and Jeannie Carson.
Context3: 28 August 1921: Fernando Fernández Gómez (28 August 1921 – 21 November 2007) better known as Fernando Fernán Gómez was a Spanish actor, screenwriter, film director, theater director and member of the Royal Spanish Academy for seven years. So the answer is 28 August 1921.
Context4: Charles Saunders (director): Charles Joel Saunders (8 April 1904 – 20 April 1997) was an English film director and screenwriter who began in the industry as a film editor, and who also contributed to television.
Question: Which film has the director who was born later, El Extraño Viaje or Love In Pawn?
Are follow up questions needed here: Yes.
Follow up: Who is the director of El Extraño Viaje?
Intermediate answer: The director of El Extraño Viaje is Fernando Fernán Gómez.
Follow up: Who is the director of Love in Pawn?
Intermediate answer: The director of Love in Pawn is Charles Saunders.
Follow up: When was Fernando Fernán Gómez born?
Intermediate answer: Fernando Fernán Gómez was born on 28 August 1921.
Follow up: When was Charles Saunders (director) born?
Intermediate answer: Charles Saunders was born on 8 April 1904.
So the final answer is: El Extraño Viaje.
#
Context1: John, Count Palatine of Neumarkt: John (Johann von Pfalz-Neumarkt; 1383 – 14 March 1443) was the Count Palatine of Neumarkt from 1410 to his death. The son of Rupert III of the Palatinate, he married Catherine of Pomerania in 1407.
Context2: John, Count Palatine of Neumarkt: John (Johann von Pfalz-Neumarkt; 1383 – 14 March 1443) was the Count Palatine of Neumarkt from 1410 to his death. The son of Rupert III of the Palatinate, he married Catherine of Pomerania in 1407.
Question: Who is Catherine Of Pomerania, Countess Palatine Of Neumarkt's father-in-law?
Are follow up questions needed here: Yes.
Follow up: Who is the husband of Catherine of Pomerania, Countess Palatine of Neumarkt?
Intermediate answer: The husband of Catherine of Pomerania, Countess Palatine of Neumarkt is John, Count Palatine of Neumarkt.
Follow up: Who is the father of John, Count Palatine of Neumarkt?
Intermediate answer: The father of John, Count Palatine of Neumarkt is Rupert III of the Palatinate.
So the final answer is: Rupert III of the Palatinate.
#
Context1: Crimen a las tres: Crimen a las tres is a 1935 Argentine crime film directed and written by Luis Saslavsky. Crimen a las tres. Directed by, Luis Saslavsky.
Context2: Elio Petri: The Working Class Goes to Heaven (Italian: La classe operaia va in paradiso), released in the US as Lulu the Tool, is a 1971 political drama film directed by Elio Petri. So the answer is Elio Petri.
Context3: March 20, 1995: Luis Saslavsky (April 21, 1903 – March 20, 1995) was an Argentine film director, screenwriter and film producer, and one of the influential directors in the Cinema of Argentina of the classic era. So the answer is March 20, 1995.
Context4: Elio Petri: Final years. In 1981, Petri visited Geneva to direct Arthur Miller\'s new play The American Clock, with Marcello Mastroianni playing the lead role. Petri died of cancer on 10 November 1982. He was 53 years old.
Question: Which film has the director died first, Crimen A Las Tres or The Working Class Goes To Heaven?
Are follow up questions needed here: Yes.
Follow up: Who is the director of Crimen a las tres?
Intermediate answer: The director of Crimen a las tres is Luis Saslavsky.
Follow up: Who is the director of The Working Class Goes to Heaven?
Intermediate answer: The director of The Working Class Goes to Heaven is Elio Petri.
Follow up: When did Luis Saslavsky die?
Intermediate answer: Luis Saslavsky died on March 20, 1995.
Follow up: When did Elio Petri die?
Intermediate answer: Elio Petri died on 10 November 1982.
So the final answer is: The Working Class Goes to Heaven
#"""
