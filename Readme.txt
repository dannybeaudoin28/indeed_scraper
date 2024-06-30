Chat GPT application: Resume builder / indeed scraper

desc: 			This program is designed to scrape indeed using a list of filters.
			After successfully scraping indeed for specific jobs it will then use 
			ChatGPT to dynamically create a tailored resume based on a users uploaded csv, 
			and the requirements of the job. 

			The program will then Generate PDF versions of the resume and allow the user to save the file to system.

			May use different programs for this concept. For example might create a PDF generator application, and a 			scraper application.

Scraper (Web App): 	The purpose of the scraper is to have the user provide search params for a query of indeeds website.
			The scraper will then construct a url string based on all the data that the client provides. 

			Upon successfully creating the url it will then take the result of the query and return all url's related 			to jobs that meet the criteria required by the client.

			The program will then call a seperate function that then scrapes the individual job advertisement. 

			Obtaining all relavent job information.

			Front End:	The front end will consist of a search bar, as well as radio buttons and selectors to add 
					paramas to the url search string. It will also contain a search button and reset button.

					The UI will then route to a component that displays a list of all jobs returned from the 					query. The user can then look through each job and deselect jobs, or click submit for all.

					upon submitting the user will be prompted to select a location to store the resume(s) and 					then the program will then hit the chat gpt integration micro service.

ChatGPT integrator: 	API:		This Api will send a copy of the users original resume, as well as the results of the 						scraper to have chatGPT automatically create a resume. The API will then return this as an 					http response to the scaper api and then call the PDF Generator.
(Micro Service)

PDF Generator:		CLI Program:	This program will take a large string as an input and generate a PDF document and return it 					as an output. Thus saving the PDF into the directory. Resulting in the user having 1 or 					more custom tailored resunes saved to the computers local filesystem